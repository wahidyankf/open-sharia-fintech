---
title: "Test-Driven Development Convention"
description: "Mandates TDD (Red→Green→Refactor) as the required practice for all code changes across the repository"
when_to_use: "Read this index to find the right Test-Driven Development Convention child document."
---

# Test-Driven Development Convention

- [Principles and Conventions Implemented](./01-principles-and-conventions-implemented.md) — The principles and companion conventions the TDD requirement implements and respects. Use when tracing why TDD is required here back to the principles and conventions it respects.
- [Scope: Which Tests TDD Covers](./02-scope-which-tests-tdd-covers.md) — The ten verification levels TDD applies to, from unit tests through security testing, and the rule for each. Use when deciding which test level (unit, integration, E2E, contract, etc.) a behavior's first failing test belongs at.
- [Manual verification is part of TDD](./03-manual-verification-is-part-of-tdd.md) — The five-step Red/Run/Green/Refactor/Promote cycle for treating a manual verification script like an automated test. Use when a behavior cannot or should not be automated and needs a written, repeatable manual verification script instead.
- [Picking the right level](./04-picking-the-right-level.md) — How to pick the cheapest test level that meaningfully exercises a behavior, and why coverage should not duplicate across levels. Use when unsure which test level a bug or behavior belongs at.
- [The Red-Green-Refactor Cycle](./05-the-red-green-refactor-cycle.md) — The three-step Red/Green/Refactor loop every code change follows under TDD. Use as the canonical definition of the Red-Green-Refactor loop before implementing any code change.
- [Mini-TDD Passes](./06-mini-tdd-passes.md) — Splitting a feature or bug fix into multiple small Red-Green-Refactor cycles instead of one large test. Use when a delivery checklist item like "implement email validation" needs breaking into a sequence of small TDD cycles.
- [Applying TDD to Plans](./07-applying-tdd-to-plans.md) — How plan-maker must express code-shipping delivery items as TDD-shaped steps, and how plan-executor and swe-\*-dev agents follow TDD during execution. Use when authoring a plan's delivery.md checklist, or when executing a delivery item that ships code.
- [TDD Shape for Delivery Checklists](./08-tdd-shape-for-delivery-checklists.md) — The mandatory three-substep RED/GREEN/REFACTOR pattern for code delivery steps, the non-code exception, and the never-combine hard rule. Use when writing a delivery checklist item that ships code, to format it as machine-executable RED/GREEN/REFACTOR substeps.
- [Gherkin-Tagged Delivery Steps](./09-gherkin-tagged-delivery-steps.md) — Why one RED-GREEN-REFACTOR cycle binds exactly one Gherkin scenario, the required tag-line format, the two exceptions, and PASS/FAIL examples. Use when writing a RED step for a plan touching apps/ or libs/ with companion Gherkin specs.
- [Enforcement and Exceptions](./10-enforcement-and-exceptions.md) — How the pre-push hook and plan-checker enforce TDD, and the five kinds of change TDD does not apply to. Use when checking whether TDD's enforcement mechanism would catch a given gap, or whether a change qualifies for an exception.
- [Examples](./11-examples.md) — A TypeScript (Vitest) and Go (Godog) Red-Green-Refactor worked example, and the Gherkin-to-test chain for BDD. Use as a concrete reference for what a Red-Green-Refactor cycle looks like in TypeScript, Go, or from a Gherkin scenario.
- [Relationship to Implementation Workflow](./12-relationship-to-implementation-workflow.md) — How TDD's Red-Green-Refactor loop maps onto the Implementation Workflow's three stages, without adding a fourth stage. Use when explaining how TDD and the three-stage Implementation Workflow fit together.
