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

## aws_cli + aws_config → aws

Both roles are removed, replaced by the single
[`aws`](../roles/aws/README.md) role. The CLI (plus Session Manager plugin
and bash completion) install is gated behind `aws_cli_install`, which
defaults to true — hosts that only applied `aws_config` set it to false and
keep getting per-user config without the CLI.

```yaml
# before
roles:
  - role: tborealis.roles.aws_cli      # CLI + config
  - role: tborealis.roles.aws_config   # config only, elsewhere

# after
roles:
  - role: tborealis.roles.aws
vars:
  aws_cli_install: false   # only where the old playbook applied aws_config alone
```

### Variable mapping

| Old | New |
|-----|-----|
| `aws_config` | unchanged (name and profile shape) |
| `aws_cli_config` (flat, single profile) | folded into `aws_config`'s multi-profile shape — see below |
| `aws_cli_version`, `aws_cli_download_path`, `aws_cli_ssm_install`, `aws_cli_ssm_version`, `aws_cli_ssm_checksums` | unchanged names; `aws_cli_ssm_install` now defaults to `false` |
| — | `aws_cli_install` (new, default `true`) |

Former `aws_cli_config` entries move `default_region` into a `default`
profile's `region`:

```yaml
# before (aws_cli_config)
aws_cli_config:
  - user: deploy
    default_region: eu-west-1
    access_key_id: ABCDE
    secret_access_key: EDCBA

# after (aws_config)
aws_config:
  - user: deploy
    profiles:
      - name: default
        region: eu-west-1
        access_key_id: ABCDE
        secret_access_key: EDCBA
```

### Behavioural changes

- **The Session Manager plugin is no longer installed by default.** Set
  `aws_cli_ssm_install: true` where hosts use it — the old `aws_cli` role
  installed it unconditionally. Flipping a host to `false` does not
  uninstall an already-installed plugin (`apt purge session-manager-plugin`
  does).
- **Profile keys are generalised.** Every profile key besides
  `access_key_id`/`secret_access_key` renders verbatim into `~/.aws/config`
  (`region`, `output`, `role_arn`, `source_profile`, `sso_*`, …); quote
  values YAML would type-cast (unquoted booleans render `True`/`False`).
- **Credentials entries are only written for profiles carrying keys**, and a
  profile must set both keys or neither (asserted). `~/.aws/credentials` is
  still always written — empty when no profile has keys — so removed keys
  are scrubbed on the next converge.
- Bash completion and the unzip/gnupg prerequisites are now installed only
  when the CLI is; acl only when `aws_config` is non-empty.

### From the ecgalaxy wrapper

Also in this release, the CLI install no longer wraps `ecgalaxy.aws_cli`
(whose GPG verification silently passed on a key that expired in 2023); the
role downloads, verifies and installs the AWS CLI itself.

- Remove `ecgalaxy.aws_cli` from your `requirements.yml` if you carried it
  there; it is gone from the collection's.
- Any external `awscli_*` variables you set for the wrapped role are replaced
  by the `aws_cli_*` variables documented in the
  [role README](../roles/aws/README.md).
- The CLI and Session Manager plugin versions are now pinned; arm64 is
  supported.

## pgsql + pgsql_client → pgsql

The `pgsql_client` role is removed; the [`pgsql`](../roles/pgsql/README.md)
role now handles both jobs via `pgsql_mode` (`server`, the default, or
`client`). All `postgres_*` variables are renamed to `pgsql_*`.

```yaml
# before
roles:
  - role: tborealis.roles.pgsql_client
vars:
  postgres_version: 15

# after
roles:
  - role: tborealis.roles.pgsql
vars:
  pgsql_mode: client
  pgsql_version: 15
```

### Variable mapping

