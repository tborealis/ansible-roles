# docker

Installs Docker Engine (`docker-ce`, `docker-ce-cli` and `containerd.io`) from Docker's apt
repository and writes `/etc/docker/daemon.json`.

The daemon logs with the `local` driver, which rotates logs (the default `json-file` driver
keeps them forever), and by default sets `no-new-privileges` on every container: setuid and
setgid binaries in an image can't raise a process's privileges. This also covers Swarm services,
whose stack files can't set `security_opt`. A container that needs setuid (sudo inside a
container, for example) has to run on a host with `docker_no_new_privileges: false`.

Docker's repository is added to unattended-upgrades, on the schedule `base` configures. An
upgrade restarts dockerd, which restarts every container, including Swarm services.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `docker_no_new_privileges` | `true` | Set `no-new-privileges` on every container; `false` leaves Docker's default (off) |
| `docker_unattended_upgrades` | `true` | Let unattended-upgrades install updates from Docker's repository; `false` removes that opt-in |
| `docker_daemon_config` | `{}` | Further `daemon.json` settings, merged over the role's `log-driver` and `no-new-privileges` |
