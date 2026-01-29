# pgsql

Installs and configures PostgreSQL server.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `postgres_databases` | `[]` | Databases to create |
| `postgres_users` | `[]` | Users to create |
| `postgres_privs` | `[]` | Privileges to grant |
| `postgres_extensions` | `[]` | Extensions to enable |
| `postgres_default_packages` | See defaults | PostgreSQL packages to install |
| `postgres_additional_packages` | `[]` | Additional packages to install |
| `postgres_shared_buffers` | `512MB` | Shared buffers size (1/4 RAM) |
| `postgres_effective_cache_size` | `1GB` | Effective cache size (1/2 RAM) |
| `postgres_max_connections` | `100` | Maximum connections |
| `postgres_risky_fast` | `false` | Disable fsync for speed (data loss risk) |
| `postgres_max_wal_size` | `1GB` | Maximum WAL size |
| `postgres_locale` | `{{ system_default_locale }}` | Database locale |
