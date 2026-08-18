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

The Rust CLI apps (`rhino-cli`) consume the same Gherkin specs from `specs/apps/<product>/behavior/<product>-cli/gherkin/` at both the unit and integration levels. The difference is what the tests use as their I/O substrate:

| Level       | Test File Location               | Implementation                                                       | What's Real                   |
| ----------- | -------------------------------- | -------------------------------------------------------------------- | ----------------------------- |
| Unit        | `#[cfg(test)]` modules in `src/` | Calls command logic with mocked I/O via injected function/trait deps | Application logic only        |
| Integration | `apps/<cli-name>/tests/*.rs`     | Drives the command in-process against `/tmp` fixtures                | Filesystem + command pipeline |

**Architecture**: Both levels exercise the same behaviour described in the feature files. Unit tests inject mock dependencies (e.g., filesystem reader/writer) to replace real filesystem calls. Integration tests run the full command path against controlled temporary directory fixtures.

```
Unit:        Behaviour -> Command Logic -> Mocked I/O dependencies
Integration: Behaviour -> Command run   -> Real /tmp filesystem
```

**Coverage**: Coverage is measured at the unit level (≥90% line coverage via `cargo-llvm-cov`). Both levels must cover all behaviour for their command.

**Spec directory**: `specs/apps/<cli-name>/` — one feature file per command, organized by domain subdirectory.
