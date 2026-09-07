---
description: Three-stage development workflow - make it work, make it right, make it fast
when_to_use: Use when planning or reviewing any code change, to sequence work-then-right-then-fast and to apply surgical scoping and goal-driven verification.
---

# Implementation Workflow

**Make it work, make it right, make it fast** - a three-stage development workflow that prioritizes functionality first, quality second, and optimization last (only when proven necessary), plus two cross-cutting practices: Surgical Changes and Goal-Driven Execution.

## Contents

- [Workflow Overview, Principles, and Conventions](./implementation/workflow-overview-principles-and-conventions.md) — The three stages, and what the workflow implements/respects.
- [Stage 1: Make It Work](./implementation/stage-1-make-it-work.md) — Simplest solution that passes tests.
- [Stage 2: Make It Right](./implementation/stage-2-make-it-right.md) — Refactor for readability and maintainability.
- [Stage 3: Make It Fast (If Needed)](./implementation/stage-3-make-it-fast.md) — Profile-driven optimization only.
- [Surgical Changes — Principle](./implementation/surgical-changes-principle.md) — Touch only what you must, and the four core rules.
- [Surgical Changes — Application Examples](./implementation/surgical-changes-application-examples.md) — Worked bug-fix and validation examples.
- [Surgical Changes — Orphans, Checklist, and Application](./implementation/surgical-changes-orphans-checklist-and-application.md) — Cleaning up your own orphans and the pre-commit checklist.
- [Goal-Driven Execution — Defining and Planning Goals](./implementation/goal-driven-execution-defining-and-planning-goals.md) — Turning tasks into verifiable goals and multi-step plans.
- [Goal-Driven Execution — Verification and Iteration](./implementation/goal-driven-execution-verification-and-iteration.md) — Test-first development and looping until verified.
- [Goal-Driven Execution — Application Examples](./implementation/goal-driven-execution-application-examples.md) — A worked API endpoint and a worked bug fix.
- [Goal-Driven Execution — Checklist and Relationship](./implementation/goal-driven-execution-checklist-and-relationship.md) — The before/during checklist and principle traceability.
- [Anti-Patterns](./implementation/anti-patterns.md) — Four failure modes around premature and unmeasured optimization.
- [Best Practices](./implementation/best-practices.md) — Six practices from starting simple to re-measuring.
- [When to Apply and References](./implementation/when-to-apply-and-references.md) — Where this workflow applies, its exceptions, and further reading.

## Related Documentation

- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) — the start-simple principle this workflow's Stage 1 implements.
- [Root Cause Orientation](../../principles/general/root-cause-orientation.md) — surgical changes implement the minimal-impact practice from this principle.
- [Code Quality Convention](../quality/code.md) — automated quality checks applied in Stage 2.
- [Trunk Based Development](../workflow/trunk-based-development.md) — the git workflow this practice runs inside.
- [Acceptance Criteria Convention](../infra/acceptance-criteria.md) — defining "works" in Stage 1.
- [Agent Workflow Orchestration](../agents/agent-workflow-orchestration.md) — how agents apply this workflow in multi-step task execution.
