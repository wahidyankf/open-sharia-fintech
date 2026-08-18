---
title: "CLI Apps: Dual-Level Spec Consumption"
description: How CLI apps consume the same Gherkin specs at both unit and integration test levels via different step implementations, plus related documentation cross-references.
category: explanation
subcategory: development
tags:
  - bdd
  - gherkin
  - integration-testing
created: 2026-03-06
when_to_use: Use when writing unit vs. integration step definitions for a CLI command, or looking up related conventions and standards this mapping cross-references.
---

# CLI Apps: Dual-Level Spec Consumption

Rust CLI apps (`rhino-cli`) consume Gherkin specs at both the unit and integration test levels. The same feature files serve as the contract for both levels — only the step implementations differ.

## Architecture

| Level       | Nx Target          | Test File Pattern                                 | Step Implementation                             | Dependencies    |
| ----------- | ------------------ | ------------------------------------------------- | ----------------------------------------------- | --------------- |
| Unit        | `test:unit`        | `src/commands/{domain}_{action}_test.rs` (no tag) | Injected function types mock all I/O            | All mocked      |
| Integration | `test:integration` | `tests/{domain}_{action}_integration_test.rs`     | Process invocation against real `/tmp` fixtures | Real filesystem |

## Unit-Level Step Definitions

Unit steps call command logic directly with mocked dependencies. Injected function types (e.g., `readFileFn`, `writeFileFn`, `statFn`) are overridden in step setup to inject controlled behavior without touching the real filesystem.

- No special build tag — included in `cargo test` and `test:quick`
- Coverage is measured at this level (≥90% line coverage)
- Must run all Gherkin scenarios for the command's `@tag`

## Integration-Level Step Definitions

Integration steps drive commands via process invocation against controlled `/tmp` filesystem fixtures. Steps create temporary directory structures, invoke the command binary, and assert on stdout/stderr and exit code.

- Runs via `test:integration` target
- Coverage is NOT measured at this level
- Must run all Gherkin scenarios for the command's `@tag`

## Example: Same Spec, Two Step Implementations

The `@agents-validate-sync` tag lives inside `agents-sync.feature` (shared feature file) and is consumed at both levels:

```
specs/apps/rhino/behavior/rhino-cli/gherkin/agents/agents-sync.feature  (contains @agents-sync + @agents-validate-sync)
  -> Unit steps in:       apps/rhino-cli/src/commands/agents_validate_sync_test.rs
  -> Integration steps in: apps/rhino-cli/tests/agents_validate_sync_integration_test.rs
```

## Related Documentation

- [Acceptance Criteria Convention](../acceptance-criteria.md) - Gherkin format standards
- [Specs Directory Structure Convention](../../../conventions/structure/specs-directory-structure.md) - Canonical path patterns and domain subdirectory rules
- [Three-Level Testing Standard](../../quality/three-level-testing-standard.md) - Mandatory isolation boundaries for unit, integration, and E2E levels where Gherkin specs are consumed
- [Nx Target Standards](../nx-targets.md) - `test:integration` target definitions and caching rules
- [specs/README.md](../../../../specs/README.md) - Spec directory organization
- [specs/apps/rhino/README.md](../../../../specs/apps/rhino/README.md) - rhino-cli spec structure
