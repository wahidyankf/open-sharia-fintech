# beavernest-be — Gherkin

Behavioral scenarios for the `beavernest-be` F#/Giraffe REST API, organized by domain.

## Feature Files

- [health/liveness.feature](./health/liveness.feature) — liveness without persistence detail
- [health/readiness-ready.feature](./health/readiness-ready.feature) — ready database state
- [health/readiness-unready.feature](./health/readiness-unready.feature) — safe unavailable state
- [routing/greeting-retirement.feature](./routing/greeting-retirement.feature) — retired greeting
  route returns 404
- [routing/missing-asset.feature](./routing/missing-asset.feature) — missing static assets do not
  return the application shell
- [routing/spa-fallback.feature](./routing/spa-fallback.feature) — dotless client routes return the
  application shell
- [routing/unknown-api.feature](./routing/unknown-api.feature) — unmatched API paths return JSON
  errors
- [development/development-data-isolation.feature](./development/development-data-isolation.feature) — local
  development uses an explicit isolated SQLite directory
- [persistence/](./persistence/) — migration and SQLite safety behavior
- [recovery/](./recovery/) — verified online backup and restore behavior
- [configuration/env-tier-loading.feature](./configuration/env-tier-loading.feature) — tiered
  `.env.<APP_ENV>` loading at startup

Derived from the current BeaverNest foundation behavior contract.

## Related

- [behavior/README.md](../../README.md) — behavior index
- [../../../containers/contracts/](../../../containers/contracts/README.md) — the OpenAPI
- [configuration — beavernest-be Gherkin Domain](./configuration/README.md)
  contract these scenarios exercise
