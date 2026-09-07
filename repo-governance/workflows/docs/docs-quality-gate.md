---
description: "Validates all docs/ content (factual accuracy, pedagogical structure, link validity) and applies fixes iteratively via Maker-Checker-Fixer."
when_to_use: "Use after creating/updating documentation, before releases, periodically, or after bulk restructuring."
---

# Documentation Quality Gate Workflow

**Purpose**: Comprehensively validate all documentation content (factual accuracy, pedagogical
structure, link validity), apply fixes iteratively until all issues are resolved.

**When to use**: after creating or updating documentation, before major releases, periodically for
quality assurance, after bulk documentation changes, or when migrating/refactoring documentation.

This workflow implements the **Maker-Checker-Fixer pattern** across three validation dimensions.

## Goal and Termination

**Goal**: Validate all docs/ content quality (factual accuracy, pedagogical structure, link validity), apply fixes iteratively until zero findings achieved

**Termination**: Zero findings across all validators on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)

## Inputs

- **`scope`** (string, optional, default `all`) — Documentation to validate (e.g., "all", "docs/tutorials/", "specific-file.md")
- **`mode`** (enum: lax, normal, strict, ocd, optional, default `strict`) — Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)
- **`min-iterations`** (number, optional) — Minimum check-fix cycles before allowing zero-finding termination (prevents premature success)
- **`max-iterations`** (number, optional, default `7`) — Maximum check-fix cycles to prevent infinite loops
- **`max-concurrency`** (number, optional, default `3`) — N+1 background-agent cap. Raise only for independent work with capacity and budget; lower under pressure; never self-promote.

## Outputs

- **`final-status`** (enum: pass, partial, fail) — Final validation status
- **`lifecycle-status`** (enum: verified, pending, not-applicable) — Lifecycle evidence state, separate from final-status
- **`iterations-completed`** (number) — Number of check-fix cycles executed
- **`docs-report`** (file, pattern `local-tmp/docs/docs__*__audit.md`) — Final factual accuracy validation report
- **`tutorial-report`** (file, pattern `local-tmp/docs-tutorial/docs-tutorial__*__audit.md`) — Final pedagogical quality validation report
- **`links-report`** (file, pattern `local-tmp/docs-link/docs-link__*__audit.md`) — Final link validity validation report
- **`execution-scope`** (string) — Scope identifier for UUID chain tracking (default "docs")

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode](./docs-quality-gate/execution-mode.md) — delegation vs. manual mode.
- [Workflow Overview](./docs-quality-gate/workflow-overview.md) — flow diagram.
- [Research Delegation](./docs-quality-gate/research-delegation.md) — web-researcher hand-off.

### Steps

- [Step 1: Parallel Validation](./docs-quality-gate/step-1-parallel-validation.md) — three checkers.
- [Step 2: Aggregate Findings](./docs-quality-gate/step-2-aggregate-findings.md) — threshold decision.
- [Step 3: Apply Factual Fixes](./docs-quality-gate/step-3-apply-factual-fixes.md) — docs-fixer.
- [Step 4: Apply Pedagogical Fixes](./docs-quality-gate/step-4-apply-pedagogical-fixes.md) — docs-tutorial-fixer.
- [Step 5: Iteration Control](./docs-quality-gate/step-5-iteration-control.md) — loop logic.
- [Step 6: Finalization](./docs-quality-gate/step-6-finalization.md) — final status.

### Criteria and Examples

- [Termination Criteria](./docs-quality-gate/termination-criteria.md) — pass/partial/fail rules.
- [Example Usage](./docs-quality-gate/example-usage.md) — invocation scenarios.
- [Iteration Example](./docs-quality-gate/iteration-example.md) — worked trace with broken links.

### Reference

- [Safety Features](./docs-quality-gate/safety-features.md) — convergence safeguards.
- [Validation Dimensions](./docs-quality-gate/validation-dimensions.md) — what each validator checks.
- [Edge Cases](./docs-quality-gate/edge-cases.md) — five worked edge cases.
- [Related Workflows](./docs-quality-gate/related-workflows.md) — composable workflows.
- [Success Metrics](./docs-quality-gate/success-metrics.md) — operational tracking.
- [Notes](./docs-quality-gate/notes.md) — key operating characteristics.
- [Principles Respected](./docs-quality-gate/principles-implemented-respected.md) — governance.
- [Conventions Respected](./docs-quality-gate/conventions-implemented-respected.md) — governance.
