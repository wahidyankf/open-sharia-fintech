---
name: ci-quality-gate
title: "ci-quality-gate"
description: Validates all projects conform to CI/CD standards and iteratively fixes non-compliance until zero findings are confirmed twice.
when_to_use: Use after adding a new app, modifying CI/CD infrastructure, as a periodic compliance check, or before major releases.
goal: Validate all projects conform to CI/CD standards and fix non-compliance iteratively
termination: "Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: scope
    type: string
    description: Scope of validation - "all" for all projects, or specific project name
    required: false
    default: all
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: max-iterations
    type: number
    description: Maximum number of check-fix cycles
    required: false
    default: 7
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
    description: Number of check-fix cycles performed
  - name: final-report
    type: file
    pattern: generated-reports/ci__*__audit.md
    description: Final audit report from ci-checker
---

# CI Quality Gate Workflow

**Purpose**: Automatically validate all projects in the repository conform to CI/CD standards
defined in `repo-governance/development/infra/ci-conventions.md`, then iteratively fix non-compliance
until zero findings are achieved.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [When to Use](./ci-quality-gate/when-to-use.md) — the four triggers.
- [Execution Mode](./ci-quality-gate/execution-mode.md) — preferred/fallback execution.
- [Steps](./ci-quality-gate/steps.md) — the five-step check-fix-recheck loop.
- [Related Workflows](./ci-quality-gate/related-workflows.md) — other workflows with a similar pattern.
- [Principles Implemented/Respected](./ci-quality-gate/principles-implemented-respected.md) — the principles this gate embodies.
- [Conventions Implemented/Respected](./ci-quality-gate/conventions-implemented-respected.md) — the conventions this gate enforces.
- [Agents](./ci-quality-gate/agents.md) — `ci-checker` and `ci-fixer`.
