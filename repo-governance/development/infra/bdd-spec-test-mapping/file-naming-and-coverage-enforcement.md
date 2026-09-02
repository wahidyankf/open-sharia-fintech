---
title: "File Naming Convention and Coverage Enforcement"
description: The file naming pattern that ties CLI commands, tests, and feature files together, how `rhino-cli specs coverage` enforces it, and the steps for adding a new CLI command.
category: explanation
subcategory: development
tags:
  - bdd
  - gherkin
  - specs:coverage
created: 2026-03-06
when_to_use: Use when naming the command/test/feature files for a new CLI command, running spec coverage checks, or scaffolding a new CLI command end-to-end.
---

# File Naming Convention and Coverage Enforcement

## File Naming Convention

| Artifact         | Pattern                                                         | Example                                                |
| ---------------- | --------------------------------------------------------------- | ------------------------------------------------------ |
| Parent cmd       | `{domain}.rs`                                                   | `agents.rs`                                            |
| Command file     | `{domain}_{action}.rs`                                          | `agents_validate_sync.rs`                              |
| Unit test        | `{domain}_{action}_test.rs`                                     | `agents_validate_sync_test.rs`                         |
| Integration test | `tests/{domain}_{action}_integration_test.rs`                   | `agents_validate_sync_integration_test.rs`             |
| Feature file     | `specs/apps/{product}/cli/behaviors/{domain}/{command}.feature` | `specs/apps/rhino/cli/behaviors/system/doctor.feature` |

**Unit test files** (`{domain}_{action}_test.rs`) serve dual purpose: they contain both Gherkin step definitions (consuming the command's `@tag` scenarios) and any non-BDD pure function tests for edge cases not covered by the Gherkin scenarios. The step definitions in unit test files use injected I/O function types instead of real filesystem access.

**The universal rule**: All Rust CLI files (command, unit test, integration test) use underscores. Feature files and `@tag`s use hyphens. The `rhino-cli specs coverage` tool normalises hyphens to underscores when matching feature stems to Rust test files.

## Coverage Enforcement

The `rhino-cli specs coverage` command enforces this mapping at three levels:

1. **File-level**: Every `.feature` file must have a matching `*_test.*` file
2. **Scenario-level**: Every `Scenario:` in the feature must appear as `// Scenario:` comment or `Scenario(...)` call in test code
3. **Step-level**: Every Given/When/Then step must have a matching step definition

Run the check:

```bash
rhino-cli specs coverage specs/apps/rhino apps/rhino-cli
```

**Scope**: Spec-coverage enforcement is currently active for **CLI apps only** (Rust + cucumber-rs naming
conventions). Enforcement for demo-be backends is **planned but deferred** — the tool needs
enhancement to support demo-be test file naming conventions (e.g., `health_steps.rs` for Rust)
which differ from the CLI app naming patterns the tool currently expects. This will be addressed in a follow-up plan.

## Adding a New Command

### Rust CLI apps (rhino-cli)

1. Create the feature file `specs/apps/{product}/cli/behaviors/{domain}/{domain}-{action}.feature`
2. Create `apps/{app}/src/commands/{domain}_{action}.rs` with the Clap subcommand (register in `main.rs`)
3. Create `apps/{app}/src/commands/{domain}_{action}_test.rs` (or inline `#[cfg(test)]` module) with unit step definitions — mock I/O via injected function types, no special build tag (runs in `test:quick`)
4. Create `apps/{app}/tests/{domain}_{action}_integration_test.rs` with integration steps — drive via process invocation against real `/tmp` fixtures
5. Verify: `rhino-cli specs coverage specs/apps/{app-spec-dir} apps/{app}`
