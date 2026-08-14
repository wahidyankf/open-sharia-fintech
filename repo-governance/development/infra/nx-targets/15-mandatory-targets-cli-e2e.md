---
title: "Mandatory Targets — CLI and E2E Test Projects"
description: The run/install targets required on CLI applications and the install/test:e2e/test:e2e:ui/test:e2e:report targets required on *-e2e projects.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when scaffolding a new CLI application or a new *-e2e Playwright runner project.
---

# Mandatory Targets — CLI and E2E Test Projects

## CLI Applications

Rust CLIs and similar tools:

| Target    | Requirement                                         |
| --------- | --------------------------------------------------- |
| `run`     | Execute the application (`cargo run` or equivalent) |
| `install` | Sync dependencies (`cargo build` or equivalent)     |

## E2E Test Projects

Playwright suites (`*-e2e`):

| Target            | Requirement                  |
| ----------------- | ---------------------------- |
| `install`         | Install npm dependencies     |
| `test:e2e`        | Run all tests headlessly     |
| `test:e2e:ui`     | Run tests with Playwright UI |
| `test:e2e:report` | Open the HTML test report    |

**Execution strategy**: `test:e2e` is **not** part of the pre-push hook. It runs on scheduled GitHub Actions cron jobs (2x daily at WIB 06:00 and 18:00) in per-service "Test" workflows that combine `test:integration` + `test:e2e` for each service. This keeps pre-push fast while ensuring continuous integration and E2E coverage.

**BDD suites**: When the E2E project uses playwright-bdd, `test:e2e` runs
`npx bddgen && npx playwright test`. The `bddgen` step regenerates `.features-gen/`
spec files from the Gherkin feature files before Playwright executes them.
See `apps/organiclever-be-e2e/project.json` for a canonical product-app example.

**API backend `test:integration` with docker-compose**: API backends expose `test:integration`
which runs `docker compose -f docker-compose.integration.yml down -v && docker compose -f docker-compose.integration.yml up --abort-on-container-exit --build`.
Each backend's `docker-compose.integration.yml` defines a `postgres` service (postgres:17-alpine with healthcheck)
and a `test-runner` service that depends on PostgreSQL being healthy. The test runner runs migrations,
optionally loads seed data, then executes all shared Gherkin scenarios
by calling application service/repository functions directly — no HTTP layer. The specs volume is
mounted read-only at `../../specs:/specs:ro`. After tests complete, `docker-compose` tears down all
containers and volumes.
