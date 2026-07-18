# Database Copy Down (DBCD)

Moves database dumps from a production server to its consumers over restricted rsync:
the client pushes dumps to the server, and consumers pull them down. A host can take
any combination of the three modes via `dbcd_modes`.

- **server** — serves the dump. Write-only rsync access for the client and read-only
  rsync access for the consumers, both via the `dbcd_server_user` account. Installs
  `rsync` (which provides `rrsync`) and ensures the `ssh-users` group exists.
- **client** — sends the database dump to the server.
- **consumer** — logs in to the server to rsync the dump down.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `dbcd_modes` | `[]` | Modes to configure on the host: any of `server`, `client`, `consumer` |
| `dbcd_server_user` | `dbcd` | Account on the server that clients and consumers connect as |
| `dbcd_data_dir` | `/home/{{ dbcd_server_user }}/data` | Directory on the server that holds the dumps |

The remaining variables have no defaults and are required by the modes below.

### server

| Variable | Description |
|----------|-------------|
| `dbcd_server_client_public_key` | Public key granted write-only access, used by the client |
| `dbcd_server_consumer_public_keys` | List of public keys granted read-only access, used by consumers |

### client

| Variable | Description |
|----------|-------------|
| `dbcd_client_user` | Username that sends dumps to the server |
| `dbcd_client_private_key` | Private key with write access to the server |
| `dbcd_server_host` | Server hostname |
| `dbcd_known_hosts` | List of known-hosts entries for the server, needed for automation |

### consumer

| Variable | Description |
|----------|-------------|
| `dbcd_consumer_user` | Local user that pulls dumps (gets the `dbcd-server-r` SSH host alias) |
| `dbcd_server_host` | Server hostname |
| `dbcd_known_hosts` | List of known-hosts entries for the server, needed for automation |
