---
title: "Mapping Layers"
description: The three mapping layers that tie a CLI command to its Gherkin tag, the tag to its feature file, and the tag to its unit and integration test files.
category: explanation
subcategory: development
tags:
  - bdd
  - gherkin
  - integration-testing
  - specs:coverage
created: 2026-03-06
when_to_use: Use when deriving a `@tag` from a command file, deciding whether a command needs its own feature file, or tracing which test files consume a given tag.
---

# Mapping Layers

The mapping operates at three levels:

## 1. Command to Tag (mandatory)

> **Scope note**: The file naming and tag derivation rules below apply to all Rust CLI apps
> (`rhino-cli`). See the
> ["CLI App Families"](./cli-dual-level-spec-consumption.md#cli-apps-dual-level-spec-consumption) section for `.rs` file patterns
> and test file locations.

The `@tag` is derived from the Rust filename: replace underscores with hyphens.

| Command File                | Full Invocation          | Feature `@tag`            |
| --------------------------- | ------------------------ | ------------------------- |
| `agents_sync.rs`            | `agents sync`            | `@agents-sync`            |
| `agents_validate_sync.rs`   | `agents validate-sync`   | `@agents-validate-sync`   |
| `agents_validate_claude.rs` | `agents validate-claude` | `@agents-validate-claude` |
| `docs_validate_links.rs`    | `docs validate-links`    | `@docs-validate-links`    |
| `doctor.rs`                 | `doctor`                 | `@doctor`                 |

## 2. Tag to Feature File (flexible)

A feature file may contain **multiple related commands** using separate `Rule` blocks with distinct `@tag` annotations. Semantically related commands (e.g., an action and its validator) can share a feature file:

```gherkin
Feature: Agent Configuration Synchronisation

  @agents-sync
  Rule: agents sync converts .claude/ configuration to .opencode/ format
    Scenario: Syncing converts agents and skills to secondary platform binding format
    ...

  @agents-validate-sync
  Rule: agents validate-sync confirms .claude/ and .opencode/ are equivalent
    Scenario: Directories that are in sync pass validation
    ...
```

Alternatively, a command with its own distinct domain gets its own feature file:

```
specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature                       <- single @doctor tag
specs/apps/rhino/behavior/rhino-cli/gherkin/agents/agents-sync.feature                  <- @agents-sync + @agents-validate-sync
specs/apps/rhino/behavior/rhino-cli/gherkin/agents/agents-validate-claude.feature       <- single @agents-validate-claude tag
```

## 3. Unit & Integration Test to Tag (mandatory)

Each command has dedicated test files at both levels that filter scenarios by `@tag`. The same tag is used at both levels, pointing to the same feature file:

**Unit test** (inline `#[cfg(test)]` module — runs in `test:quick`):

```rust
// src/commands/agents_validate_sync_test.rs
#[test]
fn unit_agents_validate_sync() {
    // Runs the @agents-validate-sync scenarios from specs/ against the
    // command logic with all I/O mocked via injected function types.
}
```

**Integration test** (`tests/` integration target — runs in `test:integration`):

```rust
// tests/agents_validate_sync_integration_test.rs
#[test]
fn integration_agents_validate_sync() {
    // Same @agents-validate-sync scenarios, driven via process invocation
    // against real /tmp fixtures (different step implementations).
}
```
