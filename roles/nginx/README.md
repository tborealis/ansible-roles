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

## Templates

The `src` of each `nginx_conf`, `nginx_snippets`, and `nginx_vhosts` entry is
resolved relative to the consuming playbook, so the templates must live next
to it in `templates/nginx/conf/`, `templates/nginx/snippets/`, and
`templates/nginx/vhosts/` respectively. See this role's molecule scenario
(`molecule/default/templates/`) for a working example.
