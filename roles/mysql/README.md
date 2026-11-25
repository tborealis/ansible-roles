# mysql

Installs and configures MySQL server.

MySQL accepts TCP connections on 127.0.0.1 only, and its X Protocol listener (port
33060) is off. Clients on the same host connect over the socket or 127.0.0.1. For
clients on other hosts, set `mysql_bind_address: "*"` (every interface) or a list of
addresses, and give their users a matching `host`.

MySQL keeps binary logs for `mysql_binlog_expire_logs_seconds` (default 30 days,
MySQL's own default). Their size follows the write volume, so bulk rewrites such as a
search index rebuild can fill the disk well before then. The value goes in
`/etc/mysql/conf.d/tuning.cnf`, so changing it restarts MySQL, which purges the logs
past the new retention at startup. A value stored with `SET PERSIST` (in
`mysqld-auto.cnf` in the data directory) overrides the file; clear it with
`RESET PERSIST binlog_expire_logs_seconds`.

`mysql_binlog_transaction_compression` compresses the row changes of each transaction
in the binary log with zstd, which can shrink logs from bulk rewrites a lot. It costs
some CPU at commit, and very large single transactions need extra memory while they are
compressed. `performance_schema.binary_log_transaction_compression_stats` reports the
ratio achieved.

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
| `mysql_binlog_expire_logs_seconds` | `2592000` | Seconds MySQL keeps binary logs before purging them (30 days) |
| `mysql_binlog_transaction_compression` | `false` | Compress binary log transactions with zstd |
| `mysql_login_unix_socket` | `/var/run/mysqld/mysqld.sock` | Socket used for role logins (always matches `root@localhost`) |
| `mysql_bind_address` | `127.0.0.1` | Address(es) for TCP connections, comma-separated; `*` for every interface |
| `mysql_mysqlx` | `false` | Enable the X Protocol listener (MySQL Shell, X DevAPI) on `mysql_bind_address` |
