# BeaverNest Combined Runtime

The production topology has one `beavernest-app` service. It serves the Flutter Web client and API
from one ASP.NET origin on container port `19300`; no separate frontend or backend host port exists.

## Start

Create a value-only operator environment file from `apps/beavernest-be/.env.example`, prepare
separate `0700` data and backup directories, then run:

```bash
bash infra/dev/beavernest-app/scripts/start.sh --env-file /absolute/path/operator.env
```

The wrapper runs fail-closed preflight before Compose. Exact host-address binding is the application
guarantee; VPN admission, routing, and firewall policy remain operator-owned.

## Operations

Use `scripts/operations.sh backup --env-file PATH --name NAME.sqlite3`,
`scripts/operations.sh integrity --env-file PATH`, or the analogous `restore` command.
Restore refuses while the app is running. The backup bind is writable but not an independent failure
domain; copy validated backups to independent or off-host storage.

## Local Development

Use `npm run beavernest:dev` to build and run the same-origin combined runtime locally. It serves
the Flutter Web bundle and API on `127.0.0.1:19300`. For backend-only watch development, use
`BEAVERNEST_BE_DEVELOPMENT_DATA_DIRECTORY=/absolute/path npm exec nx dev beavernest-be`, which
starts the API on `127.0.0.1:19320`.
