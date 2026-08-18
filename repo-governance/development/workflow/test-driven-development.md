---
title: "Test-Driven Development Convention"
description: Mandates TDD (Red→Green→Refactor) as the required practice for all code changes across the repository
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when writing any delivery checklist step that ships code, or when starting implementation of a code change.
---

# Test-Driven Development Convention

**Write the failing test first, then make it pass, then refactor** — Test-Driven Development
(TDD) is the required practice for all code changes in this repository. Red → Green → Refactor.

## Contents

- [Principles and Conventions Implemented](./test-driven-development/principles-and-conventions-implemented.md) — Why TDD is required here.
- [Scope: Which Tests TDD Covers](./test-driven-development/scope-which-tests-tdd-covers.md) — The ten verification levels TDD applies to.
- [Manual verification is part of TDD](./test-driven-development/manual-verification-is-part-of-tdd.md) — Treating a manual script like an automated test.
- [Picking the right level](./test-driven-development/picking-the-right-level.md) — Choosing the cheapest test that exercises the behavior.
- [The Red-Green-Refactor Cycle](./test-driven-development/the-red-green-refactor-cycle.md) — The three-step loop every code change follows.
- [Mini-TDD Passes](./test-driven-development/mini-tdd-passes.md) — Splitting a feature into small Red→Green→Refactor cycles.
- [Applying TDD to Plans](./test-driven-development/applying-tdd-to-plans.md) — Plan creation and plan execution requirements.
- [TDD Shape for Delivery Checklists](./test-driven-development/tdd-shape-for-delivery-checklists.md) — The mandatory RED/GREEN/REFACTOR substep pattern.
- [Gherkin-Tagged Delivery Steps](./test-driven-development/gherkin-tagged-delivery-steps.md) — One cycle per scenario, tag format, exceptions.
- [Enforcement and Exceptions](./test-driven-development/enforcement-and-exceptions.md) — How TDD is enforced, and what it does not apply to.
- [Examples](./test-driven-development/examples.md) — TypeScript, Go, and Gherkin-to-test worked examples.
- [Relationship to Implementation Workflow](./test-driven-development/relationship-to-implementation-workflow.md) — How TDD maps onto the three implementation stages.

## Related Documentation

- [Implementation Workflow Convention](../workflow/implementation.md) - Three-stage workflow that TDD operates inside
- [Three-Level Testing Standard](../quality/three-level-testing-standard.md) - Where TDD-produced tests belong
- [Acceptance Criteria Convention](../infra/acceptance-criteria.md) - Gherkin criteria as the source of first failing tests
- [plan-writing-gherkin-criteria skill](../../../.claude/skills/plan-writing-gherkin-criteria/SKILL.md) - Writing Gherkin scenarios that map to first failing tests
- [BDD Spec-to-Test Mapping Convention](../infra/bdd-spec-test-mapping.md) - Mandatory 1:1 mapping between specs and tests
- [Code Quality Convention](../quality/code.md) - Pre-push hooks that run the test suite TDD produces
- [User-Facing Delivery Hardening Convention](../quality/user-facing-delivery-hardening.md) - Rules on UI-calculation test assertions
