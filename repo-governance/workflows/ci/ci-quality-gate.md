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
    pattern: local-tmp/ci/ci__*__audit.md
    description: Final audit report from ci-checker
---

# CI Quality Gate Workflow

**Purpose**: Automatically validate all projects in the repository conform to CI/CD standards
defined in `repo-governance/development/infra/ci-conventions.md`, then iteratively fix non-compliance
until zero findings are achieved.

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Steps](./ci-quality-gate/steps.md) — the five-step check-fix-recheck loop.

## Agents

- [ci-checker](../../../.claude/agents/general/ci-checker.md) — validates all projects against CI/CD standards
- [ci-fixer](../../../.claude/agents/general/ci-fixer.md) — applies validated CI/CD compliance fixes

## Conventions Implemented/Respected

- **[CI/CD Conventions](../../development/infra/ci-conventions.md)**: The standards being validated
- **[Workflow Identifier Convention](../meta/workflow-identifier.md)**: Follows standard workflow structure

## Related Workflows

- [Plan Execution](../plan/plan-execution.md) -- Uses similar iterative check-fix pattern
- [Plan Quality Gate](../plan/plan-quality-gate.md) -- Analogous quality gate for plans

## When to Use

- After adding a new app to the repository
- After modifying CI/CD infrastructure (workflows, composite actions, Docker files)
- As a periodic compliance check
- Before major releases to ensure CI consistency

## Execution Mode

**Preferred Mode**: Agent Delegation — invoke `ci-checker` and `ci-fixer` via the Agent tool
with `subagent_type` (see [Workflow Execution Modes Convention](../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using
Read/Write/Edit tools when Agent Delegation is unavailable.

## Principles Implemented/Respected

- **Explicit Over Implicit**: All CI standards are documented in governance docs, not implicit conventions
- **Automation Over Manual**: Automated checking and fixing reduces manual compliance burden
- **Simplicity Over Complexity**: Simple iterative check-fix loop with bounded iterations