| Old | New |
|-----|-----|
| `postgres_version` | `pgsql_version` |
| `postgres_default_packages` (pgsql: server+client packages; pgsql_client: client packages — same name, conflicting meanings) | split into `pgsql_server_packages` and `pgsql_client_packages` |
| `postgres_databases` | `pgsql_databases` |
| `postgres_users` | `pgsql_users` |
| `postgres_schemas` | `pgsql_schemas` |
| `postgres_privs` | `pgsql_privs` |
| `postgres_extensions` | `pgsql_extensions` |
| `postgres_become_user` | `pgsql_become_user` |
| `postgres_additional_packages` | `pgsql_additional_packages` |
| `postgres_shared_buffers` | `pgsql_shared_buffers` |
| `postgres_effective_cache_size` | `pgsql_effective_cache_size` |
| `postgres_max_connections` | `pgsql_max_connections` |
| `postgres_risky_fast` | `pgsql_risky_fast` |
| `postgres_full_page_writes` | `pgsql_full_page_writes` |
| `postgres_synchronous_commit` | `pgsql_synchronous_commit` |
| `postgres_fsync` | `pgsql_fsync` |
| `postgres_max_wal_size` | `pgsql_max_wal_size` |
| `postgres_locale` | `pgsql_locale` |

### Version support

Server mode now supports PostgreSQL **15–18** (16 is newly accepted; 12 and
13 are dropped). Hosts still on 12/13 must upgrade the cluster to 15+ before
converging v6 server mode — `pg_upgradecluster` with both majors installed
(use the pre-v6 role or manual packages), or dump/restore into a fresh 15+
cluster. Client mode still accepts any PGDG major.

### New tunables and changed defaults

The per-version config templates are unified; the template now also manages
`work_mem`, `maintenance_work_mem`, `random_page_cost`, `wal_compression`,
`timezone`/`log_timezone` (via `pgsql_timezone`, same Europe/London default)
and, on 18+, `io_method` — see the role README's Tuning section. Deliberate
default changes to review: memory baseline 2GB → 4GB
(`pgsql_shared_buffers` 512MB → 1GB, `pgsql_effective_cache_size` 1GB →
2GB — set the old values explicitly on 2GB hosts),
`pgsql_random_page_cost: 1.1` (SSD/NVMe; set 4.0 on spinning disks),
`pgsql_wal_compression: lz4` (safe on existing clusters; set `"off"` to keep
stock behaviour) and `pgsql_maintenance_work_mem: 256MB` (stock 64MB).

### Behavioural changes

- `pgsql_locale` no longer defaults to base's `system_default_locale`; it is
  a fixed `en_GB.UTF-8` (the same effective default). Set it explicitly if
  your hosts use another locale.
- The never-notified `Restart postgres` handler is gone (the role restarts
  inline on config changes, as before). Any cross-role `notify: Restart
  postgres` in your playbooks — which never worked reliably — must go.
- The unreachable `remove-postgres.yml` / `remove-postgres-client.yml` task
  files are deleted.

## dotenv + environment → env_file

Both roles are removed, replaced by the single
[`env_file`](../roles/env_file/README.md) role: one `env_file_list` variable
whose items render plain `NAME=value` files by default, or `export NAME=value`
profile scripts with the file-level `export: true` flag.

From `dotenv`:

```yaml
# before (dotenv)
dotenv_files:
  - dest: /opt/app/.env
    owner: app
    vars:
      app_env: production

# after (env_file)
env_file_list:
  - file: /opt/app/.env
    owner: app
    vars:
      APP_ENV: production
```

`dest:` becomes `file:`, and names now render verbatim — dotenv's automatic
upper-casing is gone, so upper-case them yourself. `owner` is required;
`group`/`mode` defaults (owner / `0644`) and the `# Ansible managed` header
are unchanged.

From `environment`:

