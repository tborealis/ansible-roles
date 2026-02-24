# node

Installs Node.js from NodeSource repository.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `node_corepack_enable` | `false` | Set to `true` to enable all package managers, or a name (e.g. `yarn`) to enable one |
| `node_global_packages` | `[]` | Global npm packages to install |
| `node_npmrc` | `[]` | npmrc configuration entries |
