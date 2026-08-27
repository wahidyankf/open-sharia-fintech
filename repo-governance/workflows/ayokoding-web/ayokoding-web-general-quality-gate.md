---
name: ayokoding-web-general-quality-gate
title: "ayokoding-web-general-quality-gate"
description: Fully automated quality gate that validates ayokoding-web content quality, factual accuracy, and links in parallel, then applies fixes iteratively until zero findings.
when_to_use: Use after creating or updating ayokoding-web content, before deploying to production, or periodically to confirm content quality and accuracy.
goal: Validate all ayokoding-web content quality, apply fixes iteratively until zero findings
termination: "Zero findings across all validators on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: scope
    type: string
    description: Content to validate (e.g., "all", "ayokoding-web/content/en/", "specific-file.md")
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
  - name: content-report
    type: file
    pattern: generated-reports/ayokoding-web-general__*__audit.md
    description: Final content validation report
  - name: facts-report
    type: file
    pattern: generated-reports/ayokoding-web-facts__*__audit.md
    description: Final facts validation report
  - name: links-report
    type: file
    pattern: generated-reports/ayokoding-web-link__*__audit.md
    description: Final links validation report
---

# AyoKoding Content General Quality Gate Workflow

Fully automated workflow that validates all ayokoding-web content (quality, facts, links) and iteratively fixes findings.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode and Research Delegation](./ayokoding-web-general-quality-gate/execution-mode-and-research-delegation.md) — Agent Delegation vs. manual, research delegation.
- [Steps 1-2: Parallel Validation and Aggregate Findings](./ayokoding-web-general-quality-gate/step-1-and-2-parallel-validation-and-aggregate-findings.md) — run checkers, count findings.
- [Steps 3-4: Apply Content and Facts Fixes](./ayokoding-web-general-quality-gate/03-apply-fixes.md) — the two fixer steps.
- [Steps 5-7: Iteration Control, Final Validation, and Finalization](./ayokoding-web-general-quality-gate/step-5-to-7-iteration-final-validation-finalization.md) — continue, confirm, report.
- [Termination Criteria and Example Usage](./ayokoding-web-general-quality-gate/termination-criteria-and-example-usage.md) — pass/partial/fail, invocation examples.
- [Iteration Example and Safety Features](./ayokoding-web-general-quality-gate/iteration-example-and-safety-features.md) — worked flow, loop safeguards.
- [Validation Dimensions, Related Workflows, and Success Metrics](./ayokoding-web-general-quality-gate/validation-dimensions-related-workflows-and-success-metrics.md) — what each validator checks.
- [Notes, Principles, and Conventions Implemented](./ayokoding-web-general-quality-gate/notes-principles-and-conventions.md) — operational notes, principles, conventions.
