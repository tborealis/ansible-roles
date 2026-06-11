# AI Agent Guidelines for ansible-roles

## Project Overview

This is an Ansible Galaxy collection (`tborealis.roles`) containing reusable roles for Debian/Ubuntu server configuration.

## Commands

- **Lint**: `make lint` (runs ansible-lint in a Docker container with the version pinned in `requirements-dev.txt`)
- **Test**: No automated tests currently

## Code Style

### Variable Naming

Variables defined in roles must use the role name as a prefix:
- `base_system_packages` (not `system_packages`)
- `nginx_worker_processes` (not `worker_processes`)
- `chrome_chromedriver_version` (not `chromedriver_version`)
There are existing roles that break this convention. They will be refactored.

### Task Naming

- Jinja templates go at the end of task names: `Install packages for {{ item.name }}`
- Use FQCNs for modules: `ansible.builtin.apt`, `community.general.locale_gen`

### Ansible-lint Rules

The project uses the `shared` profile. Key rules enforced:
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

## Documentation

Role READMEs should include:
- Brief description
- Requirements (if any)
- Variables table with Name, Default, and Description columns
- No example playbook sections

## Versioning & releases

The collection follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **MAJOR** — breaking changes: removing/renaming role variables, changing default
  behaviour downstream playbooks rely on, renaming task names depended on, or raising
  the required Ansible/OS versions.
- **MINOR** — new roles, new variables, or new optional behaviour (backwards
  compatible).
- **PATCH** — bug fixes, lint fixes, or dependency bumps with no role behaviour change.

`galaxy.yml`'s `version:` is bumped only when cutting a release (see below), and CI
enforces that a pushed `vX.Y.Z` tag matches it.

### Changelog

All changes are recorded in `CHANGELOG.md`, which follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The top section is always
`## [Unreleased]`; released versions appear below as `## [X.Y.Z] - YYYY-MM-DD`.

Format rules:

- Group entries under `### Added`, `### Changed`, `### Deprecated`, `### Removed`,
  `### Fixed`, or `### Security`.
- Prefix every entry with the affected role in bold, e.g. `- **nginx:** ...`. For
  repo-wide changes (CI, docs, tooling) use `- **meta:** ...`.
- Flag breaking changes with **BREAKING** in the entry.

Example:

```markdown
## [Unreleased]

### Added
- **php_cli:** add PHP 8.5 support

### Removed
- **base:** drop `base_legacy_packages`
  **BREAKING** — downstream playbooks referencing it must be updated
```

### Maintaining the changelog (instructions for Claude)

Treat the changelog as part of every code change:

1. With each change that affects collection behaviour, add a line under
   `## [Unreleased]` in the correct category, prefixed with the affected role
   (`**meta:**` for repo-wide changes).
2. Assess whether the change is **breaking** per the MAJOR rules above. If it is,
   add **BREAKING** to the entry, explain the downstream impact, and recommend a MAJOR
   version bump in the PR description so the maintainer picks the right version.
3. If a change genuinely warrants no changelog entry (pure CI/docs/tooling), apply the
   `skip-changelog` label to the PR instead.

CI blocks any PR that does not touch `CHANGELOG.md` unless it carries the
`skip-changelog` label.

### Cutting a release

1. `make release VERSION=vX.Y.Z` (wraps `scripts/cut-release.sh`) — bumps `galaxy.yml`
   and promotes `[Unreleased]` to `## [X.Y.Z] - <today>`. It does not commit, branch, or
   tag. (You can also do these two edits by hand.)
2. Commit on a release branch, open a PR, review, and merge to `main`:

       git switch -c release/vX.Y.Z
       git add galaxy.yml CHANGELOG.md
       git commit -m "Release vX.Y.Z"

3. After merge, tag `main` and push the tag:

       git tag vX.Y.Z && git push origin vX.Y.Z

4. `.github/workflows/release.yml` runs `verify-release` (tag matches `galaxy.yml` and a
   `## [X.Y.Z]` changelog section exists) and publishes a GitHub Release using that
   changelog section as the notes.

### Downstream consumers

This repository no longer triggers downstream builds (e.g. lampsible). Rebuilding or
pinning a consumer against a release is a manual step performed from that consumer's
own repository.
