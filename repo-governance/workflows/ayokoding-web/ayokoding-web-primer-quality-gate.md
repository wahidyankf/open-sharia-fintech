---
description: Iterative Maker-Checker-Fixer quality gate for Primer ("Just Enough X") tutorials, validating example count, annotation density, and scope discipline.
when_to_use: Use after creating or updating a Primer tutorial, before publishing it, or when a primer's dependent topics change and its scope needs re-verification.
---

# AyoKoding Content Primer Quality Gate Workflow

Iterative Maker-Checker-Fixer quality gate for Primer ("Just Enough X") tutorials.

## Goal and Termination

**Goal**: Validate Primer ("Just Enough X") tutorial quality and apply fixes iteratively until EXCELLENT status achieved with zero mechanical issues

**Termination**: Primer achieves EXCELLENT status with 75-85 examples authored at By-Example pace, verified scope discipline, and zero mechanical issues on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)

## Inputs

- **`tutorial-path`** (string, required) — Path to a Primer tutorial's learning subtree (e.g., "just-enough-go/learning/", "just-enough-rust/learning/")
- **`mode`** (enum: lax, normal, strict, ocd, optional, default `strict`) — Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)
- **`min-iterations`** (number, optional) — Minimum check-fix cycles before allowing zero-finding termination (prevents premature success)
- **`max-iterations`** (number, optional, default `7`) — Maximum check-fix cycles to prevent infinite loops
- **`max-concurrency`** (number, optional, default `3`) — N+1 background-agent cap. Raise only for independent work with capacity and budget; lower under pressure; never self-promote.
- **`auto-fix-level`** (enum: high-only, high-and-medium, all, optional, default `high-only`) — Which confidence levels to auto-fix without user approval

## Outputs

- **`final-status`** (enum: excellent, needs-improvement, failing) — Final tutorial quality status
- **`lifecycle-status`** (enum: verified, pending, not-applicable) — Lifecycle evidence state, separate from final-status
- **`iterations-completed`** (number) — Number of check-fix cycles executed
- **`checker-report`** (file, pattern `local-tmp/ayokoding-web-primer/ayokoding-web-primer__*__*__audit.md`) — Final validation report from apps-ayokoding-www-primer-checker (4-part format with UUID chain)
- **`fixer-report`** (file, pattern `local-tmp/ayokoding-web-primer/ayokoding-web-primer__*__*__fix.md`) — Final fixes report from apps-ayokoding-www-primer-fixer (4-part format with UUID chain)
- **`execution-scope`** (string) — Scope identifier for UUID chain tracking (derived from tutorial-path, e.g., "just-enough-go" for that primer)
- **`examples-count`** (number) — Total number of examples in the primer
- **`scope-discipline-status`** (enum: clean, scope-creep-flagged) — Whether the checker found examples drifting beyond the "just enough to be productive" boundary

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode](./ayokoding-web-primer-quality-gate/execution-mode.md) — Agent Delegation vs. manual fallback.
- [Workflow Overview and Research Delegation](./ayokoding-web-primer-quality-gate/workflow-overview-and-research-delegation.md) — flow diagram, research delegation.
- [Steps 1-2: Maker and Checker](./ayokoding-web-primer-quality-gate/step-1-and-2-maker-and-checker.md) — create examples, validate quality.
- [Step 3: User Review](./ayokoding-web-primer-quality-gate/step-3-user-review.md) — human decision point.
- [Step 4: Fixer](./ayokoding-web-primer-quality-gate/step-4-fixer.md) — apply validated fixes.
- [Steps 5-6: Iteration Control and Finalization](./ayokoding-web-primer-quality-gate/step-5-and-6-iteration-control-and-finalization.md) — continue or finalize.
- [Termination Criteria](./ayokoding-web-primer-quality-gate/termination-criteria.md) — success/partial/failure conditions.
- [Iteration and Strictness Examples](./ayokoding-web-primer-quality-gate/iteration-and-strictness-examples.md) — two worked walkthroughs.
- [Workflow Invocation and Safety Features](./ayokoding-web-primer-quality-gate/workflow-invocation-and-safety-features.md) — how to trigger, loop safeguards.
- [Workflow Metadata and References](./ayokoding-web-primer-quality-gate/workflow-metadata-and-references.md) — metrics, related workflows, principles.
