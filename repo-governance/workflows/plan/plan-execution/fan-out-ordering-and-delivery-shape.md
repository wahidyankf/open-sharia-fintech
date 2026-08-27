---
title: "Fan-Out, Ordering, and Delivery Shape"
description: Defines the N+1 fan-out model, DAG-first ordering, and the one-PR-per-delivery-unit / one-worktree-per-repo delivery shape.
when_to_use: Use when planning how many agents to run concurrently, or how delivery units map to branches, PRs, and worktrees.
---

# Fan-Out, Ordering, and Delivery Shape

**Fan-out follows the N+1 model**: `1 main thread + N background agents = N+1 total`, default
**N=3**. The orchestrator keeps the main thread vacant and responsive — filling background slots
first — and never silently self-promotes beyond the plan's declared N. See the
[Agent Workflow Orchestration Convention](../../../development/agents/agent-workflow-orchestration.md).

**Ordering is DAG-first**: the plan's `## Parallelization Model` declares which nodes are
independent. Independent nodes fan out up to N; dependent nodes serialize; **sequence is not
dependency**. The DAG's independent-node width is the fan-out — N only caps it.

**Delivery is 1-PR↔1-branch↔1-delivery-unit, capped at 1-worktree-per-repository**: each independent
DAG node **that produces changes** gets its own branch and PR — opened and merged when that unit's
**delivery boundary** is reached, rather than at every phase or batched at plan end. The **worktree**
is a coarser, per-repository unit: a plan provisions at most one worktree per repo and reuses it
(branch-switched) across every delivery unit that repo produces
([§Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)).
A **delivery unit** is the contiguous run of phases ending at a boundary; the plan's `### Delivery
Boundaries` table names which phase in each unit opens the PR, and intermediate phases pass their own
gate while opening nothing
([§PRs Open at Delivery Boundaries](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule)).
Cleanup is the terminal DAG node, so a repo's shared worktree is removed only once **every** delivery
unit's PR that used it has landed and no in-flight node still needs it — not when the first one does.
**Phase 0 is not a delivery node** — it is setup and baseline only, so it opens no PR under any
delivery mode and the earliest PR belongs to Phase 1
([§Phase 0 Opens No PR](../../../conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule)).

**Git operations stay non-destructive and self-scoped**: assume other agents and engineers share
this machine's disk, git object store, and worktrees. Never run an operation that discards a
concurrent actor's uncommitted work, and never remove a worktree or branch you did not create. See
[No Destructive Git Operations](../../../development/workflow/no-destructive-git-operations.md) and
[Worktree and Artifact Cleanup](../../../development/workflow/worktree-and-artifact-cleanup.md).

**Status heartbeat**: when the main thread has no useful work left and only polls non-CI
background work, update the user every **5 minutes**, even when no state changed. Ordinary work
uses milestone updates; CI keeps its separate 2-minute status-read cadence. See
[Task List Discipline §Standard 6](../../../development/practice/task-list-discipline.md).
