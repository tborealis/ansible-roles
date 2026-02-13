# supervisor

Installs and configures Supervisor process manager.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `supervisor_configs` | `[]` | Supervisor program configurations |
| `supervisor_crashmail_enable` | `false` | Enable crash email notifications |
| `supervisor_users` | `[]` | Users allowed to control Supervisor |
| `supervisor_group` | `supervisor` | Supervisor group name |
