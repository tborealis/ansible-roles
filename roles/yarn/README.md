# yarn

Installs Yarn package manager.

## Requirements

The Yarn 1.x deb depends on `nodejs`, and apt satisfies that with **Debian's
distro Node.js** if none is installed yet. To run Yarn against the NodeSource
build the [`node`](../node) role provides, order `node` **before** `yarn` in
the playbook; a playbook that applies `yarn` first silently gets the distro
Node.js.

## Role Variables

None.
