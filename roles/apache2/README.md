# apache2

Installs and configures Apache2 web server with virtual hosts and modules.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `apache2_user` | `www-data` | User that Apache runs as |
| `apache2_vhosts` | `[]` | List of virtual host configurations |
| `apache2_basic_auth` | `[]` | List of basic auth configurations |
| `apache2_load_modules` | `[]` | Additional modules to load |
| `apache2_conf` | `[]` | Additional configuration files |
| `apache2_packages` | `[apache2, apache2-utils, python3-passlib]` | Packages to install |
| `apache2_modules` | `[proxy_fcgi, setenvif, rewrite, headers, ssl]` | Modules to enable |
| `apache2_disable_modules` | `[mpm_prefork]` | Modules to disable |
| `apache2_env_vars` | `[]` | Environment variables to set |
