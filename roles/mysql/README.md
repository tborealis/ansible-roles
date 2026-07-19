# mysql

Installs and configures MySQL server.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `mysql_version` | `8.4-lts` | MySQL version to install |
| `mysql_users` | `[]` | Users to create (`salt`, exactly 20 characters, makes the password idempotent) |
| `mysql_root_password_salt` | | Optional 20-character salt; without it the root password task reports changed every run |
| `mysql_databases` | `[]` | Databases to create |
| `mysql_innodb_buffer_pool_size` | | InnoDB buffer pool size (required, max 0.5 * RAM) |
| `mysql_innodb_redo_log_capacity` | `256M` | InnoDB redo log capacity (e.g. 1G if >8GB RAM) |
| `mysql_innodb_flush_log_at_trx_commit` | `1` | Flush log at commit (0 for VM performance) |
| `mysql_slow_query_log` | `0` | Enable slow query logging |
| `mysql_login_unix_socket` | `/var/run/mysqld/mysqld.sock` | Socket used for role logins (always matches `root@localhost`) |
