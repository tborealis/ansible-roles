# sudo

Configures sudo with additional sudoers files.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `sudo_additional_config` | `[]` | Additional sudoers configuration files |

## Templates

The `src` of each `sudo_additional_config` entry is resolved relative to the
consuming playbook, so the sudoers templates must live next to it in
`templates/sudo/`. See this role's molecule scenario
(`molecule/default/templates/`) for a working example.
