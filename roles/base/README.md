# base

Base system configuration including locales, timezone, users, DNS, and essential packages.

The role does not install cron. When cron is present it is restarted after a
timezone change so scheduled jobs pick up the new zone; on images without cron
(e.g. DigitalOcean's Debian 13) the restart is skipped.

## SSH

sshd settings go in `/etc/ssh/sshd_config.d/99-custom.conf`. Debian's `sshd_config`
includes that directory before its own settings, and sshd keeps the first value it
reads, so these override the main file (but not an earlier-sorting drop-in). Logins
are limited to members of `ssh-users` and `base_ssh_extra_user_groups`.

The role restores Debian's stock `/etc/ssh/sshd_config`, which DigitalOcean's image
edits (any local changes to that file are discarded), so openssh upgrades replace it
cleanly instead of keeping a locally modified copy.

Root login is disabled by default (`PermitRootLogin no`), overriding images that
allow it, such as DigitalOcean's (`PermitRootLogin yes`). A first provision
connected as root still completes, because sshd only reloads in a handler at the
end of the play; later runs must connect as one of the managed users.

Once a managed user has an authorized key, the role also deletes
`/root/.ssh/authorized_keys`, removing keys injected at creation (DigitalOcean puts
the account's SSH keys there). The deletion also waits until the end of the play.
It is on by default only while `base_ssh_permit_root_login` is `no`, and is skipped
when `root` is one of the managed users.

## Automatic updates

The role installs `unattended-upgrades` and `needrestart`:

- Debian security updates install daily at `base_unattended_upgrades_time` (local
  time), with package lists refreshed just beforehand. Point releases and third-party
  repositories are not upgraded automatically, unless a role opts its repository in
  (the `php` and `nginx` roles add theirs).
- When a kernel update is pending, the host reboots straight after that run, unless
  `base_unattended_upgrades_reboot` is `false`. A kernel installed by hand also
  triggers the reboot on the next run.
- needrestart restarts services still running outdated binaries or libraries after
  every apt run, including unattended ones. Debian's built-in exclusions (dbus,
  systemd-logind, getty, docker, …) are only listed; they pick up the new code at the
  next reboot.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `base_system_locales` | `["en_US.UTF-8", "en_GB.UTF-8"]` | Locales to generate |
| `base_system_default_locale` | `en_GB.UTF-8` | Default system locale |
| `base_system_timezone` | `Europe/London` | System timezone |
| `base_system_packages` | `[]` | Additional packages to install |
| `base_dns_primary_nameserver` | `1.1.1.1` | Primary DNS server |
| `base_dns_secondary_nameserver` | `1.0.0.1` | Secondary DNS server |
| `base_default_users` | `[]` | Default users to create |
| `base_users` | `[]` | Additional users to create |
| `base_local_hostnames` | `[]` | Local hostname entries |
| `base_known_hosts` | `[]` | SSH known hosts entries |
| `base_ssh_extra_user_groups` | `[]` | Extra groups for SSH users |
| `base_ssh_allow_tcp_forwarding` | `false` | Allow SSH TCP forwarding |
| `base_ssh_allow_stream_local_forwarding` | `false` | Allow SSH Unix-domain socket forwarding (agent forwarding is separate and unaffected) |
| `base_ssh_permit_root_login` | `"no"` | sshd `PermitRootLogin` value (`no`, `prohibit-password`, `forced-commands-only` or `yes`); quote it so YAML keeps it a string |
| `base_ssh_password_authentication` | `false` | Allow SSH password authentication |
| `base_ssh_client_alive_interval` | `120` | Seconds between sshd keepalive probes to idle clients (`0` disables) |
| `base_ssh_clear_root_authorized_keys` | `true` while root login is `no` | Delete `/root/.ssh/authorized_keys` once a managed user has an authorized key |
| `base_default_system_packages` | See defaults | Essential system packages |
| `base_profile_config` | `[]` | Profile configuration entries |
| `base_hosts_unsafe_writes` | `false` | Write /etc/hosts in place (for containers, where the bind mount breaks atomic renames) |
| `base_use_backports` | `true` on bookworm | Configure the backports repository and install openssh-server from it |
| `base_config_dhclient` | `true` on bookworm | Template /etc/dhcp/dhclient.conf to prepend the configured DNS servers |
| `base_unattended_upgrades_time` | `04:00` | Local time (`HH:MM`) of the daily unattended upgrade run; reboots happen in the same slot |
| `base_unattended_upgrades_reboot` | `true` | Reboot after the run when an installed kernel update is pending |
