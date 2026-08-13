# beavernest-app-e2e

Playwright-BDD browser E2E tests for the Flutter Web bundle served by the same-origin combined
BeaverNest runtime.

## Quick Start

1. Start the stack: `docker compose -f infra/dev/beavernest-app/docker-compose.yml up -d`
2. Run E2E: `nx run beavernest-app-e2e:test:e2e`

## Commands

| Command                                        | Description                             |
| ---------------------------------------------- | --------------------------------------- |
| `nx run beavernest-app-e2e:test:e2e`           | Run hosted Flutter E2E tests headlessly |
| `nx run beavernest-app-e2e:test:e2e:ui`        | Run with interactive UI                 |
| `nx run beavernest-app-e2e:test:e2e:report`    | View HTML report                        |
| `nx run beavernest-app-e2e:specs:e2e:coverage` | Check Gherkin scenario binding          |

## Feature Files

- [cache-update.feature](../../specs/apps/beavernest/behavior/beavernest-app/gherkin/cache/cache-update.feature)
