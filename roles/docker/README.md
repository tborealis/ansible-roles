# docker

Installs Docker Engine (`docker-ce`, `docker-ce-cli` and `containerd.io`) and the Compose and
Buildx CLI plugins (`docker compose`, `docker buildx`) from Docker's apt repository, and writes
`/etc/docker/daemon.json`.

The daemon logs with the `local` driver, which rotates logs (the default `json-file` driver
keeps them forever), and by default sets `no-new-privileges` on every container: setuid and
setgid binaries in an image can't raise a process's privileges. This also covers Swarm services,
whose stack files can't set `security_opt`. A container that needs setuid (sudo inside a
container, for example) has to run on a host with `docker_no_new_privileges: false`.

Docker's repository is added to unattended-upgrades, on the schedule `base` configures. An
upgrade restarts dockerd, which restarts every container, including Swarm services.

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
| `docker_unattended_upgrades` | `true` | Let unattended-upgrades install updates from Docker's repository; `false` removes that opt-in |
| `docker_daemon_config` | `{}` | Further `daemon.json` settings, merged over the role's `log-driver` and `no-new-privileges`; `dockerd --validate` must accept the result |
