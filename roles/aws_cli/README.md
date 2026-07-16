# AWS CLI with config

Installs the AWS CLI v2 from AWS's official archive — signature-verified against the
AWS CLI signing key shipped with the role — plus the optional Session Manager plugin,
and configures per-user credentials.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `aws_cli_config` | `[]` | Per-user configuration (keys: `user`, `default_region`, `access_key_id`, `secret_access_key`) |
| `aws_cli_version` | See defaults | AWS CLI v2 version to install; the versioned archive is downloaded and its GPG signature verified |
| `aws_cli_download_path` | `/var/tmp` | Working directory for downloads; must be exec-mounted because the AWS installer runs from it |
| `aws_cli_ssm_install` | `true` | Also install the AWS Session Manager plugin |
| `aws_cli_ssm_version` | See defaults | Session Manager plugin version |
| `aws_cli_ssm_checksums` | See defaults | sha256 checksums of the plugin deb per architecture key (`ubuntu_64bit`, `ubuntu_arm64`) |

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
