# Migrating to v6.0.0

Every breaking change in v6.0.0, with what to do about it. Sections are
ordered roughly by blast radius; skip any role you don't apply.

## PHP: `php_repo_sury`, `php_cli`, `php_fpm`, `composer` and `new_relic` → `php`

v6.0.0 replaces `php_repo_sury`, `php_cli`, `php_fpm`, `composer` and
`new_relic` with the single [`php`](../roles/php/README.md) role. This section
maps the old roles and variables onto the new one and explains what happens
the first time the new role converges an existing host.

### Playbook changes

Replace the old role list with one entry:

```yaml
# before
roles:
  - role: tborealis.roles.php_repo_sury
  - role: tborealis.roles.php_cli
  - role: tborealis.roles.php_fpm
  - role: tborealis.roles.composer
  - role: tborealis.roles.new_relic

# after
roles:
  - role: tborealis.roles.php
```

CLI is always installed. FPM and Composer default to on, New Relic to off:

```yaml
php_fpm: true        # set false where the old playbook skipped php_fpm
php_composer: true   # set false where the old playbook skipped composer
php_new_relic: true  # REQUIRED where the old playbook applied new_relic —
                     # the old role installed the agent unconditionally,
                     # the new switch defaults to false
```

### Variable mapping

| Old | New |
|-----|-----|
| `php_version` / `php_cli_version` / `php_fpm_version` / `composer_php_version` | `php_version` (single, required, 8.1–8.5) |
| `php_cli_supported_versions` / `php_fpm_supported_versions` | removed (fixed list in the role's `vars/main.yml`) |
| `php_packages` / `php_cli_packages` / `php_fpm_packages` | `php_extensions`, names without the `phpX.Y-` prefix (`php8.3-curl` → `curl`); extensions now follow `php_version` automatically |
| `php_cli_date_timezone` / `php_fpm_date_timezone` | `php_date_timezone` |
| `php_cli_error_reporting` / `php_fpm_error_reporting` | `php_error_reporting` |
| `php_cli_display_errors` / `php_fpm_display_errors` | `php_display_errors` |
| `php_cli_display_startup_errors` / `php_fpm_display_startup_errors` | `php_display_startup_errors` |
| `php_cli_mysqlnd_collect_statistics` / `php_fpm_mysqlnd_collect_statistics` | `php_mysqlnd_collect_statistics` |
| `php_cli_error_log` | `php_cli_error_log` (unchanged) |
| `php_fpm_memory_limit`, `php_fpm_max_execution_time`, `php_fpm_post_max_size`, `php_fpm_upload_max_filesize`, `php_fpm_realpath_cache_size`, `php_fpm_realpath_cache_ttl`, `php_fpm_zend_assertions`, `php_fpm_opcache_memory_consumption`, `php_fpm_opcache_max_accelerated_files`, `php_fpm_opcache_validate_timestamps`, `php_fpm_opcache_revalidate_freq`, `php_fpm_pools` | unchanged |
| `php_fpm_zend_ignore_args` | `php_fpm_zend_exception_ignore_args` |
| `php_fpm_opcache_file_cache` / `php_fpm_opcache_file_cache_only` | `php_fpm_opcache_file_cache_dir` (the role now creates the directory, `0700`, owned by `php_fpm_opcache_file_cache_user`) |
| `php_xdebug_client_host` / `php_cli_xdebug_client_host` / `php_fpm_xdebug_client_host` | `php_xdebug_client_host` |
| `php_cli_xdebug_max_nesting_level` / `php_fpm_xdebug_max_nesting_level` | `php_xdebug_max_nesting_level` |
| `php_*_xdebug_remote_enable` / `_remote_host` / `_remote_autostart` | removed (Xdebug 2 leftovers, unused since PHP 8) |
| `php_cli_xdebug`, `php_fpm_xdebug`, `php_cli_xdebug_idekey`, `php_fpm_xdebug_idekey`, `php_fpm_xdebug_start_with_request`, `php_xdebug_control_script_*` | unchanged |
| `composer_keep_updated` | `php_composer_keep_updated` |
| `composer_global_packages` | `php_composer_global_packages` |
| `newrelic_key` | `php_newrelic_key` |
| `newrelic_appname` | `php_newrelic_appname` |
| `newrelic_browser_auto_instrument` | `php_newrelic_browser_auto_instrument` |
| `newrelic_distributed_tracing_enabled` | `php_newrelic_distributed_tracing_enabled` |
| `newrelic_enable` | removed (was never used) |

New in 6.0.0 (see the [role README](../roles/php/README.md)):
`php_remove_other_versions`, `php_fpm_session_save_path`,
`php_fpm_session_use_strict_mode`, `php_fpm_session_cookie_httponly`,
per-pool `session_save_path`/`user`, `php_fpm_expose_php`,
`php_fpm_opcache_preload`/`_preload_user`,
`php_fpm_opcache_interned_strings_buffer`, `php_fpm_opcache_jit_buffer_size`,
`php_cli_extra_ini`/`php_fpm_extra_ini`.

### Behavioural changes

- **PHP 7.4 and 8.0 are no longer supported.** Upgrade to 8.1+ first (with the
  old roles) or in the same converge (the new role removes the old version).
- **`php.ini` and `php-fpm.conf` are no longer templated.** The packaged
  files stay as upstream ships them; managed settings live in
  `conf.d/99-ansible.ini`. Anything you previously changed by editing the old
  roles' templates needs an entry in `php_cli_extra_ini`/`php_fpm_extra_ini`.
  FPM's `log_level` reverts from the old template's `warning` to stock
  `notice` (it lives in `php-fpm.conf`, not php.ini).
- **Sessions move from `/tmp` to `/var/lib/php/sessions`.** The old templates
  left `session.save_path` unset, so sessions fell back to `/tmp` — shared
  between pools, not covered by Debian's `sessionclean` timer, wiped by tmp
  cleaners. Active sessions are logged out once on migration. Session
  hardening is also enabled by default (`session.use_strict_mode`,
  `session.cookie_httponly`); set the `php_fpm_session_*` variables to opt
  out.
- **New Relic is off by default.** The old role installed the agent whenever
  applied; set `php_new_relic: true` to keep it. Setting it back to `false`
  later does not uninstall the agent (`apt purge newrelic-php5` does).
- **`php_repo_sury`'s `remove-php.yml` task file is gone**, replaced by
  `php_remove_other_versions: true` (the default).
- The FPM service is now explicitly started and enabled when pools exist (the
  old role only restarted it on config changes).

### First converge on an existing host

- **Changing the version at the same time** (e.g. `php_version: "8.3"` →
  `"8.5"`): the new version is installed and configured, then every other
  installed version is stopped, purged and its `/etc/php/<version>` removed.
  Nothing of the old roles' config survives. This is the cleanest path.
- **Keeping the current version**: the role detects the old roles' marker in
  `php.ini` (`; Ansible managed`) and restores the packaged reference config
  once, then applies the drop-in. Settings the old roles managed are carried
  by the drop-in; diff your expectations against the variables table if you
  had customised the old templates. The old roles' templated `php-fpm.conf`
  is left in place — it is functionally equivalent to stock and no packaged
  reference copy exists to restore from. If a host was built some other way
  and the marker check cannot fire, restore stock manually before relying on
  the drop-in:

  ```sh
  apt-get install --reinstall -o Dpkg::Options::=--force-confmiss php8.3-fpm php8.3-cli
  ```

Roles that only need a PHP CLI (e.g. hosts running `phpbu`) can use:

```yaml
- role: tborealis.roles.php
  vars:
    php_version: "8.3"
    php_fpm: false
    php_composer: false
```

## mailhog → mailpit

The `mailhog` role is removed; use [`mailpit`](../roles/mailpit/README.md)
instead. Mailpit is the maintained MailHog successor and binds the same
default ports (SMTP 1025, web UI/API 8025), so client configuration is
unchanged.

Converging `mailpit` on a host previously managed by the `mailhog` role
removes the legacy install first (stock paths:
`/lib/systemd/system/mailhog.service`, `/opt/mailhog`, the `mailhog` user),
since both bind the same ports.

## aws_cli: first-party install replaces the ecgalaxy wrapper

The role no longer wraps `ecgalaxy.aws_cli` (whose GPG verification silently
passed on a key that expired in 2023); it downloads, verifies and installs the
AWS CLI itself.

- Remove `ecgalaxy.aws_cli` from your `requirements.yml` if you carried it
  there; it is gone from the collection's.
- Any external `awscli_*` variables you set for the wrapped role are replaced
  by the `aws_cli_*` variables documented in the
  [role README](../roles/aws_cli/README.md) (`aws_cli_version`,
  `aws_cli_download_path`, `aws_cli_ssm_install`, `aws_cli_ssm_version`,
  `aws_cli_ssm_checksums`). `aws_cli_config` is unchanged.
- The CLI and Session Manager plugin versions are now pinned; arm64 is
  supported.

## apache2: dead variables removed

`apache2_load_modules` and `apache2_conf` are removed. They were declared and
documented but used by no task, so nothing you configured through them ever
took effect — delete them from inventories. Use `apache2_modules` to enable
modules.

`/etc/apache2/envvars` now renders `APACHE_RUN_USER`/`APACHE_RUN_GROUP` from
`apache2_user` (previously hardcoded `www-data`; the default is unchanged),
and changes to it restart Apache.

## base: dead `ssh_extra_conf_files` removed

`ssh_extra_conf_files` was referenced by no task; nothing you configured
through it ever took effect. Delete it from inventories. The unreachable
`fix-prompt.yml` task file is also gone (the skel-level prompt task in
`main.yml` is the live implementation).
