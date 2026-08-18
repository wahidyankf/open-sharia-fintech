---
title: "Level 3: E2E Tests (`test:e2e`)"
description: "E2E test scope."
category: explanation
subcategory: development
tags:
  - testing
  - unit-tests
  - integration-tests
  - e2e-tests
  - bdd
  - gherkin
created: 2026-03-13
when_to_use: "Use when writing an E2E test."
---

# Level 3: E2E Tests (`test:e2e`)

**Purpose**: Verify the complete system works end-to-end, including HTTP routing, serialization, authentication, and database persistence.

| Aspect            | Rule                                                                                |
| ----------------- | ----------------------------------------------------------------------------------- |
| Dependencies      | **All real** — real HTTP, real database, real server                                |
| Gherkin specs     | **Must consume** shared specs from the project's `specs/apps/<app-name>/` directory |
| Database          | Real PostgreSQL (via docker-compose in CI)                                          |
| HTTP layer        | Real HTTP requests via Playwright                                                   |
| External services | As needed                                                                           |
| Coverage          | Not measured at this level                                                          |
| Nx caching        | `cache: false` (full stack = non-deterministic)                                     |
| Runs in           | Scheduled CI (per-service workflows)                                                |

**Architecture**: Playwright sends real HTTP requests to a running server backed by a real database.

```
Playwright -> HTTP Request -> Running Server -> Real PostgreSQL
```
