# base_minimal

Minimal base system configuration with locales, timezone, and essential packages. A lighter alternative to the `base` role.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `system_locales` | `["en_US.UTF-8", "en_GB.UTF-8"]` | Locales to generate |
| `system_default_locale` | `en_GB.UTF-8` | Default system locale |
| `system_timezone` | `Europe/London` | System timezone |
| `system_packages` | `[]` | Additional packages to install |
| `base_default_system_packages` | See defaults | Essential system packages |
| `users` | `[]` | Users to create |
