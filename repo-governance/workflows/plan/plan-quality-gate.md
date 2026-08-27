---
name: plan-quality-gate
title: "plan-quality-gate"
description: >
  Iteratively runs plan-checker and plan-fixer against a plan's documents until zero
  threshold-level findings are confirmed on two consecutive checks, or max-iterations is reached.
when_to_use: >
  Use before starting plan execution, after creating or updating a plan, or periodically to
  re-validate plan completeness and technical accuracy.
goal: Validate plan completeness and technical accuracy, apply fixes iteratively until zero findings achieved
termination: "Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: scope
    type: string
    description: Plan files to validate (e.g., "all", "plans/in-progress/", "specific-plan.md")
    required: false
    default: all
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: min-iterations
    type: number
    description: Minimum check-fix cycles before allowing zero-finding termination (prevents premature success)
    required: false
  - name: max-iterations
    type: number
    description: Maximum check-fix cycles to prevent infinite loops
    required: false
    default: 7
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final validation status
  - name: lifecycle-status
    type: enum
    values: [verified, pending, not-applicable]
    description: Lifecycle evidence state, separate from final-status
  - name: iterations-completed
    type: number
    description: Number of check-fix cycles executed
  - name: final-report
    type: file
    pattern: generated-reports/plan__*__audit.md
    description: Final audit report
---

# Plan Quality Gate Workflow

**Purpose**: Automatically validate plan completeness, technical accuracy, and implementation readiness, then apply fixes iteratively until all issues are resolved.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode](./plan-quality-gate/execution-mode.md) — agent delegation vs. manual orchestration.
- [Research Delegation](./plan-quality-gate/research-delegation.md) — when plan-checker delegates to web-researcher.
- [Step 1 — Initial Validation](./plan-quality-gate/step-1-initial-validation.md) — full validation scope.
- [Steps 2-3 — Check for Findings and Apply Fixes](./plan-quality-gate/steps-2-3-check-and-apply-fixes.md) — plan-fixer and its envelope loop.
- [Steps 4-6 — Re-validate, Iteration Control, Finalization](./plan-quality-gate/steps-4-5-6-revalidate-iterate-finalize.md) — the loop logic.
- [Termination Criteria and Delivery-Mode Relationship](./plan-quality-gate/termination-criteria-and-delivery-mode-relationship.md) — pass/partial/fail, and the merge-precondition tie-in.
- [Example Usage](./plan-quality-gate/example-usage.md) — worked invocation examples.
- [Iteration Example and Safety Features](./plan-quality-gate/iteration-example-and-safety-features.md) — convergence walkthrough, safeguards.
- [Plan-Specific Validation — Completeness Through Clarity](./plan-quality-gate/plan-specific-validation-completeness-through-clarity.md) — first half of the checklist.
- [Plan-Specific Validation — Operational Readiness](./plan-quality-gate/plan-specific-validation-operational-readiness.md) — remaining checklist.
- [Final Audit Report Structure and Observability](./plan-quality-gate/final-audit-report-structure-and-observability.md) — report shape, tracked metrics.
- [Related Workflows and Success Metrics](./plan-quality-gate/related-workflows-and-success-metrics.md) — composition, metrics.
- [Notes, Principles, and Conventions](./plan-quality-gate/notes-principles-and-conventions.md) — operational notes, catalog entries.
