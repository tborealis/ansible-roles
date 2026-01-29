# php_fpm

Configures PHP-FPM with pools and custom settings.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `php_fpm_version` | `{{ php_version }}` | PHP version |
| `php_fpm_date_timezone` | `Europe/London` | Default timezone |
| `php_fpm_realpath_cache_size` | `16M` | Realpath cache size |
| `php_fpm_realpath_cache_ttl` | `120` | Realpath cache TTL |
| `php_fpm_memory_limit` | `64M` | Memory limit |
| `php_fpm_max_execution_time` | `30` | Maximum execution time |
| `php_fpm_error_reporting` | `E_ALL & ~E_DEPRECATED & ~E_STRICT` | Error reporting level |
| `php_fpm_display_errors` | `false` | Display errors |
| `php_fpm_display_startup_errors` | `false` | Display startup errors |
| `php_fpm_post_max_size` | `8M` | Maximum POST size |
| `php_fpm_upload_max_filesize` | `8M` | Maximum upload file size |
| `php_fpm_mysqlnd_collect_statistics` | `false` | Collect MySQLnd statistics |
| `php_fpm_opcache_memory_consumption` | `128` | OPcache memory (MB) |
| `php_fpm_opcache_max_accelerated_files` | `100000` | OPcache max files |
| `php_fpm_opcache_validate_timestamps` | `0` | Validate timestamps |
| `php_fpm_xdebug` | `false` | Enable Xdebug |
| `php_fpm_pools` | `[]` | FPM pool configurations |
| `php_fpm_packages` | `{{ php_packages }}` | PHP packages to install |
