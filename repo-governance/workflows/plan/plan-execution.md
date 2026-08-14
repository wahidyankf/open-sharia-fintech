---
name: plan-execution
title: "plan-execution"
description: Executes a project plan end-to-end — orchestration, delegation, quality gates, iteration, archival — split into per-topic children.
when_to_use: Use when executing a plan, or looking up one step (worktree entry, a quality gate, finalization) of that execution.
goal: Execute a project plan, validate its completion and quality, then iteratively continue until all requirements are met and archive to plans/done/
termination: Zero findings remain after validation and plan moved to done/
inputs:
  - name: plan-path
    type: string
    description: Path to the plan file to execute (e.g., "plans/in-progress/new-feature/plan.md")
    required: true
  - name: max-iterations
    type: number
    description: Maximum number of execute-check cycles to prevent infinite loops
    required: false
    default: 10
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final execution and validation status
  - name: iterations-completed
    type: number
    description: Number of execute-check cycles performed
  - name: final-report
    type: file
    pattern: generated-reports/plan-execution__*__validation.md
    description: Final validation report from plan-execution-checker
---

# Plan Execution Workflow

**Purpose**: Execute a plan, iterate to zero findings, archive to `plans/done/`.

> **Pre-Execution Requirement**: invoke `grill-me` first, per
> [Grilling-With-Options](../../development/workflow/grilling-with-options.md).

## Contents

- [Execution Mode](./plan-execution/01-execution-mode.md) — orchestrator role.
- [How to Execute](./plan-execution/02-how-to-execute.md) — 12 actions.
- [Orchestration Model](./plan-execution/03-orchestration-model.md) — delegation rule.
- [Agent Selection](./plan-execution/04-agent-selection.md) — picking heuristics.
- [Fan-Out Shape](./plan-execution/05-fan-out-ordering-and-delivery-shape.md) — N+1, DAG.
- [Tester Gates](./plan-execution/06-surface-conditional-tester-gates.md) — per-surface.
- [Vercel MCP](./plan-execution/07-vercel-mcp-availability.md) — Phase 0 check.
- [Task-Checklist Sync](./plan-execution/08-task-checklist-synchronization.md) — 1:1 mapping.
- [Harness Task List](./plan-execution/09-harness-task-list-primary-observability-surface.md) — invariants.
- [Sync Ritual](./plan-execution/10-atomic-sync-ritual.md) — tick/notes/update.
- [Resume Reconciliation](./plan-execution/11-resume-reconciliation.md) — disk truth.
- [Iron Rules 1-5](./plan-execution/12-iron-rules-1-5.md) — task tracking.
- [Iron Rules 6-11](./plan-execution/13-iron-rules-6-11.md) — file-touch ledger.
- [Preconditions](./plan-execution/14-enter-worktree-preconditions-and-work-branch.md) — branch precedence.
- [Delivery-Mode](./plan-execution/15-enter-worktree-delivery-mode-resolution.md) — mode precedence.
- [Locate/Provision](./plan-execution/16-enter-worktree-locate-and-provision.md) — auto-provision.
- [Freshness Gate](./plan-execution/17-enter-worktree-freshness-gate.md) — pull latest.
- [Secrets/Rationale](./plan-execution/18-enter-worktree-secrets-output-and-rationale.md) — infra ops.
- [Load Checklist](./plan-execution/19-load-delivery-checklist-and-task-list.md) — task materialize.
- [Environment Setup](./plan-execution/20-environment-setup.md) — Phase 0.
- [Execution Loop](./plan-execution/21-initial-execution-loop.md) — items 1-4.
- [Verify/Sync](./plan-execution/22-initial-execution-items-5-8.md) — items 5-8.
- [Progress/Stopping](./plan-execution/23-initial-execution-progress-and-stopping-rules.md) — item 9.
- [Gates](./plan-execution/24-per-phase-quality-gate-gates.md) — Phase N Gate.
- [Push Targets](./plan-execution/25-per-phase-quality-gate-push-targets.md) — mode push.
- [Phase 0/Merging](./plan-execution/26-per-phase-quality-gate-phase0-and-boundary-merging.md) — boundary merge.
- [Cleanup Check](./plan-execution/27-per-phase-quality-gate-cleanup-and-invariant.md) — boundary assert.
- [CI Overview](./plan-execution/28-post-push-ci-verification-overview.md) — monitoring tool.
- [CI Direct-Push](./plan-execution/29-post-push-ci-verification-direct-push.md) — main CI.
- [CI PR-Branch](./plan-execution/30-post-push-ci-verification-pr-branch.md) — PR checks.
- [Assertions Web/API](./plan-execution/31-manual-behavioral-assertions-web-and-api.md) — Playwright/curl.
- [Assertions Evidence](./plan-execution/32-manual-behavioral-assertions-full-stack-and-evidence.md) — full-stack.
- [Validation](./plan-execution/33-validation-and-check-for-findings.md) — checker run.
- [Continue Execution](./plan-execution/34-continue-execution.md) — fix findings.
- [Re-validate](./plan-execution/35-revalidate-and-iteration-control.md) — loop/terminate.
- [Pre-Archival Gates](./plan-execution/36-finalization-pre-archival-gates.md) — rule-15.
- [Rule-16 Retest](./plan-execution/37-finalization-rule16-api-retest.md) — API retest.
- [Knowledge Capture](./plan-execution/38-finalization-knowledge-capture.md) — learnings.md.
- [PR-Review Gate](./plan-execution/39-finalization-pr-review-gate.md) — done-definition.
- [Status/Infra Gate](./plan-execution/40-finalization-status-logic-and-infra-gate.md) — pass/fail.
- [Cleanup/Archival](./plan-execution/41-finalization-worktree-cleanup-and-pr-archival.md) — archival-in-PR.
- [PR Merge/Status](./plan-execution/42-finalization-pr-merge-and-final-status.md) — merge/cleanup.
- [Task Rules](./plan-execution/43-task-management-rules-and-termination.md) — termination.
- [Example Usage](./plan-execution/44-example-usage-and-iteration-example.md) — invocations.
- [Safety Features](./plan-execution/45-safety-features-and-plan-specific-validation.md) — checker scope.
- [Related Workflows](./plan-execution/46-related-workflows-and-success-metrics.md) — metrics.
- [Notes](./plan-execution/47-notes.md) — characteristics.
- [TDD/Principles](./plan-execution/48-tdd-principles-conventions-agents.md) — governance.
