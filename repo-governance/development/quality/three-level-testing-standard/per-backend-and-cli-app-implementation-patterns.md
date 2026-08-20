---
title: "Per-Backend and CLI App Implementation Patterns"
description: "Implementation patterns for backend and CLI test projects."
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
when_to_use: "Use when implementing tests for a new backend or CLI app."
---

# Per-Backend and CLI App Implementation Patterns

## Per-Backend Implementation Pattern

Each API backend must have:

```
apps/{backend-name}/
  tests/
    unit/          # Unit test step definitions (mocked repos)
    integration/   # Integration test step definitions (real DB, no HTTP)
  docker-compose.integration.yml   # PostgreSQL + test runner
  Dockerfile.integration           # Integration test container
  project.json                     # test:unit, test:integration, test:e2e targets
```

The exact directory structure varies by language convention (e.g., Rust uses `#[cfg(test)]` modules alongside source plus a `tests/` directory, F# uses `tests/` with xUnit).

## CLI App Implementation Pattern

The Rust CLI apps (`rhino-cli`) consume the same Gherkin specs from `specs/apps/<product>/behavior/<product>-cli/gherkin/`. What the tests use as their I/O substrate differs; which Nx target actually executes them does not — for `rhino-cli` today, both rows below run in `test:unit` (see `apps/rhino-cli/project.json`'s `--test <name>` enumeration), not in a separate `test:integration` gate:

| Level            | Test File Location               | Implementation                                                       | What's Real                   |
| ---------------- | -------------------------------- | -------------------------------------------------------------------- | ----------------------------- |
| Unit             | `#[cfg(test)]` modules in `src/` | Calls command logic with mocked I/O via injected function/trait deps | Application logic only        |
| Command-pipeline | `apps/<cli-name>/tests/*.rs`     | Drives the command in-process against `/tmp` fixtures                | Filesystem + command pipeline |

**Architecture**: Both rows exercise the same behaviour described in the feature files. `src/`-inline tests inject mock dependencies (e.g., filesystem reader/writer) to replace real filesystem calls. The `tests/*.rs` binaries run the full command path against controlled temporary directory fixtures — and, for `rhino-cli`, that row runs in `test:unit`/`test:quick` (pre-push and CI), not in a separate `test:integration` gate; `test:integration`'s `cargo test --tests` re-runs the identical binaries on demand but is not wired into any CI job. See [Projects with Integration Tests](../../infra/nx-targets/mandatory-targets-integration-tests.md) for the current-state detail.

```
src/-inline:       Behaviour -> Command Logic -> Mocked I/O dependencies
tests/*.rs binary: Behaviour -> Command run   -> Real /tmp filesystem
```

**Coverage**: Coverage is measured at the `--lib` level only (≥90% line coverage via `cargo-llvm-cov`). Both rows must cover all behaviour for their command; a small carve-out reads the real repository tree read-only rather than an isolated `/tmp` fixture — see [Level 1 unit tests](./level-1-unit-tests-test-unit.md).

**Spec directory**: `specs/apps/<cli-name>/` — one feature file per command, organized by domain subdirectory.
