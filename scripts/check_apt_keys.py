#!/usr/bin/env python3
"""Check the apt repository signing keys managed by the apt_keys role.

Two layers, both driven by the single manifest in
roles/apt_keys/defaults/main.yml:

  Layer 1 (always): static inspection with gpg. For each keyring, find the
  keys that are still usable (not expired/revoked/invalid/disabled) and the
  date by which the longest-lived of them expires. Warn when that date is
  within --days, fail when no usable key remains. Bundled historical/expired
  subkeys are ignored, which is why a keyring like yarn's (old expired subkeys
  alongside current ones) is reported healthy.

  Layer 2 (--live, needs apt/Debian): prove the key still verifies its repo by
  running `apt-get update` against it. Catches upstream revocation/rotation
  that static inspection cannot see. A genuine key failure (EXPKEYSIG /
  REVKEYSIG / KEYEXPIRED / NO_PUBKEY) is fatal; an unreachable repo or missing
  suite is reported inconclusive, not fatal. Whether a signature is accepted
  depends on the apt of the Debian release this runs under (trixie's sequoia
  apt rejects SHA1 bindings, bookworm's gpgv does not), so run it once inside
  each debian:<release> image you care about — the suite codename is
  auto-detected from there.

Also guards against drift: every keyring file must be registered in the
manifest and vice versa.

Exit status: 2 if any keyring is broken (no usable key, live key failure, or
drift); 0 otherwise (including expiring-soon warnings). A summary of anything
worth alerting on is written to --report-file when provided.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "roles" / "apt_keys" / "defaults" / "main.yml"
DEFAULT_FILES_DIR = REPO_ROOT / "roles" / "apt_keys" / "files"

# Substrings apt/gpgv/sqv print when a repository's signature cannot be
# verified with the configured key (expired, revoked, rotated, or — on
# trixie's sequoia-based apt — bound with a now-disallowed SHA1 signature).
SIG_FAIL_MARKERS = (
    "EXPKEYSIG", "REVKEYSIG", "KEYEXPIRED", "NO_PUBKEY",
    "is not signed",
    "signature verification failed",
    "following signatures were invalid",
    "public key is not available",
)
# gpg validity codes that mean a key cannot be used to verify a repo.
UNUSABLE_VALIDITY = {"e", "r", "i", "d"}  # expired, revoked, invalid, disabled

OK, WARNING, CRITICAL, NOTICE = "OK", "WARNING", "CRITICAL", "NOTICE"


def detect_release(default: str = "trixie") -> str:
    """Return the running container's Debian codename, for matching suites."""
    try:
        for line in Path("/etc/os-release").read_text().splitlines():
            if line.startswith("VERSION_CODENAME="):
                return line.split("=", 1)[1].strip().strip('"') or default
    except OSError:
        pass
    return default


def load_entries(manifest: Path) -> list[dict]:
    data = yaml.safe_load(manifest.read_text())
    return data["apt_keys_keyrings"]


def gpg_key_records(keyring: Path) -> list[tuple[str, int | None]]:
    """Return (validity, expiry_epoch|None) for each pub/sub in the keyring."""
    home = tempfile.mkdtemp(prefix="apt-keys-gpg-")
    env = {**os.environ, "GNUPGHOME": home}
    try:
        proc = subprocess.run(
            ["gpg", "--no-default-keyring", "--show-keys",
             "--with-colons", str(keyring)],
            capture_output=True, text=True, env=env, check=False,
        )
    finally:
        shutil.rmtree(home, ignore_errors=True)
    records: list[tuple[str, int | None]] = []
    for line in proc.stdout.splitlines():
        fields = line.split(":")
        if fields[0] in ("pub", "sub"):
            validity = fields[1]
            expiry = int(fields[6]) if len(fields) > 6 and fields[6] else None
            records.append((validity, expiry))
    return records


