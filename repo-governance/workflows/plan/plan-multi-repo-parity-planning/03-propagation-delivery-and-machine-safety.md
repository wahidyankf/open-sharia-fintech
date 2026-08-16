---
title: "Propagation, Delivery Shape, and Shared-Machine Safety"
description: Covers the parallel propagation fan-out, the one-branch-one-PR delivery shape per repo, and the no-destructive-git rule for the shared machine.
when_to_use: Use when deciding whether repos can run in parallel, how a repo's plan lands as PRs, or before running any destructive-looking git operation.
---

# Parallel Propagation Shape

The repos form a propagation fan-out, not a chain: **`ose-public` is the source of truth**, and
`ose-private` is its one downstream target. Where a parity set covers more than two repos, the
downstream repos are **independent DAG nodes** — author and deliver them in parallel under the N+1
model (`1 main thread + N background agents`, default **N=3**), never serialized behind one another.
`ose-private` does not participate in the parity loop for content it does not carry.

The one hard serialization: **`apps/rhino-cli` must stay byte-identical across the parity repos
— `ose-public` and `ose-private`** — so plans touching it propagate one repo at a time
rather than concurrently
([AGENTS.md §Related Repositories](../../../../AGENTS.md#related-repositories)).

## Delivery Shape Per Repo

Each repo's plan is authored to the `worktree-to-pr` default, and each independent node lands as
its **own PR** — a strict **one branch → one PR → one delivery unit** mapping, opened and merged at
that unit's **delivery boundary** rather than at every phase or batched at the end. The **worktree**
is a coarser, per-repository unit: each repo's plan is capped at one worktree, reused across every
delivery unit it lands in that repo — see
[Plans Organization Convention §Worktree Cap](../../../conventions/structure/plans/31-worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).
Partial work reaches `main` merged-but-dark behind a
**feature flag**; a phase lands unflagged only when it ships no user-reachable behaviour change and
the step names that exemption. See
[plan-planning §Planning Granularity](../plan-planning/03-planning-granularity-and-one-branch-rule.md#planning-granularity-and-the-one-branch-one-pr-rule) for the full rule,
including delivery-boundary PR granularity and the named flag-removal step.

## Shared-Machine Safety

The parity repos share one machine's disk and git object store, and any of them may be a bare repo
driven through worktrees — verify each repo's topology, never assume it. Every git action here is
therefore bound by the **no-destructive-git** rule:
never run an operation that discards a concurrent actor's uncommitted work, and never remove a
worktree or branch you did not create. See
[No Destructive Git Operations](../../../development/workflow/no-destructive-git-operations.md) and
[Worktree and Artifact Cleanup](../../../development/workflow/worktree-and-artifact-cleanup.md).
