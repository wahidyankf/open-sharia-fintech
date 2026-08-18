---
title: "API Backend: Three-Level Spec Consumption"
description: How demo-be backends consume shared Gherkin specs from a common gherkin/ directory at the unit, integration, and E2E test levels.
category: explanation
subcategory: development
tags:
  - bdd
  - gherkin
  - integration-testing
  - demo-be
created: 2026-03-06
when_to_use: Use when wiring a demo-be backend's unit, integration, or E2E tests to shared Gherkin scenarios, or validating that all three levels pass.
---

# API Backend: Three-Level Spec Consumption

API backends consume shared Gherkin scenarios from their own `specs/apps/<backend-name>/behavior/<product>-be/gherkin/`
directory at three test levels. The feature files are the shared contract — only the step
implementations change per level.

## Shared Specs

```
specs/apps/<backend-name>/behavior/<product>-be/gherkin/
├── auth/
│   ├── login.feature
│   ├── register.feature
│   └── ...
├── resources/
│   ├── list-items.feature
│   └── ...
└── ... (see gherkin README for full list)
```

## Three Levels

| Level           | Nx Target          | Step Implementations                                        | Dependencies             | What's Real            |
| --------------- | ------------------ | ----------------------------------------------------------- | ------------------------ | ---------------------- |
| **Unit**        | `test:unit`        | Call service/repository functions directly with mocked deps | All mocked               | Application logic only |
| **Integration** | `test:integration` | Call service/repository functions directly with real DB     | Real PostgreSQL (Docker) | Application + database |
| **E2E**         | `test:e2e`         | Playwright HTTP requests to running server                  | Full running server      | Everything             |

## Unit-Level Step Definitions

Unit steps call application service/repository functions directly. All dependencies (database, external APIs) are mocked via in-memory implementations or test doubles.

- No HTTP framework, no database connections
- Steps instantiate services with mocked repositories
- Coverage is measured at this level (≥90% line coverage)
- Must run all shared scenarios

## Integration-Level Step Definitions

Integration steps call application service/repository functions directly against a real PostgreSQL database via docker-compose. No HTTP layer.

- `docker-compose.integration.yml` starts PostgreSQL + test runner
- `Dockerfile.integration` contains language runtime + test execution
- Steps connect to PostgreSQL, run migrations, execute all shared scenarios
- Coverage is NOT measured at this level
- Must run all shared scenarios

## E2E-Level Step Definitions

E2E tests live in a dedicated `*-e2e` Playwright project. Steps make real HTTP requests to a running backend via `playwright-bdd`.

- Tests the full HTTP API contract
- Must run all shared scenarios

## Validation

To verify all scenarios pass at each level for a given backend:

```bash
# Unit tests (mocked dependencies)
nx run <backend-name>:test:unit

# Integration tests (real PostgreSQL via docker-compose)
nx run <backend-name>:test:integration

# E2E tests (Playwright HTTP against running backend)
nx run <backend-name>-e2e:test:e2e
```

All three commands must report all scenarios passing. The Gherkin feature files serve as the single source of truth — if a scenario fails at any level, the backend is non-compliant.
