# ose-app-web-e2e

This project checks the OSE product web app through the same browser journeys a user takes. It turns
the app’s Gherkin examples into Playwright-BDD scenarios. 🚦

## Run locally

```bash
# Install Chromium once on this machine
npm exec nx -- run ose-app-web-e2e:install

# Start the app and the API it relies on
npm exec nx -- run ose-app-web:dev
npm exec nx -- run ose-be:dev

# In another terminal, run the browser scenarios
npm exec nx -- run ose-app-web-e2e:test:e2e
```

Use `npm exec nx -- run ose-app-web-e2e:test:e2e:ui` to debug interactively, or
`npm exec nx -- run ose-app-web-e2e:test:e2e:report` to open the last report.

## Target a running environment

The default app URL is `http://localhost:3300`. Set `WEB_BASE_URL` for a different running
environment. Keep credentials and deployment-access tokens in uncommitted local configuration only.

## Checks and specs

```bash
npm exec nx -- run ose-app-web-e2e:test:quick
npm exec nx -- run ose-app-web-e2e:test:specs
```

The product behavior source of truth is
[the OSE app-web Gherkin suite](../../specs/apps/ose/behavior/app-web/gherkin/README.md).
