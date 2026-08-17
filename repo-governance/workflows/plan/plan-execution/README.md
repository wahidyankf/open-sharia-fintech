---
title: "Plan Execution Workflow"
description: "Executes a project plan end-to-end — orchestration, delegation, quality gates, iteration, archival — split into per-topic children."
when_to_use: "Read this index to find the right Plan Execution Workflow child document."
---

# Plan Execution Workflow

- [Execution Mode](./01-execution-mode.md) — Explains that the calling context, not a dedicated plan-executor
- [How to Execute](./02-how-to-execute.md) — Lists the 12 top-level actions (0-11) the calling context
- [Orchestration Model](./03-orchestration-model.md) — States that the calling context orchestrates plan execution, routing
- [Agent Selection](./04-agent-selection.md) — Defines the priority-ordered heuristics the orchestrator uses to pick
- [Fan-Out, Ordering, and Delivery Shape](./05-fan-out-ordering-and-delivery-shape.md) — Defines the N+1 fan-out model, DAG-first ordering, and the
- [Surface-Conditional Tester Gates](./06-surface-conditional-tester-gates.md) — States which quality gates a plan must run based
- [Vercel MCP Availability (Surface-Conditional)](./07-vercel-mcp-availability.md) — Defines how execution reconfirms Vercel MCP availability at Phase
- [Task-Checklist Synchronization](./08-task-checklist-synchronization.md) — Establishes that the live Task list and on-disk delivery.md
- [Harness Task List as Primary Observability Surface](./09-harness-task-list-primary-observability-surface.md) — Defines the non-negotiable invariants for the harness Task list
- [Atomic Sync Ritual](./10-atomic-sync-ritual.md) — Defines the mandatory three-step tick-notes-TaskUpdate sequence that must land
- [Resume Reconciliation (Disk Is Truth)](./11-resume-reconciliation.md) — Defines how execution rebuilds the Task list from delivery.md
- [Iron Rules (Non-Negotiable) — Rules 1-5](./12-iron-rules-1-5.md) — States the first five non-negotiable execution rules: granular task
- [Iron Rules (Non-Negotiable) — Rules 6-11](./13-iron-rules-6-11.md) — States the remaining six non-negotiable execution rules: CI verification,
- [Enter the Designated Worktree — Preconditions and Work Branch](./14-enter-worktree-preconditions-and-work-branch.md) — Defines the backlog-promotion precondition and the three-tier precedence for
- [Enter the Designated Worktree — Delivery-Mode Resolution](./15-enter-worktree-delivery-mode-resolution.md) — Defines the three-tier precedence for resolving a plan's delivery
- [Enter the Designated Worktree — Locate and Provision](./16-enter-worktree-locate-and-provision.md) — Defines how the orchestrator locates the plan's declared Use
- [Enter the Designated Worktree — Freshness Gate](./17-enter-worktree-freshness-gate.md) — Defines the mandatory pull-latest-origin/main freshness gate that must pass
- [Enter the Designated Worktree — Secrets, Output, and Rationale](./18-enter-worktree-secrets-output-and-rationale.md) — Explains why secret- and state-dependent infra operations must run
- [Load Delivery Checklist and Materialize Task List](./19-load-delivery-checklist-and-task-list.md) — Defines how the orchestrator reads the plan, reconciles prior-run
- [Environment Setup](./20-environment-setup.md) — Defines Phase 0's environment-setup responsibilities and the hard rule
- [Initial Execution — Execution Loop](./21-initial-execution-loop.md) — Defines the single-item, strictly sequential execution loop's first four
- [Initial Execution — Verify, Capture, and Atomic Sync](./22-initial-execution-items-5-8.md) — Defines execution-loop steps 5-8: performing the item, verifying the
- [Initial Execution — Progress, Output, and Stopping Rules](./23-initial-execution-progress-and-stopping-rules.md) — Defines execution-loop step 9, progress-streaming cadence, success/failure criteria, and
- [Per-Phase Quality Gate — Gates](./24-per-phase-quality-gate-gates.md) — Defines the Phase N Gate barrier check and the
- [Per-Phase Quality Gate — Push Targets](./25-per-phase-quality-gate-push-targets.md) — Defines the push target per delivery mode and the
- [Per-Phase Quality Gate — Phase 0 Exemption and Delivery-Boundary Merging](./26-per-phase-quality-gate-phase0-and-boundary-merging.md) — Defines Phase 0's exemption from pushing or opening a
- [Per-Phase Quality Gate — Worktree Cleanup and Boundary Assertion](./27-per-phase-quality-gate-cleanup-and-invariant.md) — Defines when a repo's shared worktree may be removed,
- [Post-Push CI Verification — Overview and Monitoring Tool](./28-post-push-ci-verification-overview.md) — Defines when Post-Push CI Verification applies and the required
- [Post-Push CI Verification — Direct-Push Modes](./29-post-push-ci-verification-direct-push.md) — Defines how execution monitors and resolves failures for GitHub
- [Post-Push CI Verification — PR-Branch Modes](./30-post-push-ci-verification-pr-branch.md) — Defines how execution monitors and resolves failures for GitHub
- [Manual Behavioral Assertions — Web UI and API Verification](./31-manual-behavioral-assertions-web-and-api.md) — Defines the mandatory post-CI manual verification of web UI
- [Manual Behavioral Assertions — Full-Stack Verification and Evidence](./32-manual-behavioral-assertions-full-stack-and-evidence.md) — Defines full-stack verification covering both UI and API, and
- [Validation](./33-validation-and-check-for-findings.md) — Defines the plan-execution-checker validation step and how its findings
- [Continue Execution](./34-continue-execution.md) — Defines the finding-remediation execution loop that delegates each validation
- [Re-validate](./35-revalidate-and-iteration-control.md) — Defines the re-validation step and the iteration-control logic that
- [Finalization and Archival — Pre-Archival Gates](./36-finalization-pre-archival-gates.md) — Defines the UI- and API-bearing plan pre-archival gates and
- [Finalization and Archival — Rule-16 API Retest Gate](./37-finalization-rule16-api-retest.md) — Defines the rule-16 API exploratory retest gate that runs
- [Finalization and Archival — Knowledge Capture Gate](./38-finalization-knowledge-capture.md) — Defines the mandatory Knowledge Capture pre-archival gate requiring every
- [Finalization and Archival — PR-Review Maker→Fixer Cycle Gate](./39-finalization-pr-review-gate.md) — Defines the mandatory PR-Review Maker→Fixer Cycle gate and its
- [Finalization and Archival — Status Logic, Infra-Execution Gate, and Direct-Push Archival](./40-finalization-status-logic-and-infra-gate.md) — Defines the pass/partial/fail branching logic, the Infra-Execution Gate precondition,
- [Finalization and Archival — Direct-Push Worktree Cleanup and PR-Mode Archival](./41-finalization-worktree-cleanup-and-pr-archival.md) — Defines the prompted worktree-cleanup flow for direct-push modes and
- [Finalization and Archival — PR Merge, Cleanup, and Final Status](./42-finalization-pr-merge-and-final-status.md) — Defines the PR-mode merge and prompted worktree-cleanup steps, and
- [Task Management Rules](./43-task-management-rules-and-termination.md) — Restates the task-creation, status-update, checkbox-ticking, and never-skip rules, plus
- [Example Usage](./44-example-usage-and-iteration-example.md) — Walks through four invocation examples (default, extended iterations, from
- [Safety Features](./45-safety-features-and-plan-specific-validation.md) — Describes the infinite-loop prevention, progressive-update, error-recovery, and plan-preservation safety
- [Related Workflows](./46-related-workflows-and-success-metrics.md) — Lists workflows this one composes with and the recommended
- [Notes](./47-notes.md) — Summarizes the orchestrator model, automation posture, idempotency, and other
- [Test-Driven Development](./48-tdd-principles-conventions-agents.md) — States the TDD requirement for delivery items that ship
