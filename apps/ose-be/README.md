# OSE application backend

`ose-be` is the API backend for the OSE application: a product being built to help compliance and
risk teams compare regulator-published rules with their internal policies. It is an early-stage F#
service. Today, it provides a reliable starting point—database migration, service health, bounded
context status, and messaging status—while the document-ingestion and gap-analysis workflows are
still being developed.

## Start it locally

From the repository root, install the workspace dependencies and make sure the .NET 10 SDK is
available. Docker is needed for the local PostgreSQL and NATS services used below.

```bash
npm install
docker compose -f apps/ose-be/docker-compose.e2e.yml up -d

export DATABASE_URL='Host=localhost;Port=5432;Database=ose_app;Username=postgres;Password=postgres'
export ASPNETCORE_URLS='http://localhost:8302'

npm exec nx -- run ose-be:codegen
npm exec nx -- run ose-be:dev
```

The sample connection string is only for the local Docker services defined in this repository. The
service applies pending database migrations when it starts. In another terminal, confirm that it is
running:

```bash
curl http://localhost:8302/api/v1/health
```

Expected response:

```json
{ "status": "healthy" }
```

Stop the local services when finished:

```bash
docker compose -f apps/ose-be/docker-compose.e2e.yml down
```

## What is available today

The first product goal is AI-assisted gap analysis between regulatory documents and internal policy
documents. The backend is organized around the parts of that future workflow, but most product
operations are not exposed as public API operations yet.

| Area               | Current surface                                                                 |
| ------------------ | ------------------------------------------------------------------------------- |
| Service health     | `GET /api/v1/health` returns the service liveness status.                       |
| Regulatory sources | `GET /api/v1/regulatory-source/status` reports the context's current readiness. |
| Internal policies  | `GET /api/v1/internal-policy/status` reports the context's current readiness.   |
| Gap analysis       | `GET /api/v1/gap-analysis/status` reports the context's current readiness.      |
| AI orchestration   | `GET /api/v1/ai-orchestration/status` reports the context's current readiness.  |
| Messaging          | `GET /api/v1/system/status/messaging` reports the JetStream startup outcome.    |

The [OpenAPI contract](../../specs/apps/ose/be/contracts/openapi.yaml) is the source of
truth for API operations. At present, it formally defines the health endpoint; the status routes
are useful development surfaces while the product contract expands.

## Configuration and dependencies

The service reads configuration from process environment variables.

- `DATABASE_URL` is required. It must be a PostgreSQL connection string accepted by Npgsql.
- `ASPNETCORE_URLS` controls the listening address. The local command above binds to port `8302`.
- `OSE_BE_NATS_URL` is required; startup aborts with a clear error if it is unset. Once configured,
  connecting to NATS itself is attempted best-effort at startup — if the broker is unavailable, the
  HTTP service still starts and the messaging-status endpoint records the outcome.
- OpenRouter settings are optional. They enable the in-progress AI integration and must be supplied
  through your local environment, never committed to the repository.

PostgreSQL stores the emerging regulatory and policy document data. NATS with JetStream is used for
the current messaging demonstration. The service uses automatic migrations on startup, so use a
dedicated database for local development.

## How the code is arranged

The service uses F# on ASP.NET Core with Giraffe, PostgreSQL through EF Core and Npgsql, DbUp
migrations, and NATS. Each bounded context follows a small hexagonal slice:

```text
Contexts/<context>/
├── Domain/          business language and types
├── Application/     use cases
├── Infrastructure/  database or external adapters
└── Api/             HTTP route and response handling
```

Useful starting points:

- [`src/OseBe/Program.fs`](./src/OseBe/Program.fs) composes configuration, migrations, messaging,
  and the HTTP host.
- [`src/OseBe/WebApp.fs`](./src/OseBe/WebApp.fs) brings the bounded-context routes together.
- [`db/migrations/`](./db/migrations/) contains the embedded PostgreSQL migrations.
- [`specs/apps/ose/`](../../specs/apps/ose/README.md) contains the product, behavior, and contract
  specifications.

## Common commands

Run these from the repository root.

| Command                                      | Use it for                                                                  |
| -------------------------------------------- | --------------------------------------------------------------------------- |
| `npm exec nx -- run ose-be:codegen`          | Generate F# contract types from the bundled OpenAPI specification.          |
| `npm exec nx -- run ose-be:dev`              | Run the backend with file watching.                                         |
| `npm exec nx -- run ose-be:build`            | Produce the release build.                                                  |
| `npm exec nx -- run ose-be:typecheck`        | Compile and type-check the F# service.                                      |
| `npm exec nx -- run ose-be:lint`             | Run formatting and strict F# analysis.                                      |
| `npm exec nx -- run ose-be:test:unit`        | Run the fast F# unit tests.                                                 |
| `npm exec nx -- run ose-be:test:integration` | Test migrations and repositories against a temporary PostgreSQL container.  |
| `npm exec nx -- run ose-be:test:quick`       | Run the backend's focused quality gate, including specs coverage.           |
| `npm exec nx -- run ose-be-e2e:test:e2e`     | Run the separate Playwright backend end-to-end suite with local containers. |

For the backend's expected behavior, see the
[Gherkin scenarios](../../specs/apps/ose/be/behaviors/README.md). For the broader product
direction, see the [OSE application overview](../../specs/apps/ose/overview.md).
