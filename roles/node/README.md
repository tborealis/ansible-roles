# node

Installs a single system Node.js from the NodeSource repository, plus npm-based
package managers (Yarn classic, pnpm) and global packages, all version-pinned.

This role absorbed the removed `yarn` role — see
[docs/migrating-v6.md](../../docs/migrating-v6.md).

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `node_version` | — | **Required.** Major Node.js version to install (e.g. `22`). Switching majors removes the old NodeSource repo and upgrades in place |
| `node_npm_version` | `""` | Optional exact version to pin the bundled npm itself; empty leaves the bundled npm alone |
| `node_yarn_enabled` | `false` | Install Yarn classic globally via npm |
| `node_yarn_version` | `"1.22.22"` | Exact Yarn classic version |
| `node_pnpm_enabled` | `false` | Install pnpm globally via npm |
| `node_pnpm_version` | `"11.13.1"` | Exact pnpm version |
| `node_global_packages` | `[]` | Global npm packages to install (`name` or `name@version`) |
| `node_npmrc` | `[]` | npmrc entries; each item is `{template, dir, user}` |

Pin exact package-manager versions: `community.general.npm` reinstalls on every
run when given a range or dist-tag. Disabling a manager does not uninstall it.

## Corepack is not used

Corepack support was removed in v6. The Node.js TSC voted in March 2025 to stop
distributing corepack; Node 25+ no longer bundles it, and it downloads
package-manager binaries from the registry at run time. Package managers are
installed explicitly with pinned versions instead, and stale corepack shims
(`yarn`/`pnpm` symlinks into corepack's dist) are removed on converge.

## Yarn berry

`node_yarn_enabled` installs Yarn classic (1.x), which is also the launcher for
Yarn berry (2+) projects: berry lives per-project via `.yarnrc.yml`'s
`yarnPath` / a committed `.yarn/releases`, so there is nothing to install
globally.

## .npmrc contract

`node_npmrc` templates are playbook-relative: an item
`{template: npmrc.j2, dir: /home/deploy, user: deploy}` renders
`templates/node/npmrc.j2` from the playbook directory to
`/home/deploy/.npmrc` (mode `0600`).