def check_static(keyring: Path, days: int) -> tuple[str, str]:
    records = gpg_key_records(keyring)
    if not records:
        return CRITICAL, "no OpenPGP keys found (unreadable keyring?)"
    usable = [exp for validity, exp in records if validity not in UNUSABLE_VALIDITY]
    if not usable:
        revoked = any(v == "r" for v, _ in records)
        return CRITICAL, "all keys revoked" if revoked else "all keys expired"
    if any(exp is None for exp in usable):
        return OK, "a usable key never expires"
    last_expiry = max(usable)
    date = time.strftime("%Y-%m-%d", time.gmtime(last_expiry))
    days_left = int((last_expiry - time.time()) // 86400)
    if days_left <= days:
        return WARNING, f"all usable keys expire by {date} ({days_left}d left)"
    return OK, f"usable until {date} ({days_left}d left)"


def _release_lines(output: str, *prefixes: str) -> bool:
    """True if any 'Get:/Hit:/Err:' line refers to a (In)Release file."""
    for line in output.splitlines():
        tag = line.split(":", 1)[0]
        if tag in prefixes and ("InRelease" in line or "Release" in line):
            return True
    return False


def _conclusive(output: str) -> bool:
    """A signature failure, or a successfully fetched Release, ends retries."""
    if any(m in output for m in SIG_FAIL_MARKERS):
        return True
    return _release_lines(output, "Get", "Hit")


def run_apt_update(sources: str, retries: int = 3) -> str:
    """Run apt-get update against a single isolated sources file."""
    tmp = tempfile.mkdtemp(prefix="apt-keys-live-")
    parts = Path(tmp) / "sources.list.d"
    parts.mkdir()
    (parts / "key-check.sources").write_text(sources)
    cmd = [
        "apt-get", "update",
        "-o", "Dir::Etc::sourcelist=/dev/null",
        "-o", f"Dir::Etc::sourceparts={parts}",
        "-o", "Acquire::Languages=none",
    ]
    output = ""
    try:
        for attempt in range(retries):
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            output = proc.stdout + proc.stderr
            if proc.returncode == 0 or _conclusive(output):
                break
            time.sleep(3 * (attempt + 1))  # transient network: back off and retry
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return output


def check_live(entry: dict, files_dir: Path, release: str) -> tuple[str, str]:
    repo = entry.get("repo")
    if not repo:
        return NOTICE, "no repo coordinates in manifest; live check skipped"
    dest = Path(entry["dest"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(files_dir / entry["src"], dest)
    suites = repo["suites"].replace("{release}", release)
    uris = repo["uris"].replace("{release}", release)
    sources = (
        "Types: deb\n"
        f"URIs: {uris}\n"
        f"Suites: {suites}\n"
        f"Components: {repo['components']}\n"
        f"Signed-By: {dest}\n"
        "Enabled: yes\n"
    )
    output = run_apt_update(sources)
    marker = next((m for m in SIG_FAIL_MARKERS if m in output), None)
    if marker:
        return CRITICAL, f"apt rejected the repository signature ('{marker}') for {suites}"
    if _release_lines(output, "Get", "Hit"):
        return OK, f"apt verified the key for {suites}"
    return NOTICE, f"repo unreachable for {suites}; key not verified"


def check_drift(entries: list[dict], files_dir: Path) -> list[str]:
    registered = {e["src"] for e in entries}
    present = {p.name for p in files_dir.iterdir() if p.suffix in (".gpg", ".asc")}
    problems = []
    for src in sorted(registered - present):
        problems.append(f"manifest references missing keyring file: {src}")
    for name in sorted(present - registered):
        problems.append(f"keyring file not registered in manifest: {name}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=30,
                        help="warn when a keyring's last usable key expires within N days")
    parser.add_argument("--live", action="store_true",
                        help="also run apt-get update against each repo (needs apt)")
    parser.add_argument("--release", default=None,
                        help="Debian release for {release} in suites "
                             "(default: the running container's codename)")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--files-dir", type=Path, default=DEFAULT_FILES_DIR)
    parser.add_argument("--report-file", type=Path,
                        help="write a summary of alerts here (for Slack)")
    args = parser.parse_args()

    entries = load_entries(args.manifest)
    release = args.release or detect_release()
    alerts: list[str] = []
    has_critical = False

    drift = check_drift(entries, args.files_dir)
    if drift:
        has_critical = True
        alerts.extend(f"DRIFT: {d}" for d in drift)
        for d in drift:
            print(f"[CRITICAL] {d}")

    width = max(len(e["name"]) for e in entries)
    for entry in entries:
        status, detail = check_static(args.files_dir / entry["src"], args.days)
        print(f"{entry['name']:<{width}}  {'static':<14}  {status:<8}  {detail}")
        if status in (WARNING, CRITICAL):
            alerts.append(f"{entry['name']}: {detail}")
            has_critical = has_critical or status == CRITICAL

        if args.live:
            kind = f"live[{release}]"
            applicable = entry.get("releases")
            if applicable and release not in applicable:
                print(f"{entry['name']:<{width}}  {kind:<14}  {'SKIP':<8}  not offered on {release} (releases: {', '.join(applicable)})")
            else:
                lstatus, ldetail = check_live(entry, args.files_dir, release)
                print(f"{entry['name']:<{width}}  {kind:<14}  {lstatus:<8}  {ldetail}")
                if lstatus == CRITICAL:
                    alerts.append(f"{entry['name']}: {ldetail}")
                    has_critical = True

    if args.report_file and alerts:
        scope = f" on {release}" if args.live else ""
        header = f"apt key check found issues{scope}:\n"
        args.report_file.write_text(header + "\n".join(f"- {a}" for a in alerts) + "\n")

    if (gh_out := os.environ.get("GITHUB_OUTPUT")):
        with open(gh_out, "a") as fh:
            fh.write(f"alert={'true' if alerts else 'false'}\n")

    print()
    if has_critical:
        print("RESULT: CRITICAL — one or more keyrings are broken.")
        return 2
    if alerts:
        print("RESULT: WARNING — one or more keyrings expire soon.")
        return 0
    print("RESULT: OK — all keyrings healthy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
