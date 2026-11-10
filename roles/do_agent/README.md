# do_agent

Installs the DigitalOcean monitoring agent (`do-agent`).

It also removes `droplet-agent`, which DigitalOcean installs at droplet creation to
power the control panel's browser-based Droplet Console. The agent runs as root and
writes temporary keys into a user's `authorized_keys` when a console session opens,
so control-panel access grants a shell without going through the managed SSH keys.
The role purges the `droplet-agent` and `droplet-agent-keyring` packages (stopping
the agent and its hourly self-updater) and removes the apt source and pin added by
DigitalOcean's install script. The Recovery Console does not use the agent.

DigitalOcean does not reinstall the agent later. To restore it, set
`do_agent_remove_droplet_agent: false` and run DigitalOcean's install script.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `do_agent_remove_droplet_agent` | `true` | Purge DigitalOcean's `droplet-agent` and its apt repository; `false` leaves an existing install untouched |
