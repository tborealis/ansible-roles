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

## TLS

`nginx.conf` sets TLS defaults for every server at the `http` level, following
tlsref's intermediate profile: TLS 1.2 and 1.3, forward-secret AEAD ciphers only,
the hybrid post-quantum X25519MLKEM768 key exchange where OpenSSL supports it
(trixie), and a shared session cache. Server blocks only need their certificate and
key. Override the `nginx_ssl_*` variables to change the defaults; nginx rejects the
same directives set again at the `http` level, e.g. in a `conf.d` file.

By default `nginx.conf` also declares the `default_server` for `443` and
`[::]:443`. It refuses TLS handshakes whose SNI matches no `server_name`, or that
carry none, and closes the connection on requests whose `Host` matches no
`server_name`. Without it the first vhost on 443 answers them, so an application
could build links from an attacker's `Host` header. Vhosts must not declare their
own `default_server` on 443, and clients connecting by IP address or without SNI
are refused. Set `nginx_reject_unknown_hosts: false` to turn it off. Port 80 is
left to the vhosts.

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
| `nginx_ssl_protocols` | `TLSv1.2 TLSv1.3` | TLS versions offered |
| `nginx_ssl_ecdh_curve` | `X25519MLKEM768:X25519:prime256v1:secp384r1` (bookworm: without `X25519MLKEM768`) | Key exchange groups, in order of preference |
| `nginx_ssl_ciphers` | tlsref intermediate list | TLS 1.2 cipher suites (ECDHE with AES-GCM or ChaCha20-Poly1305) |
| `nginx_ssl_session_timeout` | `1d` | How long a TLS session can be resumed |
| `nginx_ssl_session_cache` | `shared:SSL:10m` | TLS session cache shared by the worker processes |
| `nginx_reject_unknown_hosts` | `true` | Add a default server on 443 that refuses hostnames no vhost serves |

## Templates

The `src` of each `nginx_conf`, `nginx_snippets`, and `nginx_vhosts` entry is
resolved relative to the consuming playbook, so the templates must live next
to it in `templates/nginx/conf/`, `templates/nginx/snippets/`, and
`templates/nginx/vhosts/` respectively. See this role's molecule scenario
(`molecule/default/templates/`) for a working example.
