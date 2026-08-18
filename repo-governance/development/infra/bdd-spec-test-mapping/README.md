---
title: "BDD Spec-to-Test Mapping Convention"
description: "Gherkin spec consumption rules for CLI apps (1:1 command mapping) and demo-be backends (three-level unit/integration/e2e)"
when_to_use: "Read this index to find the right BDD Spec-to-Test Mapping Convention child document."
---

# BDD Spec-to-Test Mapping Convention

- [Principles and Command Mapping](./principles-and-command-mapping.md) — Core principles and the Acceptance Criteria convention this mapping builds on, plus the mandatory Clap-subcommand-to-Gherkin-tag rule and the domain-prefixed subcommand pattern. Use when confirming which principles and conventions this mapping convention builds on, or checking the core command-to-tag mapping rule before adding a new CLI command.
- [Mapping Layers](./mapping-layers.md) — The three mapping layers that tie a CLI command to its Gherkin tag, the tag to its feature file, and the tag to its unit and integration test files. Use when deriving a `@tag` from a command file, deciding whether a command needs its own feature file, or tracing which test files consume a given tag.
- [File Naming Convention and Coverage Enforcement](./file-naming-and-coverage-enforcement.md) — The file naming pattern that ties CLI commands, tests, and feature files together, how `rhino-cli specs coverage` enforces it, and the steps for adding a new CLI command. Use when naming the command/test/feature files for a new CLI command, running spec coverage checks, or scaffolding a new CLI command end-to-end.
- [CLI Apps: Dual-Level Spec Consumption](./cli-dual-level-spec-consumption.md) — How CLI apps consume the same Gherkin specs at both unit and integration test levels via different step implementations, plus related documentation cross-references. Use when writing unit vs. integration step definitions for a CLI command, or looking up related conventions and standards this mapping cross-references.
- [API Backend: Three-Level Spec Consumption](./api-backend-spec-consumption.md) — How demo-be backends consume shared Gherkin specs from a common gherkin/ directory at the unit, integration, and E2E test levels. Use when wiring a demo-be backend's unit, integration, or E2E tests to shared Gherkin scenarios, or validating that all three levels pass.
