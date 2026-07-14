# Releasing

The canonical release and changelog policy for the `tborealis.roles` collection.

## Semantic Versioning

The collection follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **MAJOR** — breaking changes: removing/renaming role variables, changing default
  behaviour downstream playbooks rely on, renaming task names depended on, or raising
  the required Ansible/OS versions.
- **MINOR** — new roles, new variables, or new optional behaviour (backwards
  compatible).
- **PATCH** — bug fixes, lint fixes, or dependency bumps with no role behaviour change.

`galaxy.yml`'s `version:` is bumped only when cutting a release, and CI enforces that a
pushed `vX.Y.Z` tag matches it.

## Changelog

All changes are recorded in [`CHANGELOG.md`](../CHANGELOG.md), which follows
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
- **php:** add PHP 8.5 support

### Removed
- **base:** drop `base_legacy_packages`
  **BREAKING** — downstream playbooks referencing it must be updated
```

Every change that affects collection behaviour must add an entry under
`## [Unreleased]`. CI blocks any PR that does not touch `CHANGELOG.md` unless it carries
the `skip-changelog` label — use that for pure CI/docs/tooling changes (it is applied to
Dependabot PRs automatically).

## Cutting a release

1. `make release VERSION=vX.Y.Z` (wraps `scripts/cut-release.sh`) — bumps `galaxy.yml`
   and promotes `[Unreleased]` to `## [X.Y.Z] - <today>`. It does not commit, branch, or
   tag. (You can also make these two edits by hand.)
2. Commit on a release branch, open a PR, review, and merge to `main`:

       git switch -c release/vX.Y.Z
       git add galaxy.yml CHANGELOG.md
       git commit -m "Release vX.Y.Z"

3. After merge, tag `main` and push the tag:

       git tag vX.Y.Z && git push origin vX.Y.Z

4. `.github/workflows/release.yml` runs `verify-release` (the tag matches `galaxy.yml`
   and a `## [X.Y.Z]` changelog section exists) and publishes a GitHub Release using that
   changelog section as the notes.

## Downstream consumers

This repository does not trigger downstream builds (e.g. lampsible). Rebuilding or
pinning a consumer against a release is a manual step performed from that consumer's own
repository.
