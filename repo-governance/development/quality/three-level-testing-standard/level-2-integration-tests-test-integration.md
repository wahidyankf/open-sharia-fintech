---
title: "Level 2: Integration Tests (`test:integration`)"
description: "Integration test scope and isolation."
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
when_to_use: "Use when writing an integration test."
---

# Level 2: Integration Tests (`test:integration`)

**Purpose**: Verify that business logic works correctly with a real database, testing data persistence, migrations, constraints, and transactions.

| Aspect            | Rule                                                                                |
| ----------------- | ----------------------------------------------------------------------------------- |
| Dependencies      | **Real database only** — no HTTP, no external services                              |
| Gherkin specs     | **Must consume** shared specs from the project's `specs/apps/<app-name>/` directory |
| Database          | **Real PostgreSQL** via `docker-compose.integration.yml`                            |
| HTTP layer        | **None** — call service/repository functions directly, no HTTP dispatch             |
| External services | None                                                                                |
| Coverage          | Not measured at this level                                                          |
| Nx caching        | `cache: false` (real database = non-deterministic)                                  |
| Runs in           | Scheduled CI (combined with E2E in per-service workflows)                           |

**Architecture**: Step definitions call service/repository functions directly with a real PostgreSQL connection. No HTTP framework is involved — no MockMvc, no TestClient, no httptest, no ConnTest, no WebApplicationFactory, no fetch, no clj-http, no Router.oneshot.

```
Gherkin Step -> Service Function -> Real PostgreSQL
```

**What "no HTTP" means**: The test harness must NOT:

- Start an HTTP server (even in-process)
- Use HTTP client libraries (even in-process dispatch like MockMvc)
- Route requests through HTTP middleware
- Serialize/deserialize HTTP request/response bodies as part of the test path

The test harness MUST:

- Call service/handler/context functions directly as function calls
- Pass domain objects (not HTTP requests) to the service layer
- Assert on return values (not HTTP response codes)

**Docker infrastructure**: Each backend has:

- `docker-compose.integration.yml` — PostgreSQL + test runner services
- `Dockerfile.integration` — language runtime + test execution
