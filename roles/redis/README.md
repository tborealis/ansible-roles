# redis

Installs and configures Redis server from the official
[`packages.redis.io`](https://packages.redis.io) APT repository.

Managed directives are written to `/etc/redis/redis-ansible.conf`, which is included at
the end of the packaged `/etc/redis/redis.conf` so its values take precedence. The
service is enabled and started, and restarted when the configuration changes.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `redis_version` | `""` | Empty installs the latest available version. Set to a major (`8`) or major.minor (`7.4`) to pin that line via `/etc/apt/preferences.d/redis.pref`. The pinned version must still be present in the repository pool. |
| `redis_bind` | `127.0.0.1 -::1` | Addresses Redis listens on. Defaults to localhost only (IPv4 and IPv6 loopback). |
| `redis_maxmemory` | `"0"` | Memory limit (e.g. `256mb`). `0` means no limit. |
| `redis_maxmemory_policy` | `noeviction` | Eviction policy applied when `maxmemory` is reached. |
| `redis_password` | `""` | When set, requires this password (`requirepass`) for client connections. Empty disables authentication. |
| `redis_overcommit_memory` | `false` | Set `vm.overcommit_memory=1` via sysctl. |
