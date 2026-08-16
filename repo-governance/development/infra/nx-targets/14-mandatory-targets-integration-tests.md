---
title: "Projects with Integration Tests"
description: The two integration-test patterns (Docker+PostgreSQL for API backends, in-process mocking elsewhere) and the Rust CLI two-test-file convention.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when implementing or reviewing a project's test:integration target.
---

# Projects with Integration Tests

Two integration test patterns exist depending on project type:

| Pattern             | Projects                                              | Requirement                                                                                                                                                | Cacheable |
| ------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| Docker + PostgreSQL | API backends (`organiclever-be`)                      | Real PostgreSQL via `docker-compose.integration.yml`; calls application code directly (no HTTP layer); runs all shared Gherkin scenarios; fresh DB per run | No        |
| In-process mocking  | `organiclever-app-web` (MSW), Rust CLIs (cucumber-rs) | In-process mocking only (MSW / cucumber-rs / mock fixtures); no real database or external services; fully deterministic                                    | Yes       |

**API backends** expose `test:integration` which runs `docker compose -f docker-compose.integration.yml up --abort-on-container-exit --build`. This starts a fresh PostgreSQL container, runs migrations, and executes all shared Gherkin scenarios by calling application service/repository functions directly — no HTTP layer. Each backend has a `docker-compose.integration.yml` (postgres + test runner services) and a `Dockerfile.integration` (language runtime + test execution). Coverage is NOT measured at the integration level — coverage comes from `test:unit` only.

**Rust CLIs** (`ayokoding-cli`, `ose-cli`, `rhino-cli`) consume Gherkin specs at both test levels. Each command has two test files:

- `{domain}_{action}_test.rs` (unit, inline `#[cfg(test)]` or separate file) — cucumber-rs unit step definitions; runs in `test:quick` via `cargo test`; mocks all I/O via injected function types; coverage measured here
- `tests/{domain}_{action}_integration_test.rs` — cucumber-rs integration step definitions; drives the command via process invocation against controlled `/tmp` filesystem fixtures; runs in `test:integration`

Both levels consume the same feature file `@tag`. See
[BDD Spec-to-Test Mapping Convention](../bdd-spec-test-mapping.md) for the mandatory 1:1 mapping
between commands and feature file `@tags`.

**Rust libs** (`rust-commons`) expose `test:unit` using the standard `cargo test` harness with
`cargo-llvm-cov` for coverage. Because libs have no CLI commands, unit tests call the public API
directly. Feature files live in `specs/libs/{lib-name}/`.
