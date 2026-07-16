# pgsql

Installs and configures PostgreSQL from the PGDG repository — a full server by
default, or just the client tools with `pgsql_mode: client`. This role
absorbed the removed `pgsql_client` role — see
[docs/migrating-v6.md](../../docs/migrating-v6.md).

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `pgsql_mode` | `server` | `server` installs and configures a full server; `client` installs only the PGDG repository and client tools |
| `pgsql_version` | — (required) | PostgreSQL major version to install. Server mode must be one the role ships config templates for (12, 13, 15, 17 or 18); client mode accepts any PGDG major |
| `pgsql_client_packages` | See defaults | Client packages, installed in both modes |

Server mode only:

| Variable | Default | Description |
|----------|---------|-------------|
| `pgsql_server_packages` | See defaults | Server packages to install |
| `pgsql_additional_packages` | `[]` | Additional packages to install |
| `pgsql_databases` | `[]` | Databases to create |
| `pgsql_users` | `[]` | Users to create |
| `pgsql_schemas` | `[]` | Schemas to create (keys: `db`, `name`, `owner`) |
| `pgsql_privs` | `[]` | Privileges to grant (keys: `db`, `roles`, `privs`, `type`, `objs`, `schema`, `target_roles`) |
| `pgsql_extensions` | `[]` | Extensions to enable |
| `pgsql_become_user` | `postgres` | System user to run database operations as |
| `pgsql_shared_buffers` | `512MB` | Shared buffers size (1/4 RAM) |
| `pgsql_effective_cache_size` | `1GB` | Effective cache size (1/2 RAM) |
| `pgsql_max_connections` | `100` | Maximum connections |
| `pgsql_risky_fast` | `false` | Disable fsync for speed (data loss risk) |
| `pgsql_full_page_writes` | `on` | Full page writes (off if risky_fast) |
| `pgsql_synchronous_commit` | `on` | Synchronous commit (off if risky_fast) |
| `pgsql_fsync` | `on` | Fsync writes (off if risky_fast) |
| `pgsql_max_wal_size` | `1GB` | Maximum WAL size |
| `pgsql_locale` | `en_GB.UTF-8` | Database locale |
