#!/usr/bin/env python3
"""Generate the molecule CI job matrix.

Modes:
  --changed FILE   PR mode. FILE lists changed paths (one per line). A change
                   under roles/<role>/ selects that role; a change to shared
                   test infrastructure selects the canary set. Both accumulate.
  --all            Every role with a molecule/ directory (weekly, dispatch).
  --roles "a b"    Explicit space-separated role list (workflow_dispatch input).

Writes GitHub Actions outputs to the file named by $GITHUB_OUTPUT (or stdout):
  matrix=<json>        {"include": [{"role": ..., "distro": ...}, ...]}
  any=<true|false>     whether the matrix has any jobs
  build_image=<true|false>  whether docker/ changed (PR must build its own image)
"""

import argparse
import json
import os
import sys

import yaml

DISTROS = ["bookworm", "trixie"]
CANARY = ["git", "mysql"]  # one trivial, one heavy service role
INFRA_PREFIXES = (
    ".config/molecule/",
    ".github/workflows/molecule.yml",
    "requirements-dev.txt",
    "requirements.yml",
    "scripts/molecule_matrix.py",
)
IMAGE_PREFIX = "docker/"
PLATFORMS_FILE = ".config/molecule/platforms.yml"


def has_scenario(role):
    return os.path.isdir(os.path.join("roles", role, "molecule"))


def all_roles():
    return sorted(r for r in os.listdir("roles") if has_scenario(r))


def restrictions():
    if not os.path.exists(PLATFORMS_FILE):
        return {}
    with open(PLATFORMS_FILE) as f:
        return yaml.safe_load(f) or {}


def roles_from_changes(paths):
    roles = set()
    infra = False
    image = False
    for p in paths:
        if p.startswith("roles/") and p.count("/") >= 2:
            roles.add(p.split("/", 2)[1])
        elif p.startswith(IMAGE_PREFIX):
            image = True
            infra = True
        elif p.startswith(INFRA_PREFIXES):
            infra = True
    roles = {r for r in roles if has_scenario(r)}
    if infra:
        roles.update(r for r in CANARY if has_scenario(r))
    return sorted(roles), image


def build_matrix(roles):
    limits = restrictions()
    return {
        "include": [
            {"role": r, "distro": d} for r in roles for d in limits.get(r, DISTROS)
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--changed", metavar="FILE")
    mode.add_argument("--all", action="store_true")
    parser.add_argument("--roles", default="")
    args = parser.parse_args()

    image = False
    if args.changed:
        with open(args.changed) as f:
            paths = [line.strip() for line in f if line.strip()]
        roles, image = roles_from_changes(paths)
    elif args.roles.strip():
        roles = sorted(r for r in args.roles.split() if has_scenario(r))
    else:
        roles = all_roles()

    matrix = build_matrix(roles)
    out_path = os.environ.get("GITHUB_OUTPUT")
    out = open(out_path, "a") if out_path else sys.stdout
    print(f"matrix={json.dumps(matrix)}", file=out)
    print(f"any={'true' if matrix['include'] else 'false'}", file=out)
    print(f"build_image={'true' if image else 'false'}", file=out)
    print(f"Selected roles: {' '.join(roles) or '(none)'}", file=sys.stderr)


if __name__ == "__main__":
    main()
