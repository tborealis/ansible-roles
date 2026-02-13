# ssl

Manages SSL certificates and keys.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ssl_certs` | `[]` | SSL certificates to install |
| `ssl_keys` | `[]` | SSL private keys to install |
| `ssl_stapling` | `[]` | OCSP stapling configurations |
| `ssl_skip_dh` | `false` | Skip DH parameters generation |
