# organiclever-www — Behavior Surface

UI-semantic Gherkin scenarios for the OrganicLever marketing website (Next.js 16).

## Contents

- **[gherkin/](./gherkin/README.md)** — Feature files organized by domain.
  Consumed by `apps/organiclever-www-fe-e2e` (Playwright FE E2E).

## Background step

All scenarios use: `Given the app is running`

## Domains

- **home/** — Marketing landing page scenarios
- **accessibility/** — Accessibility compliance scenarios
- **env-loader/** — `APP_ENV` tier env-file loader scenarios (build-time tooling)

## Related

- [Parent behavior README](../README.md)
- [Gherkin specs](./gherkin/README.md)
