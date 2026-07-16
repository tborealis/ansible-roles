# base

Base system configuration including locales, timezone, users, DNS, and essential packages.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `base_system_locales` | `["en_US.UTF-8", "en_GB.UTF-8"]` | Locales to generate |
| `base_system_default_locale` | `en_GB.UTF-8` | Default system locale |
| `base_system_timezone` | `Europe/London` | System timezone |
| `base_system_packages` | `[]` | Additional packages to install |
| `base_dns_primary_nameserver` | `1.1.1.1` | Primary DNS server |
| `base_dns_secondary_nameserver` | `1.0.0.1` | Secondary DNS server |
| `base_default_users` | `[]` | Default users to create |
| `base_users` | `[]` | Additional users to create |
| `base_local_hostnames` | `[]` | Local hostname entries |
| `base_known_hosts` | `[]` | SSH known hosts entries |
| `base_ssh_extra_user_groups` | `[]` | Extra groups for SSH users |
| `base_ssh_allow_tcp_forwarding` | `false` | Allow SSH TCP forwarding |
| `base_default_system_packages` | See defaults | Essential system packages |
| `base_profile_config` | `[]` | Profile configuration entries |
| `base_hosts_unsafe_writes` | `false` | Write /etc/hosts in place (for containers, where the bind mount breaks atomic renames) |
