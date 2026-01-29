# base

Base system configuration including locales, timezone, users, DNS, and essential packages.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `system_locales` | `["en_US.UTF-8", "en_GB.UTF-8"]` | Locales to generate |
| `system_default_locale` | `en_GB.UTF-8` | Default system locale |
| `system_timezone` | `Europe/London` | System timezone |
| `system_packages` | `[]` | Additional packages to install |
| `dns_primary_nameserver` | `1.1.1.1` | Primary DNS server |
| `dns_secondary_nameserver` | `1.0.0.1` | Secondary DNS server |
| `default_users` | `[]` | Default users to create |
| `users` | `[]` | Additional users to create |
| `local_hostnames` | `[]` | Local hostname entries |
| `vagrant` | `false` | Whether running in Vagrant |
| `known_hosts` | `[]` | SSH known hosts entries |
| `ssh_extra_user_groups` | `[]` | Extra groups for SSH users |
| `ssh_extra_conf_files` | `[]` | Extra SSH config files |
| `ssh_allow_tcp_forwarding` | `false` | Allow SSH TCP forwarding |
| `base_default_system_packages` | See defaults | Essential system packages |
| `base_profile_config` | `[]` | Profile configuration entries |
