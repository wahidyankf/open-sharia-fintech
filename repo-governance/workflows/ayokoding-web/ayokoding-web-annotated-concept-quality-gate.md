---
name: ayokoding-web-annotated-concept-quality-gate
title: "ayokoding-web-annotated-concept-quality-gate"
description: Iterative Maker-Checker-Fixer quality gate for Annotated-concept tutorials, validating worked-example count, annotation density, mode integrity, and diagram accessibility.
when_to_use: Use after creating or updating Annotated-concept tutorials, before publishing them to ayokoding-web, or periodically to confirm existing tutorial quality.
goal: Validate Annotated-concept tutorial quality and apply fixes iteratively until EXCELLENT status achieved with zero mechanical issues
termination: "Tutorial achieves EXCELLENT status with 45-60 worked examples (20-30 scenarios for the leadership no-code sub-mode), correct mode integrity, and zero mechanical issues on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: tutorial-path
    type: string
    description: Path to an Annotated-concept tutorial's learning subtree (e.g., "computer-science-foundations/learning/", "engineering-management/learning/")
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
    description: "N+1 background-agent cap. Raise only for independent work with capacity and budget; lower under pressure; never self-promote."
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
    pattern: local-tmp/ayokoding-web-annotated-concept/ayokoding-web-annotated-concept__*__*__audit.md
    description: Final validation report from apps-ayokoding-www-annotated-concept-checker (4-part format with UUID chain)
  - name: fixer-report
    type: file
    pattern: local-tmp/ayokoding-web-annotated-concept/ayokoding-web-annotated-concept__*__*__fix.md
    description: Final fixes report from apps-ayokoding-www-annotated-concept-fixer (4-part format with UUID chain)
  - name: execution-scope
    type: string
    description: Scope identifier for UUID chain tracking (derived from tutorial-path, e.g., "computer-science-foundations" for that topic)
    required: false
  - name: detected-mode
    type: enum
    values: [standard, no-code]
    description: The anatomy mode the checker detected for this topic (standard concept-centric with code, or the leadership no-code sub-mode)
  - name: worked-example-count
    type: number
    description: Total number of worked examples (standard mode) or scenarios (no-code sub-mode) in the tutorial
---

# AyoKoding Content Annotated-Concept Quality Gate Workflow

Iterative Maker-Checker-Fixer quality gate for Annotated-concept tutorials.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode](./ayokoding-web-annotated-concept-quality-gate/execution-mode.md) — Agent Delegation vs. manual fallback.
- [Workflow Overview and Research Delegation](./ayokoding-web-annotated-concept-quality-gate/workflow-overview-and-research-delegation.md) — flow diagram, research delegation.
- [Steps 1-2: Maker and Checker](./ayokoding-web-annotated-concept-quality-gate/step-1-and-2-maker-and-checker.md) — create examples, validate quality.
- [Step 3: User Review](./ayokoding-web-annotated-concept-quality-gate/step-3-user-review.md) — human decision point.
- [Step 4: Fixer](./ayokoding-web-annotated-concept-quality-gate/step-4-fixer.md) — apply validated fixes.
- [Steps 5-6: Iteration Control and Finalization](./ayokoding-web-annotated-concept-quality-gate/step-5-and-6-iteration-control-and-finalization.md) — continue or finalize.
- [Termination Criteria](./ayokoding-web-annotated-concept-quality-gate/termination-criteria.md) — success/partial/failure conditions.
- [Iteration and Strictness Examples](./ayokoding-web-annotated-concept-quality-gate/iteration-and-strictness-examples.md) — two worked walkthroughs.
- [Workflow Invocation and Safety Features](./ayokoding-web-annotated-concept-quality-gate/workflow-invocation-and-safety-features.md) — how to trigger, loop safeguards.
- [Workflow Metadata and References](./ayokoding-web-annotated-concept-quality-gate/workflow-metadata-and-references.md) — metrics, related workflows, principles.
