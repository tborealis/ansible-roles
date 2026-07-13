# Testing

Roles are tested with [Molecule](https://ansible.readthedocs.io/projects/molecule/)
using the Docker driver. Each role's scenario converges the role in a
systemd-enabled Debian container, checks idempotence (a second converge must
report no changes), and runs functional verification — real client probes
(log in to MySQL, curl nginx) and config-content assertions, not just
"package installed" checks.

Tests run against both supported releases, **bookworm** and **trixie**, using
images built from [`docker/molecule-debian/Dockerfile`](../docker/molecule-debian/Dockerfile)
and published to `ghcr.io/tborealis/ansible-roles/molecule-debian:<release>`.

## Local setup

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
ansible-galaxy install -r requirements.yml
```

Then run a role's tests:

```sh
make test ROLE=mysql                  # both releases
make test ROLE=mysql DISTRO=bookworm  # one release
```

The `test` target symlinks the repo into
`~/.ansible/collections/ansible_collections/tborealis/roles` so converge
playbooks resolve `tborealis.roles.<name>` FQCNs (and their `apt_keys` meta
dependencies) against your working tree.

Images are pulled from GHCR automatically; to build them locally instead (for
example while changing the Dockerfile) run `make test-images`. Forks can point
at another registry with `MOLECULE_IMAGE_REPO=ghcr.io/you/your-fork`.

## Debugging a scenario

From `roles/<role>`:

```sh
molecule converge   # create + converge, leaves the container running
molecule login      # shell into the container
molecule verify     # re-run verification against the running container
molecule destroy
```

Platform names are fixed (`bookworm`, `trixie`), so two roles cannot run
molecule at the same time on one machine — the container names clash.

## Writing a scenario

Every role must ship `molecule/default/` containing:

- `molecule.yml` — usually just a comment; it inherits the shared base config
  at [`.config/molecule/config.yml`](../.config/molecule/config.yml). Dicts
  deep-merge, **lists replace**, so a role restricted to one release redefines
  `platforms:` entirely (copy the flags from the base config — see
  `roles/rabbitmq/molecule/default/molecule.yml`) and must also be added to
  [`.config/molecule/platforms.yml`](../.config/molecule/platforms.yml) so CI
  skips the excluded release.
- `converge.yml` — applies the role by FQCN (`tborealis.roles.<name>`) with
  `become: true`. Roles that do nothing with default variables must be
  converged with realistic test values. Values shared between converge and
  verify (passwords, paths) go in a `vars.yml` loaded with `vars_files`;
  fixture templates go in `molecule/default/templates/`. Use throwaway
  secrets with a realistic shape, never real ones.
- `verify.yml` — functional assertions:
  - service roles: `service_facts` + assert the service is running, a real
    client probe (curl, mysql login, `redis-cli ping`), and at least one
    config-content assertion (`slurp` + `assert` on a value converge set)
  - tool roles: run the binary and assert on its output (when the binary has
    a same-named module, tag the task
    `# noqa: command-instead-of-module` — the point is exercising the binary)
  - config roles: `stat` for owner/mode, `slurp` + `assert` for content, and
    native validators where they exist (`visudo -c`, `php-fpm -t`)
- `prepare.yml` — only for prerequisites outside the role's contract (e.g.
  installing PHP before testing `php_fpm`). Never prepare things the role
  should do itself.

Idempotence must pass: prefer fixing a non-idempotent role over tagging tasks
`molecule-idempotence-notest`. Scenario files are linted like everything else
(`make lint`): named tasks, FQCN modules, `changed_when: false` on read-only
commands.

## CI

The `molecule` workflow runs:

- **on PRs** — only roles the PR touches. Changes to shared test
  infrastructure (`.config/molecule/`, `docker/`, requirements files, the
  workflow, `scripts/molecule_matrix.py`) run a canary set (`git`, `mysql`);
  PRs changing the Dockerfile test against an image built from their own
  branch. Roles without a `molecule/` directory are skipped.
- **weekly** (Mondays 05:00 UTC, after Sunday's image rebuild) — the full
  role × release matrix, alerting Slack on failure like `key-check`.
- **manually** — `workflow_dispatch`, optionally with a space-separated list
  of roles.
