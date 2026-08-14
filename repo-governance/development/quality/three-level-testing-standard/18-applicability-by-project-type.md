---
title: "Applicability by Project Type"
description: "Which parts apply to which project type."
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
when_to_use: "Use to check applicability for a project type."
---

# Applicability by Project Type

The three-level standard applies universally, with adaptations per project type:

| Project Type                    | Unit                          | Integration                      | E2E                | test:quick | Gherkin Specs                          |
| ------------------------------- | ----------------------------- | -------------------------------- | ------------------ | ---------- | -------------------------------------- |
| API backend (`organiclever-be`) | All mocked + specs            | Real PostgreSQL, no HTTP + specs | Playwright + specs | Yes        | `specs/apps/<backend-name>/`           |
| Product app-web (`*-app-web`)   | Vitest mocks + specs          | MSW in-process (cacheable)       | Playwright + specs | Yes        | `specs/apps/{domain}/{be,fe}/gherkin/` |
| Content platform & marketing FE | Vitest mocks + all specs      | N/A (no-op `echo`)               | Playwright + specs | Yes        | `specs/apps/{domain}/{be,fe}/gherkin/` |
| CLI app (Rust)                  | cargo test unit + integration | cargo integration (cacheable)    | N/A                | Yes        | `specs/apps/<cli-name>/`               |
| Library (Rust)                  | cargo test unit               | cargo integration (cacheable)    | N/A                | Yes        | `specs/libs/<lib-name>/`               |
| E2E runner                      | N/A                           | N/A                              | Playwright         | N/A        | Shared specs                           |

**Key rules by project type**:

- **API backends**: All three levels mandatory; all consume Gherkin specs; integration uses real PostgreSQL with no HTTP
- **Product app-web (app-tier, `*-app-web`)**: All three levels mandatory; integration uses in-process backend mocking (MSW); cacheable
- **Content platforms & marketing FE (`*-www`)**: Unit + e2e mandatory; **no integration tier** (`test:integration` is a no-op `echo`); the full Gherkin contract is consumed at the unit tier (external deps mocked) plus e2e; cacheable
- **CLI apps**: Unit + integration mandatory; both levels cover the behaviour in the Gherkin specs; unit mocks all I/O via injected dependencies; integration uses real filesystem with `/tmp` fixtures; cacheable
- **Libraries**: Unit mandatory; integration optional (public API calls); cacheable
