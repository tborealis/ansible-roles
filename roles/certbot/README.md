Certbot role
============

This role installs certbot and requests certificates for the specified domains. It can be used in three modes: 
- `nginx`
- `apache`
- `dns-digitalocean`

Config
------

```yaml
certbot_mode: nginx|dns-digitalocean|apache
certbot_certs: # array of certificates to request
- admin_email: admin@example.com # administration email address
  name: example.com # name of the certificate
  domains: # array of domains in single certificate
  - example.com
  - test.example.com
  deploy_hook: /path/to/deploy.sh # optional script to run after certificate renewal
certbot_dry_run: false # test mode that prevents creation or download of certs (default: false)
certbot_apache2_ssl_vhosts: # apache mode only: SSL vhosts to install once certificates exist (default: apache2_vhosts if defined, else [])
- src: example-ssl.conf.j2 # template resolved from templates/apache2/vhosts/ next to the playbook
  dest: example-ssl.conf # filename under /etc/apache2/sites-available/, symlinked into sites-enabled
```

Notes
-----

The name key will be used for the dir of the certificate. In the example above the cert will be
stored at `/etc/letsencrypt/live/example.com/cert.pem`.

If using the `nginx` mode, this role should be run before nginx is installed as nginx will fail to start if the certs 
are not present.

If using the `apache` mode, apache2 must already be installed (e.g. via the `apache2` role). Vhost templates listed in
`certbot_apache2_ssl_vhosts` are resolved relative to the consuming playbook, so they must live in `templates/apache2/vhosts/`
next to it.

If using the `dns-digitalocean` mode, you will need to set the `certbot_digitalocean_dns_token` var to an API token with
all `domain` scopes. This can be generated at https://cloud.digitalocean.com/account/api/tokens/new.

See https://certbot.eff.org/docs/using.html#where-are-my-certificates for more details on which keys and certs
should be used in the webserver config.

The `certbot_dry_run` option is useful for testing the role without actually requesting certificates, which avoids rate 
limit issues.
