---
title: "Principles and Conventions Implemented/Respected"
description: "Principles/conventions implemented."
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
when_to_use: "Use to trace this standard's rationale."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Each test level has explicit, non-overlapping boundaries for what is real and what is mocked. There is no ambiguity about whether a test hits a real database or makes HTTP calls.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: All three levels consume the same Gherkin specifications automatically. Adding a new scenario to the shared specs propagates to unit, integration, and E2E tests without manual synchronization.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Up to three levels — no more. Each tests a distinct concern: business logic (unit), a real integration boundary such as data persistence where one exists (integration), full-stack behavior (E2E). Project types without a real integration boundary (content platforms and marketing FE) run unit + e2e only.

## Conventions Implemented/Respected

- **[Nx Target Standards](../infra/nx-targets.md)**: The three levels map to `test:unit`, `test:integration`, and `test:e2e` Nx targets with standard naming and caching rules.

- **[BDD Spec-to-Test Mapping](../../infra/bdd-spec-test-mapping.md)**: All levels consume Gherkin feature files from the shared `specs/` directory, maintaining the 1:1 spec-to-test mapping.
