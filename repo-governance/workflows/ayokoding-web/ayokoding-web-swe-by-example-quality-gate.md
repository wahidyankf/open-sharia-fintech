---
name: ayokoding-web-swe-by-example-quality-gate
title: "ayokoding-web-swe-by-example-quality-gate"
description: Iterative Maker-Checker-Fixer quality gate for by-example tutorials, validating coverage, example count, annotation density, and the mandatory Examples-by-Level section.
when_to_use: Use after creating or updating by-example tutorials, before publishing them, or periodically to confirm tutorial quality remains high.
goal: Validate by-example tutorial quality and apply fixes iteratively until EXCELLENT status achieved with zero mechanical issues
termination: "Tutorial achieves EXCELLENT status with 75-85 examples, 95% coverage, and zero mechanical issues on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: tutorial-path
    type: string
    description: Path to by-example tutorial (e.g., "golang/tutorials/by-example/", "elixir/tutorials/by-example/")
    required: true
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
  - name: auto-fix-level
    type: enum
    values: [high-only, high-and-medium, all]
    description: Which confidence levels to auto-fix without user approval
    required: false
    default: high-only
outputs:
  - name: final-status
    type: enum
    values: [excellent, needs-improvement, failing]
    description: Final tutorial quality status
  - name: lifecycle-status
    type: enum
    values: [verified, pending, not-applicable]
    description: Lifecycle evidence state, separate from final-status
  - name: iterations-completed
    type: number
    description: Number of check-fix cycles executed
  - name: checker-report
    type: file
    pattern: generated-reports/ayokoding-web-by-example__*__*__audit.md
    description: Final validation report from apps-ayokoding-www-by-example-checker (4-part format with UUID chain)
  - name: fixer-report
    type: file
    pattern: generated-reports/ayokoding-web-by-example__*__*__fix.md
    description: Final fixes report from apps-ayokoding-www-by-example-fixer (4-part format with UUID chain)
  - name: execution-scope
    type: string
    description: Scope identifier for UUID chain tracking (derived from tutorial-path, e.g., "golang" for golang tutorials)
    required: false
  - name: examples-count
    type: number
    description: Total number of examples in tutorial
  - name: coverage-percentage
    type: number
    description: Estimated coverage percentage achieved
---

# AyoKoding Content By-Example Quality Gate Workflow

Iterative Maker-Checker-Fixer quality gate for by-example tutorials.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode, Workflow Overview, and Research Delegation](./ayokoding-web-swe-by-example-quality-gate/execution-mode-workflow-overview-and-research-delegation.md) — how to run, flow diagram.
- [Steps 1-2: Maker and Checker](./ayokoding-web-swe-by-example-quality-gate/step-1-and-2-maker-and-checker.md) — create examples, validate quality.
- [Step 3: User Review](./ayokoding-web-swe-by-example-quality-gate/03-user-review.md) — human decision point.
- [Step 4: Fixer](./ayokoding-web-swe-by-example-quality-gate/04-fixer.md) — apply validated fixes.
- [Steps 5-6: Iteration Control and Finalization](./ayokoding-web-swe-by-example-quality-gate/05-iteration-control-and-finalization.md) — continue or finalize.
- [Termination Criteria](./ayokoding-web-swe-by-example-quality-gate/termination-criteria.md) — success/partial/failure conditions.
- [Iteration Examples 1-2](./ayokoding-web-swe-by-example-quality-gate/iteration-examples-1-and-2.md) — clean-path and issue-path walkthroughs.
- [Iteration Example 3](./ayokoding-web-swe-by-example-quality-gate/iteration-example-3.md) — major-rework failing-path walkthrough.
- [Strictness Examples 4-6](./ayokoding-web-swe-by-example-quality-gate/strictness-examples.md) — normal, strict, and ocd modes.
- [Workflow Invocation and Safety Features](./ayokoding-web-swe-by-example-quality-gate/workflow-invocation-and-safety-features.md) — how to trigger, loop safeguards.
- [Workflow Metadata and References](./ayokoding-web-swe-by-example-quality-gate/workflow-metadata-and-references.md) — metrics, related workflows, principles.
