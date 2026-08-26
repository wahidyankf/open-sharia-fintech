---
title: "Relationship to plan-execution.md and Concurrency Model"
description: What this workflow inherits vs. adds relative to plan-execution.md, and the parallelism, N+1 model, and status-cadence rules bounding a run.
when_to_use: Use when unsure whether a rule belongs here or in plan-execution.md, or when setting/reasoning about concurrency.
---

# Relationship to plan-execution.md and Concurrency Model

Everything about how a _single_ plan executes — the [Task-Checklist Synchronization
model](../plan-execution/task-checklist-synchronization.md), the [Atomic Sync
Ritual](../plan-execution/atomic-sync-ritual.md), [Resume Reconciliation (disk is
truth)](../plan-execution/resume-reconciliation.md), the [Iron
Rules](../plan-execution/iron-rules-1-5.md), Steps 0–8, per-phase quality gates,
post-push CI verification, manual behavioral assertions, and archival — is **inherited verbatim**
from `plan-execution.md` and applied per plan. This document specifies only the multi-plan additions:
the DAG (Phase A), the union granular Task list (Phase B), the ready-queue scheduler (Phase C), and
failure isolation (Phase D). Where the two ever appear to conflict, `plan-execution.md`'s per-plan
rules win for that plan's internal work; this document governs only cross-plan scheduling.

## Concurrency Model

- **`parallelism` (default 3)** is the maximum number of delivery-step **nodes** in flight at once
  across all plans — the "N parallel Tasks". The caller overrides it (e.g., "…with parallelism 2" or
  "…serially" = 1).
- The **effective** concurrency is `min(parallelism, max-concurrency, harness agent cap)`. Per the
  [Agent Workflow Orchestration Convention](../../../development/agents/agent-workflow-orchestration.md),
  concurrency follows the **N+1 model** — `1 main thread + N background agents = N+1 total`, default
  **N=3** (4 total). The orchestrator MUST NOT self-promote above the declared N or the harness cap.
  N is adjustable per-plan and along the way: raise it only when independent work, machine capacity,
  and budget headroom all allow, and lower it under budget, runner, or disk pressure.
- **Background-slot preference**: fill background slots up to N and keep the main thread vacant and
  responsive — orchestrator, not worker. Never split dependent work merely to fill a slot.
- **Ordering is DAG-first**: independent nodes fan out up to N, dependent nodes serialize, and
  cleanup is the terminal node. The DAG's independent-node width is the fan-out — N only caps it.
  Sequence is not dependency.
- Parallelism is a **ceiling, not a target** — the scheduler runs fewer nodes when the ready set is
  smaller or when resource conflicts force serialization.
- **Status cadence**: while nodes are in flight, update the user every **5 minutes** for generic work
  and every **3 minutes** for GitHub-CI-related work (mixed batches take the tighter 3-minute
  cadence), anchored to meaningful state changes (a node completing, a gate flipping, a plan
  quarantining) rather than to a timer alone. This is a reporting cadence and leaves the 2-minute
  CI-polling floor untouched. See
  [Task List Discipline §Standard 6](../../../development/practice/task-list-discipline.md).
- **Delivery is 1-PR↔1-branch↔1-delivery-unit**: each independent node gets its own branch and PR,
  opened and merged as that unit's **delivery boundary** completes — not at every phase, and not
  batched at the end. For worktree modes, one worktree per repository per plan is reused across
  every node landing there, per
  [Plans Organization Convention §Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).
