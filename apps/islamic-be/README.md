# islamic-be

Backend service for the OSE Islamic tools domain. Go 1.26 on [Gin](https://gin-gonic.com/),
serving a single health endpoint.

This is a deliberately small first slice: the service exists so that the Go lane, the specification
corpus, and the deployment shape are all real and gated before any domain logic lands.

## Behaviour corpus

The canonical Gherkin lives in
[`specs/apps/islamic/be/behaviours/`](../../specs/apps/islamic/be/behaviours/) and is never copied
into this project — the tests read it in place, so the two cannot drift.

| Folder                                                      | Scenarios | What it covers                          |
| ----------------------------------------------------------- | --------- | --------------------------------------- |
| [`health/`](../../specs/apps/islamic/be/behaviours/health/) | 3         | Status, content type, unknown-route 404 |
| [`config/`](../../specs/apps/islamic/be/behaviours/config/) | 5         | Listener-port resolution order          |

The HTTP contract is [`specs/apps/islamic/be/contracts/openapi.yaml`](../../specs/apps/islamic/be/contracts/openapi.yaml),
owned by the `islamic-contracts` project. `codegen` generates the Gin `ServerInterface` from it, and
`internal/router` implements that interface — so an operation added to the contract fails
compilation until it is served, rather than returning 404 at runtime.

## Test adapters

| Layer       | Owner                                   | Status                                   |
| ----------- | --------------------------------------- | ---------------------------------------- |
| Unit        | `internal/bdd` + co-located `*_test.go` | Mandatory. 100% line coverage, 99% floor |
| Integration | —                                       | **Omitted.** See below                   |
| E2E         | `islamic-be-e2e`                        | Owns the health scenarios over real HTTP |

### Why there is no `test:integration`

Integration proof exists to cover a real _local-resource_ boundary — a database, an embedded store,
the filesystem, a child process, an owned loopback socket. `islamic-be` has none. It holds no
persistent state, starts no subprocess, and reads nothing from disk at runtime.

Its only two boundaries are an HTTP surface, which is a network boundary that belongs to E2E, and
the process environment, which port resolution takes as an injected `Lookup` rather than reading
directly. An Integration target here would either duplicate the Unit tests or bind a real socket
that E2E already covers.

Per the [BDD contract](../../repo-governance/development/behaviour-driven-development.md), an
inapplicable target is omitted and explained rather than stubbed. No echo target, no success
sentinel.

## Targets

```bash
npx nx run islamic-be:dev          # serve on 8402
npx nx run islamic-be:test:quick   # typecheck, lint, unit + coverage floor, specs, validators
npx nx run islamic-be:lint         # golangci-lint (v2 schema)
npx nx run islamic-be:build        # dist/islamic-be
npx nx run islamic-be:codegen      # regenerate the contract types
```

`test:unit` enforces a 99% line-coverage floor over `./internal/...` via
[`scripts/coverage-gate.sh`](./scripts/coverage-gate.sh). `cmd/islamic-be` is excluded because it
only binds a socket and reads the environment — the boundaries Unit proof may not touch — and
`generated-contracts` is excluded because it is generated, not authored.

`compat:min-version` is a real assertion that `go.mod`'s `go` directive still matches the pinned
floor, not an echo.

## Configuration

| Variable          | Default | Notes                                                |
| ----------------- | ------- | ---------------------------------------------------- |
| `ISLAMIC_BE_PORT` | `8402`  | `--port` flag wins over it; a bare `PORT` is ignored |

A malformed value fails startup rather than falling back to the default, so a typo surfaces
immediately instead of as traffic on the wrong port. A bare `PORT` is deliberately ignored: one
exported variable must not retarget every app in the monorepo at once.

Copy [`.env.example`](./.env.example) to `.env.local` for local overrides. Never commit a real one.

## Running in Docker

```bash
npx nx run islamic-be:codegen   # the image build needs the generated types
docker compose -f ../../infra/dev/islamic-be/docker-compose.yml up --build
```

The runtime stage is `scratch` — a static binary and nothing else. It carries no CA certificates
because the service makes no outbound TLS calls; add them the moment it does.

## See also

- [Specification corpus](../../specs/apps/islamic/be/README.md) — behaviours, contract, architecture
- `apps/islamic-be-e2e` — the E2E suite for this service. Named rather than linked until DU4
  creates it; `md-links` scans the whole tree, so a forward link would fail every push.
