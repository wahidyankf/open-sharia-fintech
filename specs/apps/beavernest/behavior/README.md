# BeaverNest — Behavior

Cross-cutting Gherkin scenarios for the BeaverNest foundation, covering both C4 L2 containers.

## Structure

```
behavior/
├── beavernest-be/gherkin/    # 16 feature files — health, routing, persistence, development, recovery, configuration
│   ├── health/                # liveness, readiness-ready, readiness-unready
│   ├── routing/                # greeting-retirement, missing-asset, spa-fallback, unknown-api
│   ├── persistence/            # migration and SQLite safety behavior
│   ├── development/            # local data-directory isolation
│   ├── recovery/                # verified online backup and restore
│   └── configuration/           # tiered .env.<APP_ENV> loading
└── beavernest-app/gherkin/        # 6 feature files
    ├── workspace/                  # same-origin Flutter Web shell and responsive readiness summary
    ├── retry/                      # readiness recovery without page reload
    ├── diagnostics/                # contract-safe operational details
    ├── browser-shortcut/           # accessible online-only browser guidance
    └── cache/                      # fresh hosted Flutter Web bundle behavior
```

21 feature files, 25 scenarios total.

## Surfaces

- [beavernest-be/gherkin/](./beavernest-be/gherkin/README.md) — backend liveness/readiness, routing
  (including the retired `/api/v1/hello` route returning 404), SQLite persistence, and backup/restore
- [beavernest-app/gherkin/](./beavernest-app/gherkin/) — Flutter Web workspace shell, readiness
  recovery, safe diagnostics, browser guidance, and cache behavior

## Running the Tests

```bash
npx nx run rhino-cli:specs:structure-validation
```

## Related

- [../containers/](../containers/README.md) — C4 L2, hosts the OpenAPI contract these scenarios
  exercise
- [../system-context/](../system-context/README.md) — C4 L1
- [Beavernest Be](./beavernest-be/README.md)
