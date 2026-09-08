---
description: Discovers, reconciles, and takes over a plan's in-flight state across repos before handing off to plan-execution.md.
when_to_use: Use before plan-execution.md when the plan might already be worked somewhere; skip for a brand-new plan.
---

# Plan Takeover Execution Workflow

**Purpose**: Find whether a plan is worked anywhere, reconcile it, adopt in-flight work, clean up
leftovers, then hand off to [`plan-execution.md`](../plan/plan-execution.md).

## Agent References

The takeover keeps any existing specialist ownership; final implementation verification uses
[plan-execution-checker](../../../.claude/agents/plan/plan-execution-checker.md).

## Goal and Termination

**Goal**: Given a path to a plan, discover its true execution state across every candidate repository — local worktrees, local and remote branches, and GitHub PRs — reconcile that state into one authoritative picture, take over any in-flight implementation found rather than restarting it, remove confirmed-stale leftover worktrees/branches/build artifacts, and hand off to plan-execution.md against the reconciled state

**Termination**: Every candidate repo's plan state is classified, all confirmed-stale leftovers are removed (or explicitly held with a reason), and each live or fresh target has been handed to plan-execution.md, which reaches its own termination for that repo

## Inputs

- **`plan-path`** (string, required) — Path to the plan folder (in plans/backlog/, plans/in-progress/, or plans/done/) in the current repo, or a bare plan-identifier slug when no local folder exists at all (e.g., the plan was only ever committed on a branch or in a sibling repo).
- **`repos`** (list, optional) — Explicit override of the candidate repo set Phase A1 probes. Default (when omitted): the current repo, plus `ose-private` whenever it exists as a sibling checkout reachable from the same parent directory as this repo — this default is a FLOOR, never narrowed below the current repo, and widened automatically when the plan's own docs name additional repos in scope.
- **`max-concurrency`** (number, optional, default `3`) — Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Independent repos' discovery probes may fan out up to this bound. Never self-promoted beyond the declared value.

## Outputs

- **`takeover-report`** (file, pattern `local-tmp/plan-takeover-execution/plan-takeover-execution__*__discovery.md`) — Per-repo raw findings, bucket classification, adopted targets, removed leftovers, and any anomalies escalated (with their resolution, if resolved during the run)
- **`reconciled-targets`** (map) — Per-repo bucket assignment (nothing-found / already-delivered / live-in-flight / anomaly) and, for live-in-flight repos, the adopted worktree path, branch, and PR number if one exists
- **`plan-execution-outputs`** (map) — Every output plan-execution.md itself defines, produced once per repo this workflow hands off to

## Contents

- [When to Use, Relationship](./plan-takeover-execution/when-to-use-and-relationship.md) — scope.
- [Why This Exists](./plan-takeover-execution/why-this-workflow-exists.md) — motivation.
- [Execution Mode, Concurrency](./plan-takeover-execution/execution-mode-and-concurrency-model.md) — fan-out.
- [Task List Discipline](./plan-takeover-execution/task-list-discipline.md) — Task mapping.
- [Phase A — Identifier, Repos](./plan-takeover-execution/phase-a-discovery-plan-identifier-and-repo-set.md) — A0-A1.
- [Phase A — Per-Repo Probes](./plan-takeover-execution/phase-a-discovery-per-repo-probes-and-persistence.md) — A2-A3.
- [Phase B — Reconcile](./plan-takeover-execution/phase-b-reconcile-findings.md) — buckets.
- [Phase C — Adopt, Ledger](./plan-takeover-execution/phase-c-adopt-freshness-and-ledger.md) — steps 1-3.
- [Phase C — PR, delivery.md](./plan-takeover-execution/phase-c-pr-record-and-reconcile-delivery.md) — steps 4-5.
- [Phase D — Clean Up](./plan-takeover-execution/phase-d-clean-up-confirmed-stale-leftovers.md) — removal.
- [Phase E — Hand Off](./plan-takeover-execution/phase-e-hand-off-to-plan-execution.md) — invocation.
- [Related Documentation](./plan-takeover-execution/related-documentation.md) — cross-references.
