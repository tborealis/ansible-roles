# symfony_params

Writes a Symfony `parameters.yaml` from a consumer-supplied template.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `symfony_params_template` | — | Template filename to render; the role no-ops when unset |
| `symfony_params_file_path` | — (required when the template is set) | Directory the parameters file is written to (created `0750`) |
| `symfony_params_file_user` | — (required when the template is set) | Owner of the directory and file |
| `symfony_params_file_group` | — (required when the template is set) | Group of the directory and file |

## Templates

`symfony_params_template` is resolved relative to the consuming playbook, so
the template must live next to it in `templates/symfony-params/`. It is
rendered to `{{ symfony_params_file_path }}/parameters.yaml`. See this role's
molecule scenario (`molecule/default/templates/`) for a working example.