```yaml
# before (environment)
environment_files:
  - file: /etc/profile.d/app.sh
    owner: root
    vars:
      - name: APP_ENV
        value: production
dotenv_files:
  - file: /opt/app/.env
    owner: app
    vars:
      - name: APP_ENV
        value: production

# after (env_file)
env_file_list:
  - file: /etc/profile.d/app.sh
    owner: root
    export: true
    vars:
      APP_ENV: production
  - file: /opt/app/.env
    owner: app
    vars:
      APP_ENV: production
```

Former `environment_files` items add `export: true`; the `vars` list of
`{name, value}` pairs becomes a plain mapping. Behavioural changes: rendered
files gain the `# Ansible managed` header (a one-time diff on the next
converge), `group` now defaults to the owner instead of the apt/umask
fallback, and `mode` now defaults to `0644` instead of being umask-dependent.
Files that previously ended up stricter than `0644` will be loosened unless
the item sets `mode` — set `mode: "0600"` explicitly on files carrying
secrets.

## node + nvm + yarn → node

The `nvm` and `yarn` roles are removed and their jobs absorbed by
[`node`](../roles/node/README.md), which also drops corepack support. Yarn
classic and pnpm are now installed globally via npm with pinned versions,
and extra Node versions come from a version manager selected with
`node_version_manager` (`n` or `nvm`).

```yaml
# before
roles:
  - role: tborealis.roles.node
  - role: tborealis.roles.yarn
  - role: tborealis.roles.nvm

# after
roles:
  - role: tborealis.roles.node
```

```yaml
# inventory / group_vars
node_version: 22
node_yarn_enabled: true          # where the yarn role was applied
node_version_manager: nvm        # where the nvm role was applied
```

| Old | New |
|-----|-----|
| `node_corepack_enable` | removed — see below |
| yarn role (no variables) | `node_yarn_enabled: true` (+ `node_yarn_version`) |
| `nvm_version` | `node_nvm_version` |
| `nvm_config` | `node_nvm_config` (+ `node_version_manager: nvm`) — same item shape, minus `corepack_enable` |
| per-version `corepack_enable` | removed — use `global_packages: [yarn@1.22.22]` |
| — | `node_npm_version` (optional npm self-pin) |
| — | `node_pnpm_enabled` / `node_pnpm_version` |

Behavioural changes:

