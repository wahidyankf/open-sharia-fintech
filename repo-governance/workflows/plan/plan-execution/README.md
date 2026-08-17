---
title: "Plan Execution Workflow"
description: "Executes a project plan end-to-end — orchestration, delegation, quality gates, iteration, archival — split into per-topic children."
when_to_use: "Read this index to find the right Plan Execution Workflow child document."
---

# Plan Execution Workflow

- [Execution Mode](./01-execution-mode.md) — Orienting to who runs plan execution and why there is no dedicated plan-executor agent.
- [How to Execute](./02-how-to-execute.md) — Tracing the exact ordered actions plan execution performs, from backlog promotion through worktree cleanup.
- [Orchestration Model](./03-orchestration-model.md) — Confirming whether the orchestrator may implement a delivery item directly or must delegate it.
- [Agent Selection](./04-agent-selection.md) — Deciding which agent should execute a given delivery checklist item.
- [Fan-Out, Ordering](./05-fan-out-ordering-and-delivery-shape.md) — Planning how many agents to run concurrently, or how delivery units map to branches, PRs.
- [Surface-Conditional Tester Gates](./06-surface-conditional-tester-gates.md) — Determining which tester gates a plan's shipped surface requires before archival.
- [Vercel MCP Availability (Surface-Conditional)](./07-vercel-mcp-availability.md) — A plan touches a Vercel-deployed surface.
- [Task-Checklist Synchronization](./08-task-checklist-synchronization.md) — Reconciling the harness Task list against delivery.md.
- [Harness Task List as Primary Observability Surface](./09-harness-task-list-primary-observability-surface.md) — Auditing whether task creation, titling, and completion timing satisfy the primary-observability invariants.
- [Atomic Sync Ritual](./10-atomic-sync-ritual.md) — Ticking a delivery.md checkbox, to confirm the tick, notes, and TaskUpdate all land correctly.
- [Resume Reconciliation (Disk Is Truth)](./11-resume-reconciliation.md) — Resuming plan execution in a new conversation, or when the Task list and delivery.md disagree.
- [Rules 1-5](./12-iron-rules-1-5.md) — Checking execution against the first five hard, non-negotiable rules governing every execution step.
- [Rules 6-11](./13-iron-rules-6-11.md) — Checking execution against rules 6-11 of the hard, non-negotiable rules governing every execution step.
- [Preconditions and Work Branch](./14-enter-worktree-preconditions-and-work-branch.md) — Resolving which branch or worktree a plan executes on before any implementation work begins.
- [Delivery-Mode Resolution](./15-enter-worktree-delivery-mode-resolution.md) — Resolving which delivery mode (worktree-to-pr, main-to-origin-main, etc.) a plan executes under.
- [Locate and Provision](./16-enter-worktree-locate-and-provision.md) — A plan's worktree does not yet exist and must be provisioned from the latest origin/main.
- [Freshness Gate](./17-enter-worktree-freshness-gate.md) — Syncing a work branch or worktree with origin/main before starting implementation.
- [Secrets, Output, and Rationale](./18-enter-worktree-secrets-output-and-rationale.md) — A delivery checklist item runs terraform apply, a live Ansible converge.
- [Load Delivery Checklist](./19-load-delivery-checklist-and-task-list.md) — Starting or resuming plan execution and building the initial Task list from delivery.md.
- [Environment Setup](./20-environment-setup.md) — Running or auditing a plan's Phase 0 (environment setup and baseline) before implementation begins.
- [Execution Loop](./21-initial-execution-loop.md) — Walking through how each delivery checklist item is picked up, repo-grounded, and routed for execution.
- [Verify, Capture](./22-initial-execution-items-5-8.md) — Verifying a delegated agent's work, capturing a learning.
- [Progress, Output](./23-initial-execution-progress-and-stopping-rules.md) — Deciding whether the orchestrator may pause between items, or confirming a phase's success criteria.
- [Gates](./24-per-phase-quality-gate-gates.md) — Verifying a phase's own gate, or running local.
- [Push Targets](./25-per-phase-quality-gate-push-targets.md) — Deciding where a phase's changes should push to under the plan's resolved delivery mode.
- [Phase 0 Exemption](./26-per-phase-quality-gate-phase0-and-boundary-merging.md) — Confirming Phase 0 pushes nothing, or deciding whether a delivery unit's PR should open now.
- [Worktree Cleanup](./27-per-phase-quality-gate-cleanup-and-invariant.md) — Deciding whether a repo's worktree is safe to remove.
- [Overview and Monitoring Tool](./28-post-push-ci-verification-overview.md) — Deciding which monitoring tool and poll cadence to use for CI after a push.
- [Direct-Push Modes](./29-post-push-ci-verification-direct-push.md) — Monitoring CI after a push under worktree-to-origin-main or main-to-origin-main.
- [PR-Branch Modes](./30-post-push-ci-verification-pr-branch.md) — Monitoring CI after a push under worktree-to-pr or main-to-pr.
- [Web UI](./31-manual-behavioral-assertions-web-and-api.md) — A phase touches web UI or API code.
- [Full-Stack Verification and Evidence](./32-manual-behavioral-assertions-full-stack-and-evidence.md) — A phase touches both UI and API.
- [Validation](./33-validation-and-check-for-findings.md) — Running independent validation after execution, or deciding whether zero findings were achieved.
- [Continue Execution](./34-continue-execution.md) — A validation report returns findings that must be fixed before re-validation.
- [Re-validate](./35-revalidate-and-iteration-control.md) — Deciding whether to loop back into execution again or proceed to finalization.
- [Pre-Archival Gates](./36-finalization-pre-archival-gates.md) — A UI-bearing or web-UI feature-change plan approaches archival and must run its pre-archival visual.
- [Rule-16 API Retest Gate](./37-finalization-rule16-api-retest.md) — An API feature-change plan approaches archival and must run its near-end exploratory retest gate.
- [Knowledge Capture Gate](./38-finalization-knowledge-capture.md) — Confirming every learnings.md entry reached a terminal state before archival.
- [PR-Review Maker→Fixer Cycle Gate](./39-finalization-pr-review-gate.md) — A \*-to-pr plan approaches archival and must complete its PR review cycle before merge.
- [Status Logic](./40-finalization-status-logic-and-infra-gate.md) — Determining final plan status, or verifying a pending infra-apply step before archiving a plan.
- [Direct-Push Worktree Cleanup](./41-finalization-worktree-cleanup-and-pr-archival.md) — Cleaning up a plan's worktree after a direct push.
- [PR Merge](./42-finalization-pr-merge-and-final-status.md) — Merging a plan's delivering PR, cleaning up its worktree afterward.
- [Task Management Rules](./43-task-management-rules-and-termination.md) — A compact reference for task-list discipline rules and the pass/partial/fail termination criteria.
- [Example Usage](./44-example-usage-and-iteration-example.md) — Learning how to invoke plan execution with different arguments, or tracing a typical execute-validate cycle.
- [Safety Features](./45-safety-features-and-plan-specific-validation.md) — Explaining what safety guarantees plan execution provides, or what the checker validates.
- [Related Workflows](./46-related-workflows-and-success-metrics.md) — Composing plan execution with other workflows, or when tracking success metrics across plan executions.
- [Notes](./47-notes.md) — A quick-reference summary of plan execution's operating characteristics and how it differs from plan-quality-gate.
- [Test-Driven Development](./48-tdd-principles-conventions-agents.md) — Confirming TDD is required for a code-shipping checklist item.
