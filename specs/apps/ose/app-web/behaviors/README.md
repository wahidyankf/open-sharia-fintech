# OSE Application Web — Gherkin Scenarios

Frontend (UI-semantic) Gherkin scenarios for `ose-app-web`. The `smoke` domain is consumed by
Playwright-BDD (`apps/ose-app-web-e2e`); the `env-loader` domain is consumed by
`@amiceli/vitest-cucumber` unit tests (`apps/ose-app-web/test/unit`).

## Feature files

| Feature file                                                     | Domain     |
| ---------------------------------------------------------------- | ---------- |
| [smoke/smoke.feature](./smoke/smoke.feature)                     | smoke      |
| [env-loader/env-loader.feature](./env-loader/env-loader.feature) | env-loader |

- [env-loader — OSE Application Web Gherkin Domain](./env-loader/README.md)
- [smoke — app-web Gherkin Domain](./smoke/README.md)
