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

**Rust CLIs** (`rhino-cli`) consume Gherkin specs via cucumber-rs binaries under
`apps/rhino-cli/tests/*.rs`, one binary per feature-file cluster. Every such binary is named
explicitly in `test:unit`'s `--test <name>` enumeration (`project.json`) and therefore runs in
`test:quick` — the pre-push AND CI gate. `test:integration`'s `cargo test --tests` auto-discovers
and re-runs the identical set of binaries, but for `rhino-cli` `test:integration` itself is not
wired into pre-push or any CI workflow job, so it is a manual, on-demand duplicate run rather than
a second, distinct test level. Coverage is measured from `--lib` only (`test:coverage`), not from
the `tests/*.rs` binaries at either level. See
[BDD Spec-to-Test Mapping Convention](../bdd-spec-test-mapping.md) for the mandatory 1:1 mapping
between commands and feature file `@tags`.

**Rust libs**, when one exists, expose `test:unit` using the standard `cargo test` harness with
`cargo-llvm-cov` for coverage. Because libs have no CLI commands, unit tests call the public API
directly. Feature files live in `specs/libs/{lib-name}/`. There is no Rust lib in the workspace
today; `rhino-cli` is the only Rust project.
