# exim4

Installs and configures Exim4 mail transfer agent.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `exim4_sender_hostname` | `{{ inventory_hostname }}` | Sender hostname for outgoing mail |
| `mailname` | `{{ inventory_hostname }}` | System mail name |
