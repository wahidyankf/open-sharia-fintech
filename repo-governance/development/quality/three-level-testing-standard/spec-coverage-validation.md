---
title: "Spec-Coverage Validation"
description: "How spec coverage is validated."
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
when_to_use: "Use when a spec-coverage gate fails."
---

# Spec-Coverage Validation

`rhino-cli specs coverage` ensures every Gherkin step has a matching step definition. This
prevents scenarios from silently having no implementation.

The tool is invoked as the `specs:coverage` Nx target and is enforced by the pre-push hook alongside
`typecheck`, `lint`, and `test:quick`. All four targets are cacheable.

## Flags

**`--shared-steps`**: All projects use this flag. It validates steps across ALL source files in the
supplied directories rather than requiring a 1:1 match between each feature file and a
corresponding step file. This accommodates shared step libraries and the varying naming conventions
across languages (e.g., `health_steps.rs` for Rust, `health_steps.ts` for TypeScript). `@wip`-tagged
scenarios are fully exempt from step-gap reporting under this flag (same rule as the
`@covers`-marker coverage model) — a step definition is never required for a scenario tagged `@wip`.

**`--exclude-dir test-support`**: API backends and FE apps use this flag. It excludes
E2E-only `test-support` API spec files from validation. These specs exist only to support E2E
testing infrastructure and are not implemented at the unit or integration level. E2E runners do
**not** use this flag because they implement those steps.

## Project Coverage Status

19 projects currently have `specs:coverage` enforced. 11 projects have it temporarily deferred
pending step implementation. The project-by-project breakdown is maintained in
[Nx Target Standards](../infra/nx-targets.md).

## Relationship to the Three Test Levels

All three test levels (unit, integration, E2E) consume the same Gherkin specs. `specs:coverage`
enforces that every step referenced in the feature files has at least one step definition
somewhere in the project's source tree. It does not verify which test level implements each step —
it verifies that no step is silently unimplemented across all levels combined.

```
Gherkin feature file
  -> specs:coverage validates: every step has a matching step definition
  -> test:unit runs: unit-level step definitions (mocked dependencies)
  -> test:integration runs: integration-level step definitions (real DB, no HTTP)
  -> test:e2e runs: E2E-level step definitions (real HTTP + real DB)
```
