# nginx

Installs and configures Nginx web server from the nginx.org stable repository.

## Versions and automatic updates

nginx.org numbers stable branches with even minor versions (1.30) and mainline
with odd ones. Only the newest stable branch gets security fixes. A new one is
released each April and carries a year of mainline behaviour changes, while
releases within a branch carry only security and critical fixes.

The role installs the `nginx_version` branch and pins `nginx` and its
`nginx-module-*` packages to it, so upgrades, unattended ones included, stay
within that branch. It also installs `unattended-upgrades` and adds the nginx.org
repository to its allowed origins, so the branch's patch releases install
unattended on the schedule `base` configures. On a host without `base`, installing
`unattended-upgrades` also enables Debian's default automatic updates. Set
`nginx_unattended_upgrades: false` to leave nginx upgrades to manual runs.

Changing `nginx_version` moves the host to that branch on the next run. The default
follows the newest stable branch, so it changes, as a breaking release, each April.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `nginx_version` | `1.30` | Stable branch to install; upgrades stay within it |
| `nginx_unattended_upgrades` | `true` | Let unattended-upgrades install patch releases from the nginx.org repository |
| `nginx_user` | `nginx` | User that Nginx runs as |
| `nginx_basic_auth` | `[]` | Basic auth configurations |
| `nginx_conf` | `[]` | Additional configuration files |
| `nginx_vhosts` | `[]` | Virtual host configurations |
| `nginx_modules` | `[]` | Modules to enable |
| `nginx_snippets` | `[]` | Configuration snippets |
| `nginx_server_tokens` | `off` | Show/hide server version |
| `nginx_certbot_plugin` | `false` | Install Certbot Nginx plugin |
| `nginx_client_max_body_size` | `8m` | Maximum client request body size |

## Templates

The `src` of each `nginx_conf`, `nginx_snippets`, and `nginx_vhosts` entry is
resolved relative to the consuming playbook, so the templates must live next
to it in `templates/nginx/conf/`, `templates/nginx/snippets/`, and
`templates/nginx/vhosts/` respectively. See this role's molecule scenario
(`molecule/default/templates/`) for a working example.
