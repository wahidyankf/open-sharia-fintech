---
title: "App-Type-Specific Test Manifestations and Gherkin Consumption Matrix"
description: How each app type implements test levels and consumes Gherkin.
category: explanation
subcategory: development
tags: [ci-cd, testing]
created: 2026-03-31
when_to_use: Use when implementing tests for an app type.
---

# App-Type-Specific Test Manifestations and Gherkin Consumption Matrix

## App-Type-Specific Test Manifestations

Each app type implements the three levels according to its domain. The table below shows how each
app type realises each level.

| App Type                                          | Unit (`test:unit`)                                    | Integration (`test:integration`)                                              | E2E (`test:e2e`)                                     |
| ------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------- |
| **BE API** (`organiclever-be`)                    | BDD, mocked repos, calls service fns directly         | Real PostgreSQL via docker-compose, calls service fns directly (no HTTP)      | Playwright, real HTTP + real PostgreSQL              |
| **FE** (`organiclever-app-web`)                   | Vitest, all API calls mocked (MSW / mock services)    | MSW with real DOM; in-process mocking only                                    | Playwright against running FE + BE                   |
| **CLI** (`*-cli`)                                 | `cargo test`, all I/O mocked via dependency injection | `cargo test` with real filesystem via tmp fixtures, real HTTP via mock server | Not applicable                                       |
| **Content platform** (`ayokoding-www`, `ose-www`) | Vitest, components and tRPC routes mocked             | MSW, in-process mocking                                                       | Playwright BE E2E (`*-be-e2e`) + FE E2E (`*-fe-e2e`) |
| **Library** (`web-ui`, `ts-env-loader`)           | Vitest, dependencies mocked                           | In-process mocking only                                                       | Not applicable                                       |
| **E2E runner** (`*-e2e`)                          | Not applicable                                        | Not applicable                                                                | Playwright — this project IS the E2E suite           |

## Gherkin Consumption Matrix

All testable projects must consume Gherkin specifications at every applicable test level. E2E
runner projects ARE the Gherkin consumers at the E2E level.

| App Type                    | Unit consumes Gherkin                                                  | Integration consumes Gherkin | E2E consumes Gherkin                 |
| --------------------------- | ---------------------------------------------------------------------- | ---------------------------- | ------------------------------------ |
| BE API (`organiclever-be`)  | Yes — `specs/apps/organiclever/behavior/organiclever-be/gherkin/`      | Yes — same specs             | Yes — same specs                     |
| FE (`organiclever-app-web`) | Yes — `specs/apps/organiclever/behavior/organiclever-app-web/gherkin/` | Yes — same specs             | Yes — via `organiclever-app-web-e2e` |
| CLI (`*-cli`)               | Yes — `specs/apps/{domain}/behavior/<product>-cli/gherkin/`            | Yes — same specs             | Not applicable                       |
| Content platform            | Yes — project-local specs                                              | Yes — same specs             | Yes — via `*-be-e2e` / `*-fe-e2e`    |
| Library                     | Yes — library-specific specs                                           | Yes — same specs             | Not applicable                       |
| E2E runner                  | Not applicable                                                         | Not applicable               | Yes — consumes shared specs          |
