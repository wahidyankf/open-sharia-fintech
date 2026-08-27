---
name: rules-quality-gate
title: "rules-quality-gate"
description: "Orchestrated quality gate that runs repo-rules-checker iteratively until zero findings, then applies fixes and re-validates."
when_to_use: "Use after changing conventions/principles/development practices, before major releases, periodically for repo health, or after adding/modifying agents."
goal: Validate repository consistency across all layers, apply fixes iteratively until zero findings achieved
termination: "Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
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
  - name: iterations-completed
    type: number
    description: Number of check-fix cycles executed
  - name: final-report
    type: file
    pattern: generated-reports/repo-rules__*__*__audit.md
    description: Final audit report (4-part format with UUID chain)
  - name: execution-scope
    type: string
    description: Scope identifier for UUID chain tracking (default "repo-rules")
    required: false
---

# Repository Rules Validation Workflow

Automatically validates repository consistency across principles, conventions, development
practices, agent/skill source definitions, and subdirectory README files, then applies fixes
iteratively until all issues are resolved. Validates source only (`repo-governance/`,
`.claude/agents/`, `.claude/skills/`, `docs/explanation/` partially) — see the Purpose and Scope
child below for the full validates/skips breakdown.

## Contents

- [Purpose and Scope](./rules-quality-gate/purpose-and-scope.md) — what's validated vs. skipped.
- [Execution Mode](./rules-quality-gate/execution-mode.md) — Agent Delegation, invocation.
- [Step 0.5: Preflight — Overview](./rules-quality-gate/step-0-5-deterministic-preflight.md) — what the audit orchestrator does.
- [Step 0.5: Preflight — Command](./rules-quality-gate/step-0-5-deterministic-preflight-continued.md) — invocation and exit-code handling.
- [Step 1: Initial Validation](./rules-quality-gate/step-1-initial-validation.md) — the first checker pass.
- [Step 2: Check for Findings](./rules-quality-gate/step-2-check-for-findings.md) — threshold counting.
- [Step 3: Apply Fixes](./rules-quality-gate/step-3-apply-fixes.md) — mode-scoped fixing.
- [Step 4: Re-validate](./rules-quality-gate/step-4-re-validate.md) — preflight + checker re-run.
- [Step 5: Iteration Control](./rules-quality-gate/step-5-iteration-control.md) — loop/terminate logic.
- [Step 6: Finalization](./rules-quality-gate/step-6-finalization.md) — final status reporting.
- [Termination Criteria](./rules-quality-gate/termination-criteria.md) — pass/partial/fail by mode.
- [Example Usage](./rules-quality-gate/example-usage.md) — normal/strict/ocd/bounded invocations.
- [Iteration Example](./rules-quality-gate/iteration-example.md) — a worked four-iteration trace.
- [Safety Features](./rules-quality-gate/safety-features.md) — loop, convergence, and fix safeguards.
- [Skip-list Curation Rules](./rules-quality-gate/skip-list-curation-rules.md) — the false-positives file.
- [Related Workflows](./rules-quality-gate/related-workflows.md) — deployment/release/content gates.
- [Observability Metrics](./rules-quality-gate/observability-metrics.md) — the nine tracked metrics.
- [Notes](./rules-quality-gate/notes.md) — automation posture, idempotency, terminology.
- [Backlog](./rules-quality-gate/backlog.md) — extending scope to all of docs/.
- [Principles Implemented/Respected](./rules-quality-gate/principles-implemented-respected.md) — traceability.
- [Conventions Implemented/Respected](./rules-quality-gate/conventions-implemented-respected.md) — traceability.
- [What Changed](./rules-quality-gate/what-changed.md) — the Step 0.5 changelog.
