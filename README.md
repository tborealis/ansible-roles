# Ansible Collection - tborealis.roles

Ansible Galaxy collection of roles for provisioning development and production environments.
Requires **Ansible 2.15** or newer.

## Installation

Install the latest version directly from GitHub:

```shell
ansible-galaxy collection install git+https://github.com/TomAdam/ansible-roles.git
```

## Usage

Reference the roles using the collection namespace:

```yaml
- hosts: all
  roles:
    - role: tborealis.roles.base
```

## Development

Run `make lint` to check the collection with Docker:

```shell
make lint
```
The Makefile uses the `cytopia/ansible-lint` image.
If Docker is unavailable, install `ansible-lint` locally and run it directly:

```shell
pip install ansible-lint
ansible-lint
```

See `galaxy.yml` for collection metadata and dependencies.
