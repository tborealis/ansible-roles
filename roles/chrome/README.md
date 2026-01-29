# chrome

Installs Google Chrome and optionally ChromeDriver using Puppeteer's browser installer.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `chrome_version` | `stable` | Chrome version to install |
| `chrome_chromedriver_version` | `{{ chrome_version }}` | ChromeDriver version to install |
| `chrome_install_chromedriver` | `false` | Whether to install ChromeDriver |
| `chrome_remove_system_chrome` | `false` | Remove system-installed Chrome first |
| `chrome_system_dependencies` | See defaults | System dependencies for Chrome |
