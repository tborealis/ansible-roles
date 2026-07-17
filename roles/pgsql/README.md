# pgsql

Installs and configures PostgreSQL from the PGDG repository — a full server by
default, or just the client tools with `pgsql_mode: client`. This role
absorbed the removed `pgsql_client` role — see
[docs/migrating-v6.md](../../docs/migrating-v6.md).

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `pgsql_mode` | `server` | `server` installs and configures a full server; `client` installs only the PGDG repository and client tools |
| `pgsql_version` | — (required) | PostgreSQL major version to install. Server mode supports 15–18; client mode accepts any PGDG major |
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
| `pgsql_shared_buffers` | `1GB` | Shared buffers size (1/4 RAM, 4GB baseline) |
| `pgsql_effective_cache_size` | `2GB` | Effective cache size (1/2 RAM, 4GB baseline) |
| `pgsql_work_mem` | `4MB` | Per-operation sort/hash memory |
| `pgsql_maintenance_work_mem` | `256MB` | VACUUM / CREATE INDEX memory |
| `pgsql_random_page_cost` | `1.1` | 1.1 SSD/NVMe / 4.0 spinning disks |
| `pgsql_max_connections` | `100` | Maximum connections |
| `pgsql_risky_fast` | `false` | Disable fsync for speed (data loss risk) |
| `pgsql_full_page_writes` | `on` | Full page writes (off if risky_fast) |
| `pgsql_synchronous_commit` | `on` | Synchronous commit (off if risky_fast) |
| `pgsql_fsync` | `on` | Fsync writes (off if risky_fast) |
| `pgsql_max_wal_size` | `1GB` | Soft WAL ceiling between checkpoints |
| `pgsql_wal_compression` | `lz4` | Compress WAL full-page images (`off`, `pglz`, `lz4`, `zstd`) |
| `pgsql_io_method` | `worker` | PostgreSQL 18+ only: async I/O method (`worker`, `io_uring`, `sync`) |
| `pgsql_timezone` | `Europe/London` | Server and log timezone |
| `pgsql_locale` | `en_GB.UTF-8` | Database locale |

## Tuning

Defaults are sized for a 4GB-RAM SSD/NVMe host with a mixed workload; adjust
per host:

- **`pgsql_shared_buffers`** — PostgreSQL's own page cache; ~25% of RAM is
  the standard starting point. Going much higher rarely helps because the OS
  page cache does the rest.
- **`pgsql_effective_cache_size`** — a planner *hint* (no memory is
  allocated): how much of the dataset is likely cached across shared buffers
  plus the OS cache. ~50–75% of RAM; higher values make index scans more
  attractive.
- **`pgsql_work_mem`** — memory per sort/hash *per query node*, so the worst
  case is roughly connections × nodes × work_mem. Keep low (4–8MB) for
  many-connection OLTP; raise (16–64MB) for analytics/reporting with few
  concurrent queries to avoid on-disk sorts.
- **`pgsql_maintenance_work_mem`** — used by VACUUM, CREATE INDEX and
  autovacuum workers. The 256MB default suits the 4GB baseline; drop toward
  the stock 64MB on smaller hosts, raise further on larger ones for faster
  index builds.
- **`pgsql_random_page_cost`** — how expensive the planner thinks random I/O
  is relative to sequential (1.0). 1.1 for SSD/NVMe, 4.0 for spinning disks;
  lowering it biases the planner toward index scans.
- **`pgsql_max_connections`** — keep modest and use a pooler (e.g. PgBouncer)
  rather than raising it: every connection costs memory and multiplies the
  worst-case `work_mem`.
- **`pgsql_max_wal_size`** — soft ceiling on WAL between checkpoints. Raise
  (2–4GB) on write-heavy hosts with disk to spare: fewer, calmer checkpoints
  and fewer full-page images, at the cost of longer crash recovery.
- **`pgsql_wal_compression`** — compresses the full-page images that dominate
  WAL volume on write-heavy loads. `lz4` (default) is near-free CPU; `zstd`
  compresses harder if CPU is spare; `off` only if CPU-bound at peak write
  throughput. Safe to change on an existing cluster — it only affects newly
  written WAL.
- **`pgsql_io_method`** (18+) — `worker` (stock) suits most hosts; `io_uring`
  can help high-concurrency I/O on modern kernels; `sync` restores pre-18
  behaviour.
- **`pgsql_risky_fast`** — turns off fsync/synchronous_commit/
  full_page_writes for a large write-speed boost. A crash can corrupt the
  cluster unrecoverably: only for disposable data.
