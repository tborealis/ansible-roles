# php_repo_sury

Adds the Sury PHP repository and installs PHP packages.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `php_cli_xdebug` | `false` | Enable Xdebug for CLI |
| `php_fpm_xdebug` | `false` | Enable Xdebug for FPM |
| `php_xdebug_control_script_enable` | `xdebug-enable.j2` | Xdebug enable script template |
| `php_xdebug_control_script_disable` | `xdebug-disable.j2` | Xdebug disable script template |
