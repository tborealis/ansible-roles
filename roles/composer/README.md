# composer

Installs PHP Composer and optionally global packages.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `composer_global_packages` | `[]` | Global Composer packages to install |
| `composer_php_version` | `{{ php_cli_version }}` | PHP version to use |
| `composer_keep_updated` | `true` | Keep Composer updated to latest version |
