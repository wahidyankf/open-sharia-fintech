# organiclever-www-fe-e2e

This project makes sure OrganicLever’s public site remains understandable, usable, and accessible
in a real browser. It checks the marketing home page and its WCAG-focused behavior from a visitor’s
point of view. 🌱

## Run the suite

```bash
# Install Chromium once on this machine
npm exec nx -- run organiclever-www-fe-e2e:install

# Run all browser scenarios; the test target starts the site it needs
npm exec nx -- run organiclever-www-fe-e2e:test:e2e
```

For an interactive investigation, use `npm exec nx -- run organiclever-www-fe-e2e:test:e2e:ui`. To
open the last report, use `npm exec nx -- run organiclever-www-fe-e2e:test:e2e:report`.

## Checks and specs

```bash
npm exec nx -- run organiclever-www-fe-e2e:test:quick
npm exec nx -- run organiclever-www-fe-e2e:test:specs
```

The default target is `http://localhost:3200`. Set `BASE_URL` only to check another running
environment. The scenarios live in
[the OrganicLever public-site Gherkin specs](../../specs/apps/organiclever/www/behaviors/frontend/README.md).
