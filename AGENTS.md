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
