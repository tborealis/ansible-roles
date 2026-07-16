# php

Installs and configures a complete PHP stack from the
[Sury repository](https://packages.sury.org/php/): CLI (always), PHP-FPM,
Composer and the New Relic PHP agent, each behind a feature switch.
Replaces the removed `php_repo_sury`, `php_cli`, `php_fpm`, `composer` and
`new_relic` roles — see [docs/migrating-v6.md](../../docs/migrating-v6.md).

The stock `php.ini` is never modified: all managed settings live in
`/etc/php/<version>/{cli,fpm}/conf.d/99-ansible.ini`, which is parsed last and
therefore wins, while upstream config changes flow through package upgrades
untouched. Turning a feature switch off means the feature is not managed, not
that it is uninstalled.

When `php_version` changes, previously installed PHP versions are stopped,
purged and their `/etc/php/<version>` directories removed (disable with
`php_remove_other_versions: false` — but note `/usr/bin/php` alternatives are
not pinned, so with several versions installed `php` may not point at
`php_version`). Hosts that were converged by the removed `php_cli`/`php_fpm`
roles at the same version get the packaged `php.ini`/`php-fpm.conf` restored
once, detected via the old templates' Ansible-managed marker.

## FPM pools

Pool config is supplied by the consuming playbook: each `php_fpm_pools` item
names a template at `templates/fpm/pools/<src>` relative to the playbook,
installed to `pool.d/<dest>`. The packaged default pool (`www.conf`) is
removed, and with no pools the FPM service is stopped and disabled. An item
may also set `session_save_path` and `user`: the role creates that directory
(mode `0700`, owned by `user`) and the pool template can point PHP at it —
the item is in scope during templating:

```ini
php_admin_value[session.save_path] = {{ item.session_save_path }}
```

Keep per-pool session directories under `/var/lib/php/sessions/` or enable
pool-level garbage collection (`php_admin_value[session.gc_probability]`) —
Debian's `sessionclean` timer does not see pool-level save paths.

## Xdebug

The xdebug package is installed when either switch is on, but the module is
left disabled; `/usr/local/bin/xdebug-enable` and `xdebug-disable` toggle it
at runtime. Re-running the role disables it again.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `php_version` | — (required) | PHP version to install; must be one the role supports (8.1–8.5) |
| `php_fpm` | `true` | Install and manage PHP-FPM |
| `php_composer` | `true` | Install Composer |
| `php_new_relic` | `false` | Install the New Relic PHP agent |
| `php_remove_other_versions` | `true` | Stop, purge and remove config of other installed PHP versions |
| `php_extensions` | `[]` | Extension names (e.g. `[curl, mbstring]`), installed as `php<version>-<name>` |
| `php_date_timezone` | `Europe/London` | `date.timezone` for both SAPIs |
| `php_error_reporting` | `E_ALL & ~E_DEPRECATED` | `error_reporting` for both SAPIs |
| `php_display_errors` | `false` | `display_errors` for both SAPIs |
| `php_display_startup_errors` | `false` | `display_startup_errors` for both SAPIs |
| `php_mysqlnd_collect_statistics` | `false` | `mysqlnd.collect_statistics` for both SAPIs |
| `php_cli_error_log` | `syslog` | CLI `error_log` |
| `php_cli_extra_ini` | `{}` | Extra CLI ini directives, rendered verbatim into the drop-in |
| `php_fpm_expose_php` | `false` | `expose_php` (FPM) |
| `php_fpm_memory_limit` | `64M` | `memory_limit` (FPM) |
| `php_fpm_max_execution_time` | `30` | `max_execution_time` (FPM) |
| `php_fpm_post_max_size` | `8M` | `post_max_size` (FPM) |
| `php_fpm_upload_max_filesize` | `8M` | `upload_max_filesize` (FPM) |
| `php_fpm_realpath_cache_size` | `16M` | `realpath_cache_size` (FPM) |
| `php_fpm_realpath_cache_ttl` | `120` | `realpath_cache_ttl` (FPM) |
| `php_fpm_zend_exception_ignore_args` | `true` | `zend.exception_ignore_args` (FPM) |
| `php_fpm_zend_assertions` | `-1` | `zend.assertions` (FPM) |
| `php_fpm_opcache_memory_consumption` | `128` | `opcache.memory_consumption` (FPM) |
| `php_fpm_opcache_max_accelerated_files` | `100000` | `opcache.max_accelerated_files` (FPM) |
| `php_fpm_opcache_validate_timestamps` | `0` | `opcache.validate_timestamps` (FPM); 0 needs an FPM restart on deploys |
| `php_fpm_opcache_revalidate_freq` | `0` | `opcache.revalidate_freq` (FPM) |
| `php_fpm_extra_ini` | `{}` | Extra FPM ini directives, rendered verbatim into the drop-in |
| `php_fpm_session_save_path` | `/var/lib/php/sessions` | `session.save_path`; the Debian default dir (sticky, cleaned by the `sessionclean` timer) instead of PHP's `/tmp` fallback |
| `php_fpm_session_use_strict_mode` | `true` | `session.use_strict_mode` (session-fixation hardening) |
| `php_fpm_session_cookie_httponly` | `true` | `session.cookie_httponly` |
| `php_fpm_opcache_preload` | `""` | `opcache.preload` script path (e.g. a Symfony `config/preload.php`); empty disables preloading |
| `php_fpm_opcache_preload_user` | `www-data` | `opcache.preload_user`, rendered with `opcache.preload` |
| `php_fpm_opcache_interned_strings_buffer` | `16` | `opcache.interned_strings_buffer` (stock: 8) |
| `php_fpm_opcache_jit_buffer_size` | `0` | `opcache.jit_buffer_size`; a size (e.g. `100M`) enables the tracing JIT |
| `php_fpm_opcache_file_cache_dir` | `""` | `opcache.file_cache` directory, created `0700`; empty disables the second-level cache |
| `php_fpm_opcache_file_cache_user` | `www-data` | Owner of the opcache file cache directory |
| `php_fpm_pools` | `[]` | Pool definitions (keys: `src`, `dest`, optional `session_save_path`, `user`) — see above |
| `php_cli_xdebug` | `false` | Install xdebug for the CLI and render its settings into the CLI drop-in |
| `php_fpm_xdebug` | `false` | Install xdebug for FPM and render its settings into the FPM drop-in |
| `php_xdebug_client_host` | `""` | `xdebug.client_host` for both SAPIs |
| `php_xdebug_mode` | `debug,develop` | `xdebug.mode` for both SAPIs |
| `php_xdebug_max_nesting_level` | `500` | `xdebug.max_nesting_level` for both SAPIs |
| `php_cli_xdebug_idekey` | `cli` | CLI `xdebug.idekey` |
| `php_fpm_xdebug_idekey` | `fpm` | FPM `xdebug.idekey` |
| `php_fpm_xdebug_start_with_request` | `yes` | FPM `xdebug.start_with_request` (CLI is always `trigger`) |
| `php_xdebug_control_script_enable` | `xdebug-enable.j2` | Template for `/usr/local/bin/xdebug-enable` |
| `php_xdebug_control_script_disable` | `xdebug-disable.j2` | Template for `/usr/local/bin/xdebug-disable` |
| `php_composer_keep_updated` | `true` | Run `composer self-update` on each converge |
| `php_composer_global_packages` | `[]` | Global Composer packages (keys: `name`, `version`) |
| `php_newrelic_key` | — (required when `php_new_relic`) | New Relic licence key |
| `php_newrelic_appname` | — (required when `php_new_relic`) | New Relic application name |
| `php_newrelic_browser_auto_instrument` | `false` | `newrelic.browser_monitoring.auto_instrument` |
| `php_newrelic_distributed_tracing_enabled` | `true` | `newrelic.distributed_tracing_enabled` |
