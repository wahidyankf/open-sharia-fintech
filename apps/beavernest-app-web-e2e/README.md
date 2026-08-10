# beavernest-app-web-e2e

Playwright-BDD frontend E2E tests for the same-origin BeaverNest workspace. The combined runtime is
introduced in Phase 5; direct viewport tests start Vite locally and fixture readiness with
`page.route()`.

## Quick Start

1. Start the stack: `docker compose -f infra/dev/beavernest-app/docker-compose.yml up -d`
2. Run E2E: `nx run beavernest-app-web-e2e:test:e2e`

## Commands

| Command                                                                                          | Description                          |
| ------------------------------------------------------------------------------------------------ | ------------------------------------ |
| `nx run beavernest-app-web-e2e:test:e2e`                                                         | Run FE E2E tests headlessly          |
| `nx run beavernest-app-web-e2e:test:e2e:ui`                                                      | Run with interactive UI              |
| `nx run beavernest-app-web-e2e:test:e2e:report`                                                  | View HTML report                     |
| `nx run beavernest-app-web-e2e:specs:e2e:coverage`                                               | Check Gherkin scenario binding       |
| `npm exec -- playwright test --config apps/beavernest-app-web-e2e/playwright.viewport.config.ts` | Check Vite at the required viewports |

## Feature Files

- [browser-readiness.feature](../../specs/apps/beavernest/behavior/beavernest-app-web/gherkin/workspace/browser-readiness.feature)
- [readiness-loading.feature](../../specs/apps/beavernest/behavior/beavernest-app-web/gherkin/workspace/readiness-loading.feature)
- [readiness-recovery.feature](../../specs/apps/beavernest/behavior/beavernest-app-web/gherkin/network/readiness-recovery.feature)
- [no-promotional-cta.feature](../../specs/apps/beavernest/behavior/beavernest-app-web/gherkin/workspace/no-promotional-cta.feature)
