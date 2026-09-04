---
name: ayokoding-web-in-the-field-quality-gate
title: "ayokoding-web-in-the-field-quality-gate"
description: Iterative Maker-Checker-Fixer quality gate for in-the-field production guides, validating guide count, standard-library-first ordering, annotation density, and production code quality.
when_to_use: Use after creating or updating in-the-field production guides, before publishing them, or periodically to confirm production code quality.
goal: Validate in-the-field production guide quality and apply fixes iteratively until EXCELLENT status achieved with zero mechanical issues
termination: "Tutorial achieves EXCELLENT status with 20-40 guides, production code quality, and zero mechanical issues on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: tutorial-path
    type: string
    description: Path to in-the-field tutorials (e.g., "java/in-the-field/", "golang/in-the-field/")
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
    pattern: local-tmp/ayokoding-web-in-the-field/ayokoding-web-in-the-field__*__*__audit.md
    description: Final validation report from apps-ayokoding-www-in-the-field-checker (4-part format with UUID chain)
  - name: fixer-report
    type: file
    pattern: local-tmp/ayokoding-web-in-the-field/ayokoding-web-in-the-field__*__*__fix.md
    description: Final fixes report from apps-ayokoding-www-in-the-field-fixer (4-part format with UUID chain)
  - name: execution-scope
    type: string
    description: Scope identifier for UUID chain tracking (derived from tutorial-path, e.g., "java" for Java tutorials)
    required: false
  - name: guides-count
    type: number
    description: Total number of production guides
  - name: production-coverage
    type: string
    description: Production scenarios covered
---

# AyoKoding Content In-the-Field Quality Gate Workflow

Iterative Maker-Checker-Fixer quality gate for in-the-field production guides.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode, Workflow Overview, and Research Delegation](./ayokoding-web-in-the-field-quality-gate/execution-mode-workflow-overview-and-research-delegation.md) — how to run, flow diagram.
- [Steps 1-2: Maker and Checker](./ayokoding-web-in-the-field-quality-gate/step-1-and-2-maker-and-checker.md) — create guides, validate quality.
- [Step 3: User Review](./ayokoding-web-in-the-field-quality-gate/03-user-review.md) — human decision point.
- [Step 4: Fixer](./ayokoding-web-in-the-field-quality-gate/04-fixer.md) — apply validated fixes.
- [Steps 5-6: Iteration Control and Finalization](./ayokoding-web-in-the-field-quality-gate/05-iteration-control-and-finalization.md) — continue or finalize.
- [Termination Criteria and Safety Features](./ayokoding-web-in-the-field-quality-gate/termination-criteria-and-safety-features.md) — success conditions, loop safeguards.
- [Related Workflows, Principles, Conventions, and Documentation](./ayokoding-web-in-the-field-quality-gate/related-workflows-principles-conventions-and-documentation.md) — cross-references.
