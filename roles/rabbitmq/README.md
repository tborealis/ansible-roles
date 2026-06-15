# rabbitmq

Installs and configures the RabbitMQ message broker from RabbitMQ's official APT
repositories on `deb1.rabbitmq.com`: the `rabbitmq-erlang` repository (pinned so its
Erlang packages take precedence over the distribution's) and the `rabbitmq-server`
repository, both signed by the Team RabbitMQ key. The key is managed by the
[apt_keys](../apt_keys/README.md) role.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `rabbitmq_admin_password` | Required | Password for the admin user |
