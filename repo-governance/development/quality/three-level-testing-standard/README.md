---
title: "Three-Level Testing Standard"
description: "Defines the three-level testing standard (unit, integration, E2E) for all projects in the monorepo"
when_to_use: "Read this index to find the right Three-Level Testing Standard child document."
---

# Three-Level Testing Standard

- [Principles and Conventions Implemented/Respected](./principles-and-conventions-implemented-respected.md) — Principles/conventions implemented. Use to trace this standard's rationale.
- [Level 1: Unit Tests (`test:unit`)](./level-1-unit-tests-test-unit.md) — Unit test scope and isolation. Use when writing a unit test.
- [Level 2: Integration Tests (`test:integration`)](./level-2-integration-tests-test-integration.md) — Integration test scope and isolation. Use when writing an integration test.
- [Level 3: E2E Tests (`test:e2e`)](./level-3-e2e-tests-test-e2e.md) — E2E test scope. Use when writing an E2E test.
- [Spec Consumption Summary](./spec-consumption-summary.md) — Which level consumes which spec artifact. Use to check which level consumes a spec.
- [Nx Cache Inputs Requirement](./nx-cache-inputs-requirement.md) — Declaring specs/ as an Nx cache input. Use when configuring a test target's cache inputs.
- [Coverage Enforcement and Threshold Rationale](./coverage-enforcement-and-threshold-rationale.md) — How and why coverage is enforced. Use when a coverage gate fails or its threshold is questioned.
- [Mandatory Test Levels Matrix](./mandatory-test-levels-matrix.md) — Mandatory levels per project type. Use to check required test levels for a project type.
- [Gherkin-Everywhere Mandate](./gherkin-everywhere-mandate.md) — Every level consumes Gherkin specs. Use when a test lacks a Gherkin scenario.
- [No Network in Integration Tests, External Dependencies Optional in E2E](./no-network-and-external-dependencies-in-tests.md) — Network/dependency rules for integration vs. E2E. Use when a test needs an external dependency.
- [Testing Contract Enforcement](./testing-contract-enforcement.md) — The four machine-checked testing policies and the command that enforces each. Use when a test-contract check fails or when adding a project to the testing registry.
- [Repository Pattern Requirement](./repository-pattern-requirement.md) — Persistence must go through a repository interface. Use when adding data access code.
- [Contract-Driven Development](./contract-driven-development.md) — API contracts drive test development. Use when an API contract changes.
- [CI Workflow Mapping](./ci-workflow-mapping.md) — Which CI job runs which test level. Use to locate a test level's CI job.
- [Spec-Coverage Validation](./spec-coverage-validation.md) — How spec coverage is validated. Use when a spec-coverage gate fails.
- [Accessibility Testing](./accessibility-testing.md) — Accessibility testing within this standard. Use when scoping an accessibility test.
- [Known Gaps](./known-gaps.md) — Known testing gaps. Use to check if a gap is already known.
- [Per-Backend and CLI App Implementation Patterns](./per-backend-and-cli-app-implementation-patterns.md) — Implementation patterns for backend and CLI test projects. Use when implementing tests for a new backend or CLI app.
- [Applicability by Project Type](./applicability-by-project-type.md) — Which parts apply to which project type. Use to check applicability for a project type.
- [Anti-Patterns](./anti-patterns.md) — Testing anti-patterns to avoid. Use when reviewing a test for anti-patterns.
- [CI Integration, Principles Traceability, and See Also](./ci-integration-principles-traceability-and-see-also.md) — CI integration, principle traceability, and related links. Use for CI wiring, principle tracing, or related docs.
