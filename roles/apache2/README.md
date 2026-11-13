# apache2

Installs and configures Apache2 web server with virtual hosts and modules.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `apache2_user` | `www-data` | User that Apache runs as |
| `apache2_vhosts` | `[]` | List of virtual host configurations |
| `apache2_basic_auth` | `[]` | List of basic auth configurations |
| `apache2_packages` | `[apache2, apache2-utils, python3-passlib]` | Packages to install |
| `apache2_modules` | `[proxy_fcgi, setenvif, rewrite, headers, ssl]` | Modules to enable |
| `apache2_disable_modules` | `[mpm_prefork]` | Modules to disable |
| `apache2_env_vars` | `{}` | Environment variables to set |
| `apache2_server_tokens` | `Prod` | `ServerTokens`: how much of the version and OS the `Server` header shows |
| `apache2_server_signature` | `Off` | `ServerSignature`: the version footer on Apache's own error and index pages |

## Templates

The `src` of each `apache2_vhosts` entry is resolved relative to the consuming
playbook, so the vhost templates must live next to it in
`templates/apache2/vhosts/`. See this role's molecule scenario
(`molecule/default/templates/`) for a working example.

Server-wide settings go in `/etc/apache2/conf-available/server-defaults.conf`, which
is enabled after Debian's `security.conf` so its values take precedence.

Vhosts and `/etc/apache2/envvars` are installed `0640 root:root`, as they can hold
secrets such as `OIDCClientSecret`; Apache reads them as root before dropping
privileges.
