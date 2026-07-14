# pgsql_client

Installs PostgreSQL client tools.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `postgres_version` | — (required) | PostgreSQL client major version to install (any major available in the pgdg apt repository) |
| `postgres_default_packages` | See defaults | PostgreSQL client packages to install |
