# wahidyankf-www

This is the personal portfolio site for Wahidyan Kresna Fridayoka. It is a small, accessible Next.js
site for a CV, projects, and search—not a product surface for OSE itself. ✨

## Run it locally

```bash
# Start at http://localhost:3201
npm exec nx -- run wahidyankf-www:dev

# Create a production build
npm exec nx -- run wahidyankf-www:build

# Serve a completed local build
npm exec nx -- run wahidyankf-www:start
```

## Check your changes

```bash
npm exec nx -- run wahidyankf-www:test:quick
npm exec nx -- run wahidyankf-www:test:integration
npm exec nx -- run wahidyankf-www:test:specs
```

Browser coverage is in the sibling
[wahidyankf-www-fe-e2e](../wahidyankf-www-fe-e2e/README.md) project. The reader-facing behavior
is described in [the Wahidyankf specs](../../specs/apps/wahidyankf/behavior/wahidyankf-www/README.md).

## Code map

Routes in `src/app/` stay thin. Most work lives in `src/features/`, where each feature separates
pure data and decisions in `core/` from React and browser behavior in `shell/`. This keeps the
portfolio easy to understand without hiding the ordinary parts behind a heavy framework.

## Delivery boundary

The site’s production delivery is automated by the repository workflow. Do not push deployment
branches manually.
