# gpg

Installs GnuPG and imports per-user private and public keys, setting owner trust on
the public keys. Keys already present in the user's keyring are left untouched.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `gpg_config` | `[]` | Per-user keys to import; see below |

## Per-user configuration

Each `gpg_config` item manages one user's `~/.gnupg`:

```yaml
gpg_config:
  - user: deploy              # unix username
    private_keys:
      - id: <full key id>
        key: <base64-encoded armoured key>
        passphrase: <key passphrase>
    public_keys:
      - id: <full key id>
        key: <base64-encoded armoured key>
        owner_trust_level: 5  # owner trust (see `man gpg2`; 5 = ultimately trusted)
```
