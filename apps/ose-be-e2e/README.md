# ose-be-e2e

This project tests OSE’s backend through its HTTP API. Playwright-BDD executes the same behavior
examples that describe the service, without needing a browser. 🧪

## Run locally

```bash
# Install test dependencies once on this machine
npm exec nx -- run ose-be-e2e:install

# Start the API at http://localhost:8302
npm exec nx -- run ose-be:dev

# In another terminal, run the API scenarios
npm exec nx -- run ose-be-e2e:test:e2e
```

Use `npm exec nx -- run ose-be-e2e:test:e2e:ui` for Playwright’s UI or
`npm exec nx -- run ose-be-e2e:test:e2e:report` for the most recent report.

## Target a running environment

The default API address is `http://localhost:8302`. Set `API_BASE_URL` to point the suite at a
different running environment; never commit credentials or real access values.

## Checks and specs

```bash
npm exec nx -- run ose-be-e2e:test:quick
npm exec nx -- run ose-be-e2e:test:specs
```

The behavior source of truth is
[the OSE backend Gherkin suite](../../specs/apps/ose/be/behaviors/README.md).
