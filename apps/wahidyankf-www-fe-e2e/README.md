# wahidyankf-www-fe-e2e

End-to-end tests for [`apps/wahidyankf-www`](../wahidyankf-www/) using
Playwright and `playwright-bdd`. Consumes the Gherkin feature files at
`specs/apps/wahidyankf/fe/gherkin/` shared with the FE unit tests.

## Commands

```bash
# Install Chromium for Playwright
nx run wahidyankf-www-fe-e2e:install

# Build a fresh production Docker image, wait for its health check, and run all E2E scenarios
nx run wahidyankf-www-fe-e2e:test:e2e

# Run with Playwright UI
nx run wahidyankf-www-fe-e2e:test:e2e:ui

# View last run report
nx run wahidyankf-www-fe-e2e:test:e2e:report

# Pre-push quick gate (typecheck + lint; e2e runs nightly / on demand)
nx run wahidyankf-www-fe-e2e:test:quick
```

## Features consumed

- `home.feature`
- `search.feature`
- `cv.feature`
- `theme.feature`
- `personal-projects.feature`
- `responsive.feature`
- `accessibility.feature` — E2E-only, axe-core-driven
- `static-filterable-routes.feature` — production-container route and crawler checks

## Default base URL

The regular E2E command builds a fresh production Docker image, starts an isolated container on an
ephemeral loopback port, waits for its health check, then supplies that URL to Playwright. It never
reuses a checkout server.

Set `BASE_URL` only to run the same suite against an already-running staging or production deployment:

```bash
BASE_URL=https://example.com nx run wahidyankf-www-fe-e2e:test:e2e
```
