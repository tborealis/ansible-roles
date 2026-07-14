# mailhog

**Deprecated:** upstream MailHog has been archived and unmaintained since ~2020; the
binary download is unverified and amd64-only. Use the [`mailpit`](../mailpit/README.md)
role instead (same default ports). This role will be removed in the next major release.

Installs MailHog for email testing in development environments.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `mailhog_binary_url` | See defaults | URL to download MailHog binary |
| `mailhog_install_dir` | `/opt/mailhog` | Installation directory |
| `mailhog_user` | `mailhog` | User to run MailHog as |
