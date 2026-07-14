# mailpit

Installs [Mailpit](https://github.com/axllent/mailpit) for email testing in development
environments. Mailpit is the maintained successor to MailHog and serves the same
purpose with the same default ports: SMTP capture on 1025 and a web UI/API on 8025.

This role replaces the deprecated `mailhog` role.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `mailpit_version` | See defaults | Mailpit release to install |
| `mailpit_checksums` | See defaults | sha256 checksums of the release tarball per architecture (`amd64`, `arm64`) |
| `mailpit_install_dir` | `/opt/mailpit` | Installation directory |
| `mailpit_user` | `mailpit` | User to run Mailpit as |

## Updating

Upstream publishes no checksum manifest, so when bumping `mailpit_version` update both
`mailpit_checksums` entries from the release tarballs
(`https://github.com/axllent/mailpit/releases/download/v<version>/mailpit-linux-<arch>.tar.gz`).
