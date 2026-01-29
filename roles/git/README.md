# git

Installs Git and configures SSH known hosts for common Git providers.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `git_known_hosts` | GitHub keys | SSH known hosts entries for Git providers |
| `git_rewrite_deprecated_protocol` | `true` | Rewrite git:// URLs to https:// |
