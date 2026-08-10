# BeaverNest — Behavior

Cross-cutting Gherkin scenarios for the BeaverNest foundation, covering both C4 L2 containers.

## Structure

```
behavior/
├── beavernest-be/gherkin/    # 15 feature files — health, routing, persistence, development, recovery
│   ├── health/                # liveness, readiness-ready, readiness-unready
│   ├── routing/                # greeting-retirement, missing-asset, spa-fallback, unknown-api
│   ├── persistence/            # migration and SQLite safety behavior
│   ├── development/            # local data-directory isolation
│   └── recovery/                # verified online backup and restore
└── beavernest-app-web/gherkin/    # 4 feature files
    ├── workspace/                # browser-readiness, readiness-loading, no-promotional-cta
    └── network/                   # readiness-recovery
```

19 feature files, 19 scenarios total.

## Surfaces

- [beavernest-be/gherkin/](./beavernest-be/gherkin/README.md) — backend liveness/readiness, routing
  (including the retired `/api/v1/hello` route returning 404), SQLite persistence, and backup/restore
- [beavernest-app-web/gherkin/](./beavernest-app-web/gherkin/README.md) — foundation-status readiness
  panel content, loading state, and network recovery

## Running the Tests

```bash
npx nx run rhino-cli:specs:structure-validation
```

## Related

- [../containers/](../containers/README.md) — C4 L2, hosts the OpenAPI contract these scenarios
  exercise
- [../system-context/](../system-context/README.md) — C4 L1
