---
title: "Phase 12: Playwright Browsers (Sequential)"
description: "Phase 12: install Playwright's Chromium, Firefox, and WebKit browsers required by all E2E test projects."
when_to_use: "Use when setting up or repairing Playwright browsers for E2E tests."
---

# Phase 12: Playwright Browsers (Sequential)

**Depends on**: Phase 11

Required for: All E2E tests (`*-e2e` projects)

## 12.1 Install Playwright browsers

```bash
npx playwright install
```

This downloads Chromium, Firefox, and WebKit browsers used by Playwright E2E tests.
Doctor now checks for Playwright browsers — if browsers are missing, it shows a warning
with the install command.

**Success criteria**: `npx playwright install` exits 0 without errors. `npm run doctor`
shows playwright as OK (not warning).

**On failure**: On Linux, install system dependencies first:
`npx playwright install-deps`
