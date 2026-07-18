# AI Agent Guidelines for ansible-roles

## Project Overview

This is an Ansible Galaxy collection (`tborealis.roles`) containing reusable roles for Debian/Ubuntu server configuration.

## Commands

- **Lint**: `make lint` (runs ansible-lint in a Docker container with the version pinned in `requirements-dev.txt`)
- **Test**: `make test ROLE=<name> [DISTRO=bookworm|trixie]` (Molecule with the Docker driver; see [`docs/testing.md`](docs/testing.md))

## Code Style

### Variable Naming

Variables defined in roles must use the role name as a prefix:
- `base_system_packages` (not `system_packages`)
- `nginx_worker_processes` (not `worker_processes`)
- `chrome_chromedriver_version` (not `chromedriver_version`)

### Task Naming

- Jinja templates go at the end of task names: `Install packages for {{ item.name }}`
- Use FQCNs for modules: `ansible.builtin.apt`, `community.general.locale_gen`

### Ansible-lint Rules

The project uses the `production` profile. Key rules enforced:
- `partial-become`: Tasks with `become_user` must also have `become: true`
- `risky-shell-pipe`: Shell commands with pipes need `set -o pipefail`
- `no-handler`: Avoid `when: result is changed` patterns
- `command-instead-of-module`: Use modules instead of raw commands where possible

## Role Structure

Each role follows standard Ansible structure:
```
roles/example/
├── defaults/main.yml    # Default variables (use role_ prefix)
├── tasks/main.yml       # Main tasks
├── handlers/main.yml    # Handlers (if needed)
├── templates/           # Jinja2 templates
└── README.md            # Role documentation with variable table
```

## Apt repository keys

Roles that add a third-party apt repository must **not** ship or copy their own signing
key. All keys are managed centrally by the `apt_keys` role, which installs them to
`/etc/apt/keyrings/` before any `apt-get update` (including `base`'s). When adding a repo
to a new role:

1. Drop the keyring file in `roles/apt_keys/files/`.
2. Add one entry to `apt_keys_keyrings` in `roles/apt_keys/defaults/main.yml` (`name`,
   `src`, `dest`, upstream `url`, and the `repo` coordinates used by the live verifier).
3. Point the role's `deb822_repository` at `signed_by: <dest>` and add `apt_keys` to the
   role's `meta/main.yml` dependencies (`- role: apt_keys`).

The scheduled `key-check` workflow discovers keys from this manifest automatically — no
CI changes are needed — and a drift check fails the build if a keyring file is added
without a manifest entry (or vice versa). The live verification runs against each
supported Debian release (bookworm and trixie) in its own container, because whether a
signature is accepted depends on that release's apt. Slack alerts require a
`SLACK_WEBHOOK_URL` repository secret. Run `make check-keys` to run all checks locally.

## Testing

Every role must ship a Molecule scenario at `roles/<role>/molecule/default/`
(`molecule.yml`, `converge.yml`, `verify.yml`). Scenarios inherit the shared base
config at `.config/molecule/config.yml`; verification must be functional (real client
probes and config-content assertions), not just package/service existence checks.
Roles that no-op on default variables must be converged with realistic test values.
A role restricted to a subset of releases overrides `platforms:` in its own
`molecule.yml` **and** gets an entry in `.config/molecule/platforms.yml`. Scenario
files must pass `make lint`. Full guide: [`docs/testing.md`](docs/testing.md).

## Documentation

Role READMEs should include:
- Brief description
- Requirements (if any)
- Variables table with Name, Default, and Description columns
- No example playbook sections

## Versioning & releases

The collection uses [SemVer](https://semver.org/) and a Keep a Changelog
`CHANGELOG.md`. **The full policy lives in [`docs/releasing.md`](docs/releasing.md)** —
read it before cutting a release. The essentials for day-to-day work:

**Update the changelog on every change.** Add a line under `## [Unreleased]` in the
right category (`Added`/`Changed`/`Fixed`/`Removed`/`Deprecated`/`Security`), prefixed
with the affected role, e.g. `- **nginx:** ...` (use `- **meta:** ...` for CI, docs, or
tooling). Assess whether the change is **breaking** (removed/renamed variables, changed
default behaviour, renamed depended-on task names, raised Ansible/OS requirements); if
so, add **BREAKING** to the entry and recommend a MAJOR bump in the PR description. If no
entry is warranted (pure CI/docs), apply the `skip-changelog` label instead. CI blocks
PRs that don't touch `CHANGELOG.md` unless that label is set.

**Cut a release** with `make release VERSION=vX.Y.Z` (bumps `galaxy.yml` and promotes
`[Unreleased]` to a dated heading), commit on a `release/vX.Y.Z` branch, merge to
`main`, then `git tag vX.Y.Z && git push origin vX.Y.Z`. CI verifies the tag matches
`galaxy.yml`/`CHANGELOG.md` and publishes the GitHub Release.
