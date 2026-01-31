# php_cli

Configures PHP CLI with custom settings.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `php_cli_version` | `{{ php_version }}` | PHP version |
| `php_cli_date_timezone` | `Europe/London` | Default timezone |
| `php_cli_error_reporting` | `E_ALL & ~E_DEPRECATED & ~E_STRICT` | Error reporting level |
| `php_cli_display_errors` | `false` | Display errors |
| `php_cli_display_startup_errors` | `false` | Display startup errors |
| `php_cli_error_log` | `syslog` | Error log destination |
| `php_cli_mysqlnd_collect_statistics` | `false` | Collect MySQLnd statistics |
| `php_cli_xdebug` | `false` | Enable Xdebug |
| `php_cli_xdebug_remote_enable` | `true` | Enable Xdebug remote debugging |
| `php_cli_xdebug_remote_host` | `{{ php_cli_xdebug_client_host }}` | Xdebug remote host (legacy) |
| `php_cli_xdebug_remote_autostart` | `true` | Xdebug remote autostart (legacy) |
| `php_cli_xdebug_client_host` | `{{ php_xdebug_client_host }}` | Xdebug client host |
| `php_cli_xdebug_idekey` | `cli` | Xdebug IDE key |
| `php_cli_xdebug_max_nesting_level` | `500` | Maximum nesting level |
| `php_cli_packages` | `{{ php_packages }}` | PHP packages to install |
