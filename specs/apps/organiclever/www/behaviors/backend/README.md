# organiclever-www-be Gherkin Specs

Placeholder gherkin directory for the `organiclever-www` backend E2E slot.

## Background

`organiclever-www` is a pure Next.js static marketing site with no tRPC route
handlers or dedicated backend API. There are no real backend scenarios to cover.

This directory exists to satisfy the standardized `{app}-be-e2e` +
`{app}-fe-e2e` reusable workflow pair. The `organiclever-www-be-e2e` project
is tolerated-absent in CI (called with `|| true`).

## Structure

```
specs/apps/organiclever/www/behaviors/backend/
└── placeholder/
    └── placeholder.feature   # Structural placeholder — no real scenarios
```

## Consumed by

- **E2E**: `apps/organiclever-www-be-e2e/src/steps/` via `playwright-bdd`

## Related

- **FE counterpart**: [organiclever-www behavior specs](../frontend/README.md)
- **Parent**: [behavior specs](../../README.md)
