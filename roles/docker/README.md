# docker

Installs Docker Engine (`docker-ce`, `docker-ce-cli` and `containerd.io`) and the Compose and
Buildx CLI plugins (`docker compose`, `docker buildx`) from Docker's apt repository, and writes
`/etc/docker/daemon.json`.

The daemon is configured with:

- the `local` log driver, which rotates logs (the default `json-file` driver keeps them
  forever);
- `no-new-privileges` on every container, so setuid and setgid binaries in an image can't
  raise a process's privileges. A Compose service that needs setuid (sudo inside the
  container, for example) opts out with `security_opt: ["no-new-privileges=false"]`;
- a default bind address of `docker_default_bind_address` (`127.0.0.1`) for published
  ports, on the default bridge and on user-defined networks such as Compose's. `ports:
  ["8080:80"]` is then reachable from the host only, e.g. by a reverse proxy; publish
  publicly with an explicit address, `ports: ["0.0.0.0:443:443"]`;
- `userland-proxy: false`, so published ports are reached through NAT rather than a
  `docker-proxy` process. Ports on IPv4-only networks, Compose's default, are not
  reachable over IPv6;
- `icc: false`: containers on the default bridge can't reach each other. Compose's
  networks are unaffected.

`apparmor` is installed so containers get Docker's `docker-default` AppArmor profile;
without `apparmor_parser` they run unconfined.

Published ports bypass ufw and other `INPUT` rules: Docker forwards their traffic to the
container before `INPUT` sees it. So the role filters it in Docker's `DOCKER-USER` chain:
connections that arrive on `docker_firewall_interface` (the default route's interface,
`eth0` on a DigitalOcean droplet) reach only the ports in `docker_firewall_allowed_ports`,
over IPv4 and IPv6. Replies to containers' own connections, and traffic from other
interfaces (loopback, a private VPC network) are unaffected. A public service therefore
needs both an explicit address in Compose and an entry in the list, e.g. `ports:
["0.0.0.0:443:443"]` and `docker_firewall_allowed_ports: [443]`. A oneshot unit,
`docker-firewall.service`, applies the rules before dockerd starts. They need Docker's
default iptables firewall backend.

Each `docker compose pull` leaves the previous image behind, so a weekly timer,
`docker-prune.timer`, removes images no container uses (stopped ones included) and build
cache unused for a week. Volumes are never pruned.

Docker's repository is added to unattended-upgrades, on the schedule `base` configures. An
upgrade restarts dockerd, which restarts every container; give Compose services a restart
policy (`restart: unless-stopped`) so they come back, after reboots too. `live-restore` is
left off: Docker supports it across patch releases only, and unattended upgrades also cross
minor releases.

Docker Engine, containerd and Compose are pinned to a major release (`docker_version`,
`docker_containerd_version`, `docker_compose_version`), so upgrades, unattended ones
included, never cross one: Engine 29.0 raised the minimum API version and broke clients
such as Traefik. Pre-releases are pinned out, even if one reaches the stable channel.
Raising one of these variables upgrades the packages in that run; lowering one doesn't
downgrade them.

## Requirements

Debian 13 (trixie); the role fails on any other release.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `docker_version` | `"29"` | Docker Engine major release to stay on |
| `docker_containerd_version` | `"2"` | containerd.io major release to stay on |
| `docker_compose_version` | `"5"` | Compose plugin major release to stay on |
| `docker_no_new_privileges` | `true` | Set `no-new-privileges` on every container; `false` leaves Docker's default (off) |
| `docker_default_bind_address` | `127.0.0.1` | Host address published ports bind to when they name none |
| `docker_firewall` | `true` | Filter connections from `docker_firewall_interface` to published ports; `false` removes the rules |
| `docker_firewall_interface` | `ansible_facts['default_ipv4']['interface']` | Public interface to filter |
| `docker_firewall_allowed_ports` | `[]` | Published ports reachable through it, e.g. `443`, `"443/udp"`, `"8000:8100"` |
| `docker_prune` | `true` | Prune unused images and old build cache on `docker_prune_schedule`; `false` removes the timer |
| `docker_prune_schedule` | `Sun *-*-* 03:00` | systemd `OnCalendar` schedule for the prune, in local time |
| `docker_unattended_upgrades` | `true` | Let unattended-upgrades install updates from Docker's repository; `false` removes that opt-in |
| `docker_daemon_config` | `{}` | Further `daemon.json` settings, merged over (and replacing) the role's top-level keys; `dockerd --validate` must accept the result |
