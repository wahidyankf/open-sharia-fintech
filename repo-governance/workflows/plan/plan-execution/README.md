---
title: "Plan Execution Workflow"
description: "Executes a project plan end-to-end — orchestration, delegation, quality gates, iteration, archival — split into per-topic children."
when_to_use: "Read this index to find the right Plan Execution Workflow child document."
---

# Plan Execution Workflow

- [Execution Mode](./execution-mode.md) — That the calling context, not a dedicated plan-executor agent, directly orchestrates plan execution.
- [How to Execute](./how-to-execute.md) — Tracing the exact ordered actions plan execution performs, from backlog promotion through worktree cleanup.
- [Orchestration Model](./orchestration-model.md) — That the calling context orchestrates plan execution, routing substantive work to specialized agents.
- [Agent Selection](./agent-selection.md) — Deciding which agent should execute a given delivery checklist item.
- [Fan-Out, Ordering, and Delivery Shape](./fan-out-ordering-and-delivery-shape.md) — The N+1 fan-out model, DAG-first ordering, and the one-PR-per-delivery-unit / one-worktree-per-repo delivery shape.
- [Surface-Conditional Tester Gates](./surface-conditional-tester-gates.md) — Determining which tester gates a plan's shipped surface requires before archival.
- [Vercel MCP Availability (Surface-Conditional)](./vercel-mcp-availability.md) — How execution reconfirms Vercel MCP availability at Phase 0 for plans touching a Vercel-deployed surface.
- [Task-Checklist Synchronization](./task-checklist-synchronization.md) — Reconciling the harness Task list against delivery.md, or confirming every checkbox maps to exactly one task.
- [Harness Task List as Primary Observability Surface](./harness-task-list-primary-observability-surface.md) — Auditing task creation, titling, and timing against the observability invariants.
- [Atomic Sync Ritual](./atomic-sync-ritual.md) — The mandatory three-step tick-notes-TaskUpdate sequence that must land together for every completed checklist item.
- [Resume Reconciliation (Disk Is Truth)](./resume-reconciliation.md) — Resuming plan execution in a new conversation, or when the Task list and delivery.md disagree.
- [Rules 1-5](./iron-rules-1-5.md) — Checking execution against the first five hard, non-negotiable rules governing every execution step.
- [Rules 6-11](./iron-rules-6-11.md) — Checking execution against rules 6-11 of the hard, non-negotiable rules governing every execution step.
- [Preconditions and Work Branch](./enter-worktree-preconditions-and-work-branch.md) — The backlog-promotion precondition and the three-tier precedence for selecting the plan's work branch.
- [Delivery-Mode Resolution](./enter-worktree-delivery-mode-resolution.md) — Resolving which delivery mode (worktree-to-pr, main-to-origin-main, etc.) a plan executes under.
- [Locate and Provision](./enter-worktree-locate-and-provision.md) — How the orchestrator finds the declared ## Worktree section and provisions it.
- [Freshness Gate](./enter-worktree-freshness-gate.md) — Syncing a work branch or worktree with origin/main before starting implementation.
- [Secrets, Output, and Rationale](./enter-worktree-secrets-output-and-rationale.md) — A checklist item runs a state-changing infrastructure operation.
- [Load Delivery Checklist and Materialize Task List](./load-delivery-checklist-and-task-list.md) — Starting or resuming plan execution and building the initial Task list from delivery.md.
- [Environment Setup](./environment-setup.md) — Running or auditing a plan's Phase 0 (environment setup and baseline) before implementation begins.
- [Execution Loop](./initial-execution-loop.md) — Walking through how each delivery checklist item is picked up, repo-grounded, and routed for execution.
- [Verify, Capture, and Atomic Sync](./initial-execution-items-5-8.md) — Execution-loop steps 5-8, through to the atomic sync ritual.
- [Progress, Output, and Stopping Rules](./initial-execution-progress-and-stopping-rules.md) — Execution-loop step 9, progress-streaming cadence, success/failure criteria, and the sanctioned stopping rules.
- [Gates](./per-phase-quality-gate-gates.md) — Verifying a phase's own gate, or running local and integration/e2e quality gates after a phase completes.
- [Push Targets](./per-phase-quality-gate-push-targets.md) — The push target per delivery mode and the direct-push vs. \*-to-pr branch/PR mechanics.
- [Phase 0 Exemption and Delivery-Boundary Merging](./per-phase-quality-gate-phase0-and-boundary-merging.md) — Phase 0's PR exemption and the delivery-boundary merge-not-batch rule.
- [Worktree Cleanup and Boundary Assertion](./per-phase-quality-gate-cleanup-and-invariant.md) — Deciding whether a worktree is safe to remove, or whether a boundary phase opened its PR.
- [Overview and Monitoring Tool](./post-push-ci-verification-overview.md) — When Post-Push CI Verification applies and the required ScheduleWakeup-based monitoring tool and cadence.
- [Direct-Push Modes](./post-push-ci-verification-direct-push.md) — Monitoring CI after a push under worktree-to-origin-main or main-to-origin-main.
- [PR-Branch Modes](./post-push-ci-verification-pr-branch.md) — Monitoring CI after a push under worktree-to-pr or main-to-pr.
- [Web UI and API Verification](./manual-behavioral-assertions-web-and-api.md) — A phase touches web UI or API code and needs manual verification.
- [Full-Stack Verification and Evidence](./manual-behavioral-assertions-full-stack-and-evidence.md) — Full-stack verification covering both UI and API, and the evidence-capture requirements for delivery.md.
- [Validation](./validation-and-check-for-findings.md) — Running independent validation after execution, or deciding whether zero findings were achieved.
- [Continue Execution](./continue-execution.md) — A validation report returns findings that must be fixed before re-validation.
- [Re-validate](./revalidate-and-iteration-control.md) — The re-validation step and the iteration-control logic that loops execution or proceeds to finalization.
- [Pre-Archival Gates](./finalization-pre-archival-gates.md) — A UI-bearing or web-UI feature-change plan approaches archival and must run its pre-archival visual and retest gates.
- [Rule-16 API Retest Gate](./finalization-rule16-api-retest.md) — An API feature-change plan approaches archival and must run its near-end exploratory retest gate.
- [Knowledge Capture Gate](./finalization-knowledge-capture.md) — Confirming every learnings.md entry reached a terminal state before archival.
- [PR-Review Maker→Fixer Cycle Gate](./finalization-pr-review-gate.md) — A \*-to-pr plan approaches archival and must complete its PR review cycle before merge.
- [Status Logic, Infra-Execution Gate, and Direct-Push Archival](./finalization-status-logic-and-infra-gate.md) — The pass/partial/fail branching and the Infra-Execution Gate precondition.
- [Direct-Push Worktree Cleanup and PR-Mode Archival](./finalization-worktree-cleanup-and-pr-archival.md) — Worktree cleanup for direct-push modes, archival-in-PR for \*-to-pr modes.
- [PR Merge, Cleanup, and Final Status](./finalization-pr-merge-and-final-status.md) — The PR-mode merge, safe immediate worktree cleanup, and final pass/partial/fail status determination.
- [Task Management Rules](./task-management-rules-and-termination.md) — A compact reference for task-list discipline rules and the pass/partial/fail termination criteria.
- [Example Usage](./example-usage-and-iteration-example.md) — Learning how to invoke plan execution with different arguments, or tracing a typical execute-validate cycle.
- [Safety Features](./safety-features-and-plan-specific-validation.md) — Explaining what safety guarantees plan execution provides, or what the checker validates.
- [Related Workflows](./related-workflows-and-success-metrics.md) — Composing plan execution with other workflows, or when tracking success metrics across plan executions.
- [Notes](./notes.md) — A quick-reference summary of plan execution's operating characteristics and how it differs from plan-quality-gate.
- [Test-Driven Development](./tdd-principles-conventions-agents.md) — Confirming TDD is required for a code-shipping checklist item, or checking which principles/conventions this workflow follows.
