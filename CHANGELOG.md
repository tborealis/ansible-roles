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
- **pgsql:** add `postgres_become_user` variable (default `postgres`) to configure the
  system user that database operations run as

### Changed

- **yarn:** update the bundled Yarn APT repository signing key
- **base, do_agent, mysql, new_relic, nginx, node, pgsql, pgsql_client,
  php_repo_sury, yarn:** stop using the deprecated `ansible.builtin.apt_repository` module
  (slated for removal in ansible-core 2.25). Repositories are now configured with
  `deb822_repository`, and these roles install the `python3-debian` package the
  new module requires. Stale `.list` files left by the old module are removed on the next
  run so apt no longer warns about duplicate sources.
- **chrome:** drop the deprecated `ansible.builtin.apt_repository` task that removed the
  Google Chrome repository during system-chrome cleanup.
- **rabbitmq:** replace the deprecated `ansible.builtin.apt_key` and `apt_repository` with
  a `/usr/share/keyrings` key and a `signed-by` `deb822_repository`.
- **tasks:** replace the deprecated `ansible.builtin.apt_key` in the shared `add-key`
  helper with a copy into `/etc/apt/trusted.gpg.d` (the `key_path` interface is unchanged).
- **mysql:** **BREAKING** switch from the deprecated `community.mysql` collection to the
  renamed `ansible.mysql` collection. Consumers of `tborealis.roles` must now install the
  `ansible.mysql` collection.

### Fixed

- **php_cli, php_fpm:** accept an unquoted YAML version (e.g. `php_version: 8.1`
  parsed as a float) in the supported-version check by coercing to a string before
  comparison

## [1.0.0] - 2026-06-11

### Added

- Initial release of the `tborealis.roles` collection: roles for provisioning local and
  production Debian/Ubuntu environments.
- **meta:** SemVer release policy, `CHANGELOG.md`, tag-triggered GitHub Actions release
  workflow, and a per-PR changelog gate.
