# AGENTS Configuration

## Scope
This configuration applies to the entire repository.

## Testing
Install `ansible-dev-tools` with `pipx`, which includes `ansible` and `ansible-lint`:

```
pipx install --include-deps ansible-dev-tools
```

Install collection dependencies listed in `requirements.yml`:

```
ansible-galaxy collection install -r requirements.yml
```

Run `ansible-lint` before committing changes. If Docker is available you can also run `make lint` which uses the official ansible-lint container.

## YAML style
Use two-space indentation for YAML and Ansible files.

## Commit messages
Write concise commit messages describing why the change is made.

