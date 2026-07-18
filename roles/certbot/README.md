# certbot

Installs certbot and requests Let's Encrypt certificates in one of three modes:
`nginx`, `apache` or `dns-digitalocean`.

## Requirements

- `nginx` mode should run **before** nginx is installed, as nginx fails to start
  when configured certificates are missing.
- `apache` mode expects apache2 to be installed already (e.g. via the `apache2` role).
- `dns-digitalocean` mode needs a DigitalOcean API token with all `domain` scopes,
  generated at https://cloud.digitalocean.com/account/api/tokens/new.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `certbot_mode` | Required | Mode: `nginx`, `apache` or `dns-digitalocean` |
| `certbot_certs` | `[]` | Certificates to request; see below |
| `certbot_dry_run` | `false` | Pass `--dry-run` to certbot: exercises the request without creating certificates, avoiding rate limits |
| `certbot_apache2_ssl_vhosts` | `apache2_vhosts` if defined, else `[]` | `apache` mode only: SSL vhosts to install once certificates exist; see below |
| `certbot_digitalocean_dns_token` | Required in `dns-digitalocean` mode | DigitalOcean API token with all `domain` scopes |

## Certificates

Each `certbot_certs` item requests one certificate:

```yaml
certbot_certs:
  - name: example.com                # certificate directory: /etc/letsencrypt/live/<name>/
    admin_email: admin@example.com   # registration and expiry email address
    domains:                         # domains covered by the single certificate
      - example.com
      - test.example.com
    deploy_hook: /path/to/deploy.sh  # optional: script run after issue/renewal
```

See https://certbot.eff.org/docs/using.html#where-are-my-certificates for which keys
and certificates to reference in webserver config.

## Apache SSL vhosts

`apache` mode installs the vhosts in `certbot_apache2_ssl_vhosts` after the
certificates exist. Templates are resolved relative to the consuming playbook, so they
must live in `templates/apache2/vhosts/` next to it:

```yaml
certbot_apache2_ssl_vhosts:
  - src: example-ssl.conf.j2  # template in templates/apache2/vhosts/
    dest: example-ssl.conf    # filename under /etc/apache2/sites-available/, symlinked into sites-enabled
```
