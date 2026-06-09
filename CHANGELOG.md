# Changelog

All notable changes to the `tborealis.roles` collection are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this collection adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Each entry is prefixed with the affected role, e.g. `**nginx:**`. Changes that affect
the whole repository (CI, docs, tooling) use the `**meta:**` scope. Breaking changes are
flagged with **BREAKING** and require a MAJOR version bump.

## [Unreleased]

### Added

- **pgsql:** add `postgres_schemas` variable to create schemas, and
  `schema`/`target_roles` keys in `postgres_privs` for schema-scoped and
  default-privilege grants

## [1.0.0] - 2026-06-11

### Added

- Initial release of the `tborealis.roles` collection: roles for provisioning local and
  production Debian/Ubuntu environments.
- **meta:** SemVer release policy, `CHANGELOG.md`, tag-triggered GitHub Actions release
  workflow, and a per-PR changelog gate.