- **Corepack is gone.** The Node.js TSC voted in March 2025 to stop
  distributing corepack, Node 25+ no longer bundles it, and it downloads
  package-manager binaries from the registry at run time. Package managers
  are now explicit, pinned npm installs. On the first converge the role
  removes stale corepack shims (`yarn`/`pnpm`/`yarnpkg`/`pnpx` symlinks into
  corepack's dist under `/usr/bin` or `/usr/local/bin`) — npm would otherwise
  refuse to install the real managers over them.
- **Yarn moves from apt to npm.** The dl.yarnpkg.com repo is frozen at
  1.22.x, and its deb's `nodejs` dependency silently installed Debian's
  distro Node when the roles were mis-ordered. The role now removes the apt
  `yarn` package, the repo file and the `/etc/apt/keyrings/yarn-repo.gpg`
  keyring on converge, then installs the pinned Yarn via npm (same
  `/usr/bin/yarn` path; Yarn berry projects keep working — classic is only
  the launcher for a committed `.yarnrc.yml` `yarnPath`).
- **Old NodeSource repos are cleaned up.** Switching `node_version` now also
  removes NodeSource repo files for other majors before adding the new one.
- **New: extra Node versions via tj/n.** `node_version_manager: n` caches
  additional versions machine-wide (`node_n_versions`), used explicitly via
  `n --offline run`/`n --offline exec`; the system Node stays the default.
  n and nvm are mutually exclusive.
- **nvm is no longer installed by `curl | bash`.** Each user's `~/.nvm` is a
  git clone of nvm-sh/nvm at the pinned `node_nvm_version` tag, and the init
  lines in `~/.bashrc` are now a role-managed block. A `~/.nvm` originally
  installed as a tarball (host without git at install time) is re-cloned;
  declared versions reinstall in the same converge. Init lines the old
  installer appended are left in place — sourcing nvm.sh twice is harmless.

First converge on an existing host: corepack-shimmed or apt-installed Yarn is
replaced by the npm install in a single converge (there is a brief gap
mid-converge where no `yarn` binary exists). Anything pinned through corepack
(`packageManager` fields relying on shims) must move to the explicit
`node_yarn_version`/`node_pnpm_version` pins. Per-user corepack shims under
`~/.nvm/versions/node/*/bin` are not cleaned up — replace them by declaring
the package manager in that version's `global_packages`.

## phpbu: version-pinned, GPG-verified install

The phar (now 6.0.33) and its `.asc` signature are downloaded from the GitHub
release and verified against the signing key shipped with the role before
install. The install is pinned by a single variable:

| Old | New |
|-----|-----|
| `phpbu_phar_url` | removed — derived from `phpbu_version` |
| `phpbu_phar_checksum` | removed — replaced by GPG signature verification |
| `phpbu_schema_url` | removed — derived from `phpbu_version` |
| — | `phpbu_version` (default `6.0.33`) |

If you overrode any of the removed variables to pin a different release, set
`phpbu_version` instead. The role also gained an uninstall entrypoint:

```yaml
- ansible.builtin.import_role:
    name: tborealis.roles.phpbu
    tasks_from: remove
```

## rrsync: role removed

Since Debian bookworm, rsync ships `/usr/bin/rrsync` as a first-class binary,
which left the role installing rsync plus a redundant
`/usr/local/bin/rrsync` symlink. Roles that need rsync (e.g. `dbcd` server
mode) install it themselves, and `dbcd`'s forced commands resolve `rrsync`
via PATH.

Removing the role does not delete the symlink from existing hosts, so
`authorized_keys` entries hardcoding `/usr/local/bin/rrsync` keep working
until it is removed manually. Rewrite them to plain `rrsync` (or
`/usr/bin/rrsync`) anyway — the symlink is no longer managed.

## apache2: dead variables removed

`apache2_load_modules` and `apache2_conf` are removed. They were declared and
documented but used by no task, so nothing you configured through them ever
took effect — delete them from inventories. Use `apache2_modules` to enable
modules.

`/etc/apache2/envvars` now renders `APACHE_RUN_USER`/`APACHE_RUN_GROUP` from
`apache2_user` (previously hardcoded `www-data`; the default is unchanged),
and changes to it restart Apache.

## base and exim4: variables gain role prefixes

All of base's unprefixed variables are renamed with a `base_` prefix, and
exim4's `mailname` becomes `exim4_mailname`. Rendered configs are unchanged
when the new names carry the old values — this is a pure inventory rename.

| Old | New |
|-----|-----|
| `system_locales` | `base_system_locales` |
| `system_default_locale` | `base_system_default_locale` |
| `system_timezone` | `base_system_timezone` |
| `system_packages` | `base_system_packages` |
| `dns_primary_nameserver` | `base_dns_primary_nameserver` |
| `dns_secondary_nameserver` | `base_dns_secondary_nameserver` |
| `default_users` | `base_default_users` |
| `users` | `base_users` |
| `local_hostnames` | `base_local_hostnames` |
| `known_hosts` | `base_known_hosts` |
| `ssh_extra_user_groups` | `base_ssh_extra_user_groups` |
| `ssh_allow_tcp_forwarding` | `base_ssh_allow_tcp_forwarding` |
| `mailname` (exim4) | `exim4_mailname` |

Note that `pgsql_locale` no longer follows `system_default_locale` (see the
pgsql section), so renaming the base variable does not cascade.

## base: dead `ssh_extra_conf_files` removed

`ssh_extra_conf_files` was referenced by no task; nothing you configured
through it ever took effect. Delete it from inventories. The unreachable
`fix-prompt.yml` task file is also gone (the skel-level prompt task in
`main.yml` is the live implementation).
