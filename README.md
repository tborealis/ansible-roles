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
| [aws_cli](roles/aws_cli/README.md) | AWS CLI installation and configuration |
| [aws_config](roles/aws_config/README.md) | AWS credentials configuration |
| [base](roles/base/README.md) | Base system configuration |
| [certbot](roles/certbot/README.md) | Let's Encrypt SSL certificates |
| [chrome](roles/chrome/README.md) | Google Chrome and ChromeDriver |
| [composer](roles/composer/README.md) | PHP Composer |
| [cron](roles/cron/README.md) | Cron job management |
| [dbcd](roles/dbcd/README.md) | Database Copy Down |
| [do_agent](roles/do_agent/README.md) | DigitalOcean monitoring agent |
| [dotenv](roles/dotenv/README.md) | Dotenv file creation |
| [environment](roles/environment/README.md) | Environment file management |
| [exim4](roles/exim4/README.md) | Exim4 mail transfer agent |
| [git](roles/git/README.md) | Git installation and configuration |
| [gpg](roles/gpg/README.md) | GPG key management |
| [mailhog](roles/mailhog/README.md) | MailHog email testing |
| [mysql](roles/mysql/README.md) | MySQL server |
| [new_relic](roles/new_relic/README.md) | New Relic PHP agent |
| [nginx](roles/nginx/README.md) | Nginx web server |
| [node](roles/node/README.md) | Node.js from NodeSource |
| [nvm](roles/nvm/README.md) | Node Version Manager |
| [pgsql](roles/pgsql/README.md) | PostgreSQL server |
| [pgsql_client](roles/pgsql_client/README.md) | PostgreSQL client |
| [php_cli](roles/php_cli/README.md) | PHP CLI configuration |
| [php_fpm](roles/php_fpm/README.md) | PHP-FPM configuration |
| [php_repo_sury](roles/php_repo_sury/README.md) | Sury PHP repository |
| [phpbu](roles/phpbu/README.md) | PHPBU database backups |
| [rabbitmq](roles/rabbitmq/README.md) | RabbitMQ message broker |
| [redis](roles/redis/README.md) | Redis server |
| [rrsync](roles/rrsync/README.md) | Restricted rsync |
| [ssl](roles/ssl/README.md) | SSL certificate management |
| [stripe_cli](roles/stripe_cli/README.md) | Stripe CLI |
| [sudo](roles/sudo/README.md) | Sudo configuration |
| [supervisor](roles/supervisor/README.md) | Supervisor process manager |
| [symfony_params](roles/symfony_params/README.md) | Symfony parameters |
| [tasks](roles/tasks/README.md) | Shared task files |
| [yarn](roles/yarn/README.md) | Yarn package manager |

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

See `galaxy.yml` for collection metadata and dependencies.
