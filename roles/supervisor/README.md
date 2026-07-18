# supervisor

Installs and configures Supervisor process manager.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `supervisor_configs` | `[]` | Supervisor program configurations |
| `supervisor_crashmail_enable` | `false` | Enable crash email notifications |
| `supervisor_users` | `[]` | Users allowed to control Supervisor |
| `supervisor_group` | `supervisor` | Supervisor group name |

The following variables have no defaults and are required when
`supervisor_crashmail_enable` is `true`:

| Variable | Description |
|----------|-------------|
| `supervisor_crashmail_to` | Recipient address for crash/fatal mails |
| `supervisor_crashmail_from` | Sender address |
| `supervisor_crashmail_subject` | Subject for crash mails |
| `supervisor_crashmail_subject_fatal` | Subject for fatal mails |
| `supervisor_crashmail_smtp_host` | SMTP host (TLS is always used) |
| `supervisor_crashmail_smtp_user` | SMTP username |
| `supervisor_crashmail_smtp_password` | SMTP password |
