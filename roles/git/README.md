# git

Installs Git and configures SSH known hosts for common Git providers.

It also marks GitHub's RSA host key from before March 2023, which GitHub replaced
after its private key was exposed, as `@revoked` in `/etc/ssh/ssh_known_hosts`, and
removes any system entry that trusts it (older versions of this role added one). ssh
then refuses that key even where a user's own `known_hosts` still lists it.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `git_known_hosts` | GitHub keys | SSH known hosts entries for Git providers |
| `git_rewrite_deprecated_protocol` | `true` | Rewrite git:// URLs to https:// |
| `git_use_backports` | `true` on bookworm | Install Git from the backports repository |
