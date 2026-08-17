---
title: "Three-Level Testing Standard"
description: "Defines the three-level testing standard (unit, integration, E2E) for all projects in the monorepo"
when_to_use: "Read this index to find the right Three-Level Testing Standard child document."
---

# Three-Level Testing Standard

- [Principles and Conventions Implemented/Respected](./01-principles-and-conventions-implemented-respected.md) — Principles/conventions implemented. Use to trace this standard's rationale.
- [Level 1: Unit Tests (`test:unit`)](./02-level-1-unit-tests-test-unit.md) — Unit test scope and isolation. Use when writing a unit test.
- [Level 2: Integration Tests (`test:integration`)](./03-level-2-integration-tests-test-integration.md) — Integration test scope and isolation. Use when writing an integration test.
- [Level 3: E2E Tests (`test:e2e`)](./04-level-3-e2e-tests-test-e2e.md) — E2E test scope. Use when writing an E2E test.
- [Spec Consumption Summary](./05-spec-consumption-summary.md) — Which level consumes which spec artifact. Use to check which level consumes a spec.
- [Nx Cache Inputs Requirement](./06-nx-cache-inputs-requirement.md) — Declaring specs/ as an Nx cache input. Use when configuring a test target's cache inputs.
- [Coverage Enforcement and Threshold Rationale](./07-coverage-enforcement-and-threshold-rationale.md) — How and why coverage is enforced. Use when a coverage gate fails or its threshold is questioned.
- [Mandatory Test Levels Matrix](./08-mandatory-test-levels-matrix.md) — Mandatory levels per project type. Use to check required test levels for a project type.
- [Gherkin-Everywhere Mandate](./09-gherkin-everywhere-mandate.md) — Every level consumes Gherkin specs. Use when a test lacks a Gherkin scenario.
- [No Network in Integration Tests, External Dependencies Optional in E2E](./10-no-network-and-external-dependencies-in-tests.md) — Network/dependency rules for integration vs. E2E. Use when a test needs an external dependency.
- [Repository Pattern Requirement](./11-repository-pattern-requirement.md) — Persistence must go through a repository interface. Use when adding data access code.
- [Contract-Driven Development](./12-contract-driven-development.md) — API contracts drive test development. Use when an API contract changes.
- [CI Workflow Mapping](./13-ci-workflow-mapping.md) — Which CI job runs which test level. Use to locate a test level's CI job.
- [Spec-Coverage Validation](./14-spec-coverage-validation.md) — How spec coverage is validated. Use when a spec-coverage gate fails.
- [Accessibility Testing](./15-accessibility-testing.md) — Accessibility testing within this standard. Use when scoping an accessibility test.
- [Known Gaps](./16-known-gaps.md) — Known testing gaps. Use to check if a gap is already known.
- [Per-Backend and CLI App Implementation Patterns](./17-per-backend-and-cli-app-implementation-patterns.md) — Implementation patterns for backend and CLI test projects. Use when implementing tests for a new backend or CLI app.
- [Applicability by Project Type](./18-applicability-by-project-type.md) — Which parts apply to which project type. Use to check applicability for a project type.
- [Anti-Patterns](./19-anti-patterns.md) — Testing anti-patterns to avoid. Use when reviewing a test for anti-patterns.
- [CI Integration, Principles Traceability, and See Also](./20-ci-integration-principles-traceability-and-see-also.md) — CI integration, principle traceability, and related links. Use for CI wiring, principle tracing, or related docs.
