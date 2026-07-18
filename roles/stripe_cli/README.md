# stripe_cli

Installs the Stripe CLI from Stripe's GPG-signed apt repository
(`packages.stripe.dev`), pinned to `stripe_cli_version`. The repository retains
every released version, so any published version can be pinned; the signing key
is managed by the `apt_keys` role.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `stripe_cli_version` | Required | Version of Stripe CLI to install |
