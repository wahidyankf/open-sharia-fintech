---
description: "Defines how orchestration behaviour is gated by the current harness's capabilities."
when_to_use: Use when an orchestration behaviour depends on whether the current harness supports it.
---

# Operating Budgets — Harness Capability Gating

Not every coding-agent harness can run background or parallel subagents. The model above is stated so that it degrades cleanly rather than becoming inapplicable:

> Where the harness supports background or parallel subagents, execute independent DAG nodes concurrently up to the declared cap. Under `*-to-pr`, each unit has its own branch; under permitted direct modes, each unit uses its declared checkpoint. Worktree modes reuse at most one worktree per repo per plan, while main modes use the primary checkout and provision none. Route every compute-bearing node through HIPPO; capacity may defer execution without changing the DAG. Without background subagents, walk the same DAG serially. In every case, preserve dependency and correctness order, non-destructive Git, mode-specific integration safety, and cleanup.

The DAG itself is the portable artifact: the same dependency graph drives a wide fan-out on a background-capable harness and a serial walk on a single-threaded one. Concurrency changes the schedule, never the ordering or the safety rules.

A subagent dispatch whose isolation mode may auto-provision its own worktree still counts against that repo's cap. Target a repo already under an active plan's worktree cap by naming the plan's existing worktree explicitly, never by isolation alone. Where isolation is used regardless, verify with `git worktree list` immediately on return that no extra worktree resulted in a capped repo, and remove it before continuing. See [Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).
