# phpbu

Database backups with [phpbu](https://phpbu.de).

## Requirements

PHP must already be installed (e.g. via the `php` role) — the role fails fast
if it is not. phpbu is a phar that needs `ext-dom` to parse its XML config, so
include `xml` in `php_extensions`. The role deliberately does not install PHP
itself, since the PHP version and configuration are site-specific.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `phpbu_enable` | `true` | Set to `false` to skip the role entirely |
| `phpbu_phar_url` | GitHub release 6.0.23 | URL of the phpbu phar |
| `phpbu_phar_checksum` | `sha256:eea90...` | Checksum the downloaded phar must match |
| `phpbu_schema_url` | GitHub tag 6.0.23 | URL of the phpbu XSD used to validate the config |
| `phpbu_cron_enable` | `true` | Install (or remove, when `false`) the backup cron entry |
| `phpbu_cron_time` | `["30", "2", "*", "*", "*"]` | Five cron fields (minute, hour, day, month, weekday); daily at 02:30 |
| `phpbu_log_dir` | `/var/log/phpbu` | Log directory |
| `phpbu_lib_dir` | `/var/lib/phpbu` | Install directory for the phar and schema |
| `phpbu_backup_dir` | `{{ phpbu_lib_dir }}/backups` | Where backups are written |
| `phpbu_private_key` | — | Optional base64-encoded ed25519 private key for the `phpbu` user (`base64 -w0 <key file>`) |

## Templates

The role templates the consumer-supplied config file `templates/phpbu/phpbu.xml`,
resolved relative to the consuming playbook, to `/etc/phpbu.xml` (validated
against the phpbu XSD). See this role's molecule scenario
(`molecule/default/templates/`) for a working example.

## Updating phpbu

Releases and checksums are published on
[GitHub](https://github.com/sebastianfeldmann/phpbu/releases); the
phar.phpbu.de/schema.phpbu.de mirrors are dead. Bump `phpbu_phar_url`,
`phpbu_phar_checksum`, and `phpbu_schema_url` together.

## TODO

- Build config from vars rather than templating
