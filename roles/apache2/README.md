# apache2

Installs and configures Apache2 web server with virtual hosts and modules.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `apache2_user` | `www-data` | User that Apache runs as |
| `apache2_vhosts` | `[]` | List of virtual host configurations; one removed from the list is disabled and deleted on the next run |
| `apache2_basic_auth` | `[]` | List of basic auth configurations |
| `apache2_packages` | `[apache2, apache2-utils, python3-passlib]` | Packages to install |
| `apache2_modules` | `[proxy_fcgi, setenvif, rewrite, headers, ssl]` | Modules to enable; one removed from the list is disabled on the next run |
| `apache2_disable_modules` | `[mpm_prefork]` | Modules to disable |
| `apache2_env_vars` | `{}` | Environment variables to set |
| `apache2_server_tokens` | `Prod` | `ServerTokens`: how much of the version and OS the `Server` header shows |
| `apache2_server_signature` | `Off` | `ServerSignature`: the version footer on Apache's own error and index pages |
| `apache2_ssl_protocols` | `-all +TLSv1.2 +TLSv1.3` | `SSLProtocol` for every vhost (tlsref intermediate) |
| `apache2_ssl_curves` | `X25519MLKEM768:X25519:prime256v1:secp384r1` (bookworm: without `X25519MLKEM768`) | Key exchange groups (`SSLOpenSSLConfCmd Curves`) |
| `apache2_ssl_ciphers` | tlsref intermediate TLS 1.2 ciphers (ECDHE with AES-GCM or ChaCha20-Poly1305) | `SSLCipherSuite` for TLS 1.2 |
| `apache2_reject_unknown_hosts` | `true` | Answer HTTPS requests for hostnames no vhost names with `403` and Debian's self-signed certificate |

## Templates

The `src` of each `apache2_vhosts` entry is resolved relative to the consuming
playbook, so the vhost templates must live next to it in
`templates/apache2/vhosts/`. See this role's molecule scenario
(`molecule/default/templates/`) for a working example.

Server-wide settings go in `/etc/apache2/conf-available/server-defaults.conf`, which
is enabled after Debian's `security.conf` so its values take precedence. That
includes the TLS settings, which follow tlsref's intermediate profile; a vhost can
still set its own.

It also adds the first vhost on port 443, which answers requests for hostnames that
no other vhost names (including requests by IP address or without SNI) with `403`
and Debian's self-signed snakeoil certificate. Without it, Apache passes them to
whichever vhost sorts first. Port 80 is left alone, so a playbook's catch-all
HTTP-to-HTTPS redirect keeps working.

The role records the modules and vhosts it enabled in
`/var/lib/apache2/ansible-managed.json`, and disables any that have left
`apache2_modules` or `apache2_vhosts` since the previous run. Modules and vhosts
enabled by Debian or by hand are never touched, and nothing is disabled on the first
run of this version, which only writes the record.

Vhosts and `/etc/apache2/envvars` are installed `0640 root:root`, as they can hold
secrets such as `OIDCClientSecret`; Apache reads them as root before dropping
privileges.
