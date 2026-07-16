Writes per-user AWS CLI configuration (`~/.aws/config` and `~/.aws/credentials`).
The role deliberately does **not** install the AWS CLI and has no dependency on
the `aws_cli` role — apply `aws_cli` yourself where the binary is needed.

# Config example

```yaml
aws_config:
- user: user1
  profiles:
  - name: default
    region: eu-west-1
    access_key_id: ABCDE
    secret_access_key: EDCBA
  - name: backup
    region: eu-west-2
    access_key_id: ABCDE
    secret_access_key: EDCBA
```
