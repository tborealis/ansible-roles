# chrome

Installs Google Chrome and optionally ChromeDriver from
[Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/), unpacked
under `/opt/chrome` and `/opt/chromedriver` and linked as
`/usr/local/bin/google-chrome` and `/usr/local/bin/chromedriver`. Only the x86_64
build is installed.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `chrome_version` | `stable` | Release channel (`stable`, `beta`, `dev`, `canary`), major milestone (e.g. `127`) or exact version to install |
| `chrome_chromedriver_version` | `{{ chrome_version }}` | ChromeDriver channel, major milestone or exact version to install |
| `chrome_install_chromedriver` | `false` | Whether to install ChromeDriver |
| `chrome_remove_system_chrome` | `false` | Remove system-installed Chrome first |
| `chrome_system_dependencies` | See defaults | System dependencies for Chrome (packages renamed per Debian release are appended automatically) |
