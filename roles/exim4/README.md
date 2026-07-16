# exim4

Installs and configures Exim4 mail transfer agent.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `exim4_sender_hostname` | `{{ inventory_hostname }}` | Sender hostname for outgoing mail |
| `exim4_mailname` | `{{ inventory_hostname }}` | System mail name, written to `/etc/mailname` and included in exim's local domains so aliased local mail (e.g. postmaster) stays routeable |
