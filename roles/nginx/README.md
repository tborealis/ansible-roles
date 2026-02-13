# nginx

Installs and configures Nginx web server.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `nginx_user` | `nginx` | User that Nginx runs as |
| `nginx_basic_auth` | `[]` | Basic auth configurations |
| `nginx_conf` | `[]` | Additional configuration files |
| `nginx_vhosts` | `[]` | Virtual host configurations |
| `nginx_modules` | `[]` | Modules to enable |
| `nginx_snippets` | `[]` | Configuration snippets |
| `nginx_server_tokens` | `off` | Show/hide server version |
| `nginx_certbot_plugin` | `false` | Install Certbot Nginx plugin |
| `nginx_client_max_body_size` | `8m` | Maximum client request body size |
