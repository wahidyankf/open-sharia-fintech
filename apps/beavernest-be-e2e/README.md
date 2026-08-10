# beavernest-be-e2e

Playwright-BDD backend E2E tests for beavernest-be.

## Quick Start

1. Start the stack: `npm run beavernest:dev` (or let `scripts/run-e2e.sh` do it for you)
2. Run E2E: `nx run beavernest-be-e2e:test:e2e`

When `API_BASE_URL` is set, the E2E runner reuses that existing backend instead of starting a second
Compose stack. This is required by the full-stack CI workflow.

## Commands

| Command                                       | Description                    |
| --------------------------------------------- | ------------------------------ |
| `nx run beavernest-be-e2e:test:e2e`           | Run BE E2E tests headlessly    |
| `nx run beavernest-be-e2e:test:e2e:ui`        | Run with interactive UI        |
| `nx run beavernest-be-e2e:test:e2e:report`    | View HTML report               |
| `nx run beavernest-be-e2e:specs:e2e:coverage` | Check Gherkin scenario binding |

## Feature Files

The behavior source of truth is
[the BeaverNest backend Gherkin suite](../../specs/apps/beavernest/behavior/beavernest-be/gherkin/README.md).
