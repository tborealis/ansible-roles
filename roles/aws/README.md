# AWS CLI and per-user config

Installs the AWS CLI v2 from AWS's official archive — signature-verified against the
AWS CLI signing key shipped with the role — plus the optional Session Manager plugin,
and writes per-user configuration (`~/.aws/config` and `~/.aws/credentials`). Set
`aws_cli_install: false` to only write configuration, e.g. on hosts that use
instance profiles or where the CLI is not needed.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `aws_config` | `[]` | Per-user configuration; see below |
| `aws_cli_install` | `true` | Install the AWS CLI (and, with `aws_cli_ssm_install`, the Session Manager plugin); when `false` only per-user config is written |
| `aws_cli_version` | See defaults | AWS CLI v2 version to install; the versioned archive is downloaded and its GPG signature verified |
| `aws_cli_download_path` | `/var/tmp` | Working directory for downloads; must be exec-mounted because the AWS installer runs from it |
| `aws_cli_ssm_install` | `true` | Also install the AWS Session Manager plugin (only alongside the CLI) |
| `aws_cli_ssm_version` | See defaults | Session Manager plugin version |
| `aws_cli_ssm_checksums` | See defaults | sha256 checksums of the plugin deb per architecture key (`ubuntu_64bit`, `ubuntu_arm64`) |

## Per-user configuration

Each `aws_config` item configures one user's `~/.aws`:

```yaml
aws_config:
  - user: user1
    profiles:
      - name: default
        region: eu-west-1
        output: json
        access_key_id: ABCDE
        secret_access_key: EDCBA
      - name: assumed
        region: eu-west-2
        role_arn: arn:aws:iam::123456789012:role/example
        source_profile: default
```

`name` is required. `access_key_id`/`secret_access_key` (set both or neither) go
into `~/.aws/credentials`; every other key is rendered verbatim into
`~/.aws/config` (`region`, `output`, `role_arn`, `source_profile`, `sso_*`, …),
so quote values that YAML would otherwise type-cast (booleans render as
`True`/`False` unquoted). The credentials file is always written — empty when no
profile carries keys — so keys removed from a profile are scrubbed on the next
converge. Top-level `[sso-session]` sections are not modelled.

## Updating

Bump `aws_cli_version` freely — every archive version is signed with the same AWS CLI
key, so no checksum maintenance is needed. When bumping `aws_cli_ssm_version`, update
both entries in `aws_cli_ssm_checksums` from the corresponding
`https://s3.amazonaws.com/session-manager-downloads/plugin/<version>/<arch>/session-manager-plugin.deb`
files.

The signing key in `files/aws-cli-signing-key.asc` (fingerprint
`FB5D B77F D5C1 18B8 0511 ADA8 A631 0ACC 4672 475C`) is periodically re-issued by AWS
with an extended expiry; refresh it from
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html when it
nears expiry (currently 2027-07-01). An expired key fails the install loudly
(`GOODSIG` is required, `EXPKEYSIG` is rejected).
