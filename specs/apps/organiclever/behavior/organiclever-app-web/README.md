# organiclever-app-web — Behavior Surface

UI-semantic Gherkin scenarios for the OrganicLever app frontend (Next.js 16).

## Contents

- **[gherkin/](./gherkin/README.md)** — Feature files organized by feature context.
  Consumed by `apps/organiclever-app-web-e2e` (Playwright FE E2E).

## Background step

All scenarios use: `Given the app is running`

## Domains

- **app-shell/** — Navigation chrome and entry-logging overlays
- **env-loader/** — `APP_ENV` tier env-file loader scenarios (build-time tooling)
- **health/** — Backend connectivity status page
- **journal/** — Home screen and journal entry mechanism
- **routine/** — Workout routine management
- **routing/** — URL scheme and disabled-route guards
- **settings/** — User preferences (dark mode, language)
- **stats/** — History and progress screens
- **workout-session/** — Active workout session FSM

## Related

- [Parent behavior README](../README.md)
- [Gherkin specs](./gherkin/README.md)
- [Component specs](../../components/app-web/README.md)
