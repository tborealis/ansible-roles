# apt_keys

Installs the apt repository signing keys for every role in this collection that uses a
third-party apt repository. Keys are written to `/etc/apt/keyrings/` (Debian's location
for locally/config-managed keyrings) **before** any `apt-get update` runs, so a stale
key left on a re-provisioned host is overwritten before it can break the cache update.

Each repo role (and `base`) declares this role as a meta dependency, so the keyrings are
always in place first. The role only copies files — it performs no apt or network
operations — which is what makes it safe to run ahead of the first cache update.

The keyrings and their metadata live in a single manifest, `apt_keys_keyrings`
(`defaults/main.yml`). That same manifest drives the scheduled key-expiry monitor
(`scripts/check_apt_keys.py`), so a key added here is automatically monitored.

## Adding a key for a new role

1. Drop the keyring file in this role's `files/` directory.
2. Add one entry to `apt_keys_keyrings` (`name`, `src`, `dest`, `url`, and `repo`
   coordinates for the live verifier).
3. Point the new role's `deb822_repository` at `signed_by: {{ entry.dest }}` and add
   `apt_keys` to its `meta/main.yml` dependencies.

No CI changes are needed — the monitor discovers it from the manifest.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `apt_keys_keyrings` | see `defaults/main.yml` | List of managed keyrings. Each item has `name`, `src` (filename under `files/`), `dest` (absolute keyring path), `url` (upstream key, for manual refresh), and `repo` (`uris`/`suites`/`components`, used only by the live verifier; `{release}` is substituted with the target Debian release). |
