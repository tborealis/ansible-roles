# mysql

Installs and configures MySQL server.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `mysql_version` | `8.4-lts` | MySQL version to install |
| `mysql_users` | `[]` | Users to create |
| `mysql_databases` | `[]` | Databases to create |
| `mysql_innodb_buffer_pool_size` | | InnoDB buffer pool size (required, max 0.5 * RAM) |
| `mysql_innodb_log_file_size` | `128M` | InnoDB log file size (256M if >8GB RAM) |
| `mysql_innodb_flush_log_at_trx_commit` | `1` | Flush log at commit (0 for VM performance) |
| `mysql_innodb_log_files_in_group` | `2` | Log files in group (4 if >2GB RAM) |
| `mysql_slow_query_log` | `0` | Enable slow query logging |
