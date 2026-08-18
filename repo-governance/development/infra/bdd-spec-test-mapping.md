---
title: "BDD Spec-to-Test Mapping Convention"
description: Gherkin spec consumption rules for CLI apps (1:1 command mapping) and demo-be backends (three-level unit/integration/e2e)
category: explanation
subcategory: development
tags:
  - bdd
  - gherkin
  - integration-testing
  - specs:coverage
  - demo-be
created: 2026-03-06
when_to_use: Use when deciding how a CLI command or demo-be backend should consume its Gherkin specs, or when navigating to the mapping-layer, coverage-enforcement, or backend-consumption detail pages.
---

# BDD Spec-to-Test Mapping Convention

This convention defines how Gherkin specifications are consumed across the monorepo:

- **CLI apps**: Mandatory 1:1 mapping between commands and Gherkin specs via the Rust test harness at both unit and integration test levels
- **Demo-be backends**: Three-level consumption of shared Gherkin specs (unit/integration/e2e) with different step implementations at each level

## Documentation

- [Principles and Command Mapping](./bdd-spec-test-mapping/principles-and-command-mapping.md) — Core principles and the Acceptance Criteria convention this mapping builds on, plus the mandatory Clap-subcommand-to-Gherkin-tag rule and the domain-prefixed subcommand pattern. Use when confirming which principles and conventions this mapping convention builds on, or checking the core command-to-tag mapping rule before adding a new CLI command.
- [Mapping Layers](./bdd-spec-test-mapping/mapping-layers.md) — The three mapping layers that tie a CLI command to its Gherkin tag, the tag to its feature file, and the tag to its unit and integration test files. Use when deriving a `@tag` from a command file, deciding whether a command needs its own feature file, or tracing which test files consume a given tag.
- [File Naming Convention and Coverage Enforcement](./bdd-spec-test-mapping/file-naming-and-coverage-enforcement.md) — The file naming pattern that ties CLI commands, tests, and feature files together, how `rhino-cli specs coverage` enforces it, and the steps for adding a new CLI command. Use when naming the command/test/feature files for a new CLI command, running spec coverage checks, or scaffolding a new CLI command end-to-end.
- [CLI Apps: Dual-Level Spec Consumption](./bdd-spec-test-mapping/cli-dual-level-spec-consumption.md) — How CLI apps consume the same Gherkin specs at both unit and integration test levels via different step implementations, plus related documentation cross-references. Use when writing unit vs. integration step definitions for a CLI command, or looking up related conventions and standards this mapping cross-references.
- [API Backend: Three-Level Spec Consumption](./bdd-spec-test-mapping/api-backend-spec-consumption.md) — How demo-be backends consume shared Gherkin specs from a common gherkin/ directory at the unit, integration, and E2E test levels. Use when wiring a demo-be backend's unit, integration, or E2E tests to shared Gherkin scenarios, or validating that all three levels pass.
