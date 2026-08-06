# wahidyankf-www-fe-e2e

This project checks the portfolio site in a real browser: navigation, search, CV content, theme,
responsive behavior, and accessibility. It gives the public site a practical release-confidence
signal without relying on a shared development server. ✨

## Run the suite

```bash
# Install Chromium once on this machine
npm exec nx -- run wahidyankf-www-fe-e2e:install

# Build an isolated local production container and run the scenarios
npm exec nx -- run wahidyankf-www-fe-e2e:test:e2e
```

The regular test command creates its own short-lived local container and health-checks it before
Playwright starts. For interactive debugging, run
`npm exec nx -- run wahidyankf-www-fe-e2e:test:e2e:ui`; for the last report, run
`npm exec nx -- run wahidyankf-www-fe-e2e:test:e2e:report`.

## Check a deployed environment

Set `BASE_URL` only when deliberately running the suite against an already-running staging or
production site. Keep any access values out of tracked files.

## Checks and specs

```bash
npm exec nx -- run wahidyankf-www-fe-e2e:test:quick
npm exec nx -- run wahidyankf-www-fe-e2e:test:specs
```

The behavior source of truth is in
[the Wahidyankf public-site Gherkin specs](../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/README.md).
