# Ansible Collection - tborealis.roles

Ansible Galaxy collection of roles for provisioning development and production environments.
Requires **Ansible 2.15** or newer.

## Installation

Install the latest version directly from GitHub:

```shell
ansible-galaxy collection install git+https://github.com/tborealis/ansible-roles.git
```

## Usage

Reference the roles using the collection namespace:

```yaml
- hosts: all
  roles:
    - role: tborealis.roles.base
```

## Roles

| Role | Description |
|------|-------------|
| [ant](roles/ant/README.md) | Apache Ant installation |
| [apache2](roles/apache2/README.md) | Apache2 web server |
| [apt_keys](roles/apt_keys/README.md) | Centralised apt repository signing keys |
| [aws](roles/aws/README.md) | AWS CLI installation and per-user configuration |
| [base](roles/base/README.md) | Base system configuration |
| [certbot](roles/certbot/README.md) | Let's Encrypt SSL certificates |
| [chrome](roles/chrome/README.md) | Google Chrome and ChromeDriver |
| [cron](roles/cron/README.md) | Cron job management |
| [dbcd](roles/dbcd/README.md) | Database Copy Down |
| [do_agent](roles/do_agent/README.md) | DigitalOcean monitoring agent |
| [env_file](roles/env_file/README.md) | Environment (.env / profile.d) file management |
| [exim4](roles/exim4/README.md) | Exim4 mail transfer agent |
| [git](roles/git/README.md) | Git installation and configuration |
| [gpg](roles/gpg/README.md) | GPG key management |
| [mailpit](roles/mailpit/README.md) | Mailpit email testing |
| [mysql](roles/mysql/README.md) | MySQL server |
| [nginx](roles/nginx/README.md) | Nginx web server |
| [node](roles/node/README.md) | Node.js from NodeSource, npm/Yarn/pnpm, extra versions via tj/n or per-user nvm |
| [pgsql](roles/pgsql/README.md) | PostgreSQL server and client |
| [php](roles/php/README.md) | PHP stack (Sury repo, CLI, FPM, Composer, New Relic) |
| [phpbu](roles/phpbu/README.md) | PHPBU database backups |
| [rabbitmq](roles/rabbitmq/README.md) | RabbitMQ message broker |
| [redis](roles/redis/README.md) | Redis server |
| [ssl](roles/ssl/README.md) | SSL certificate management |
| [stripe_cli](roles/stripe_cli/README.md) | Stripe CLI |
| [sudo](roles/sudo/README.md) | Sudo configuration |
| [supervisor](roles/supervisor/README.md) | Supervisor process manager |
| [symfony_params](roles/symfony_params/README.md) | Symfony parameters |

## Development

Run `make lint` to check the collection with Docker:

```shell
make lint
```

The ansible-lint version is pinned in `requirements-dev.txt` and shared between CI and local linting.
If Docker is unavailable, install the dependencies locally and run ansible-lint directly:

```shell
pip install -r requirements-dev.txt
ansible-lint
```

Run `make check-keys` to check the apt repository signing keys for expiry and to verify
each one still validates its repository on Debian bookworm and trixie. A scheduled CI job
runs the same checks weekly and posts to Slack when a key is expiring or no longer verifies.

See `galaxy.yml` for collection metadata and dependencies.

## Releases

The collection follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and
records every change in [`CHANGELOG.md`](CHANGELOG.md). Releases are cut by pushing a
`vX.Y.Z` tag to `main`, which publishes a GitHub Release via GitHub Actions. See
[`docs/releasing.md`](docs/releasing.md) for the full process and changelog conventions.
