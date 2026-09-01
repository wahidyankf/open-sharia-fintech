---
title: "Three-Level Testing Standard"
description: Defines the three-level testing standard (unit, integration, E2E) for all projects in the monorepo
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
when_to_use: "Use when scoping, writing, or reviewing a unit, integration, or E2E test."
---

# Three-Level Testing Standard

Every project in this monorepo tests at three levels -- unit, integration, and E2E -- each consuming Gherkin specs and enforced by its own coverage and CI gates.

## Documents

- [Principles and Conventions Implemented/Respected](./three-level-testing-standard/principles-and-conventions-implemented-respected.md) — Principles/conventions implemented. Use to trace this standard's rationale.
- [Level 1: Unit Tests (`test:unit`)](./three-level-testing-standard/level-1-unit-tests-test-unit.md) — Unit test scope and isolation. Use when writing a unit test.
- [Level 2: Integration Tests (`test:integration`)](./three-level-testing-standard/level-2-integration-tests-test-integration.md) — Integration test scope and isolation. Use when writing an integration test.
- [Level 3: E2E Tests (`test:e2e`)](./three-level-testing-standard/level-3-e2e-tests-test-e2e.md) — E2E test scope. Use when writing an E2E test.
- [Spec Consumption Summary](./three-level-testing-standard/spec-consumption-summary.md) — Which level consumes which spec artifact. Use to check which level consumes a spec.
- [Nx Cache Inputs Requirement](./three-level-testing-standard/nx-cache-inputs-requirement.md) — Declaring specs/ as an Nx cache input. Use when configuring a test target's cache inputs.
- [Coverage Enforcement and Threshold Rationale](./three-level-testing-standard/coverage-enforcement-and-threshold-rationale.md) — How and why coverage is enforced. Use when a coverage gate fails or its threshold is questioned.
- [Mandatory Test Levels Matrix](./three-level-testing-standard/mandatory-test-levels-matrix.md) — Mandatory levels per project type. Use to check required test levels for a project type.
- [Gherkin-Everywhere Mandate](./three-level-testing-standard/gherkin-everywhere-mandate.md) — Every level consumes Gherkin specs. Use when a test lacks a Gherkin scenario.
- [No Network in Integration Tests, External Dependencies Optional in E2E](./three-level-testing-standard/no-network-and-external-dependencies-in-tests.md) — Network/dependency rules for integration vs. E2E. Use when a test needs an external dependency.
- [Testing Contract Enforcement](./three-level-testing-standard/testing-contract-enforcement.md) — The four machine-checked policies and their commands. Use when a test-contract check fails.
- [Repository Pattern Requirement](./three-level-testing-standard/repository-pattern-requirement.md) — Persistence must go through a repository interface. Use when adding data access code.
- [Contract-Driven Development](./three-level-testing-standard/contract-driven-development.md) — API contracts drive test development. Use when an API contract changes.
- [CI Workflow Mapping](./three-level-testing-standard/ci-workflow-mapping.md) — Which CI job runs which test level. Use to locate a test level's CI job.
- [Spec-Coverage Validation](./three-level-testing-standard/spec-coverage-validation.md) — How spec coverage is validated. Use when a spec-coverage gate fails.
- [Accessibility Testing](./three-level-testing-standard/accessibility-testing.md) — Accessibility testing within this standard. Use when scoping an accessibility test.
- [Known Gaps](./three-level-testing-standard/known-gaps.md) — Known testing gaps. Use to check if a gap is already known.
- [Per-Backend and CLI App Implementation Patterns](./three-level-testing-standard/per-backend-and-cli-app-implementation-patterns.md) — Implementation patterns for backend and CLI test projects. Use when implementing tests for a new backend or CLI app.
- [Applicability by Project Type](./three-level-testing-standard/applicability-by-project-type.md) — Which parts apply to which project type. Use to check applicability for a project type.
- [Anti-Patterns](./three-level-testing-standard/anti-patterns.md) — Testing anti-patterns to avoid. Use when reviewing a test for anti-patterns.
- [CI Integration, Principles Traceability, and See Also](./three-level-testing-standard/ci-integration-principles-traceability-and-see-also.md) — CI integration, principle traceability, and related links. Use for CI wiring, principle tracing, or related docs.
