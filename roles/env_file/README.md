# env_file

Renders `NAME=value` environment files — plain `.env` files by default, or
`export NAME=value` profile scripts (e.g. for `/etc/profile.d/`) with
`export: true`. This role replaces the removed `dotenv` and `environment`
roles — see [docs/migrating-v6.md](../../docs/migrating-v6.md).

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `env_file_list` | `[]` | List of env files to render |

Each item takes:

| Key | Default | Description |
|-----|---------|-------------|
| `file` | — (required) | Destination path; the parent directory must already exist |
| `owner` | — (required) | Owner of the file; the user must already exist |
| `group` | `owner` | Group of the file |
| `mode` | `0644` | File mode; set e.g. `"0600"` for files carrying secrets |
| `export` | `false` | Prefix every line with `export ` (for files sourced by a shell) |
| `vars` | — (required) | Mapping of `NAME: value`; names render verbatim, values are shell-quoted |

Rendered files start with an `{{ ansible_managed }}` comment header.

```yaml
env_file_list:
  - file: /opt/app/.env
    owner: app
    mode: "0600"
    vars:
      APP_ENV: production
      DATABASE_URL: pgsql://…
  - file: /etc/profile.d/app.sh
    owner: root
    export: true
    vars:
      APP_ENV: production
```
