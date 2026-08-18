---
title: "Planning Granularity and the One-Branch-One-PR Rule"
description: Introduces the planning-granularity rules and states the hard rule that each independent delivery unit lands as its own branch, PR, and delivery unit.
when_to_use: Use when cutting a plan into phases, or when deciding whether two phases belong in the same PR or two different PRs.
---

# Planning Granularity and the One-Branch-One-PR Rule

How a plan is cut into phases determines how much of it can proceed in parallel and how early each
piece reaches `main`. These rules bind at authoring time, not merely at execution time.

## One Branch, One PR, One Delivery Unit (HARD RULE)

Each independent node of the plan's dependency DAG **that produces changes** lands as **its own
PR**. The mapping is strict and one-to-one: **one branch → one PR → one delivery unit**. Never open
two PRs from one branch, and never drive one PR from two branches.

The **worktree** is not part of this 1:1 mapping. A plan provisions **at most one worktree per
repository**, reused — branch-switched — across every delivery unit it produces in that repo; see
[Plans Organization Convention §Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule).
Never provision a second worktree for a repo the plan already has one open in — switch branches
inside the existing one instead.

A **delivery unit** is the contiguous run of phases ending at a **delivery boundary** — the phase
after which the accumulated work is independently shippable. The unit, not the individual phase, is
what maps to a PR: a plan opens a PR at its natural delivery points, which may be once at the very
end or several times through the plan. Phases inside a unit that are not its boundary still pass
their own `### Phase N Gate`, but open no PR and merge nothing. The boundary test, the required
`### Delivery Boundaries` declaration table, and the anti-batching counterweight are stated in
[Plans Organization Convention §PRs Open at Delivery Boundaries](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).

Genuinely dependent phases stay a single delivery unit. The DAG governs, not the phase numbering:
phases that merely appear in sequence are not thereby dependent, and splitting **independent** work
into separate delivery units is the default. Sequence is not dependency — and neither is it a
licence to fold independent nodes together to reduce PR count.

**Phase 0 is not one of these nodes — the earliest PR is Phase 1 (HARD RULE)**. Phase 0 is
Environment Setup and Baseline: it installs dependencies, converges the toolchain, records the
baseline, and clears preexisting failures. It produces nothing reviewable, so it opens no PR, pushes
no branch, runs no review cycle, and merges nothing — under **every** delivery mode, the default
`worktree-to-pr` included. Author it as a local, gate-terminated phase whose evidence artifacts ride
the Phase 1 PR. A Phase 0 that genuinely produces reviewable changes is mis-scoped: move that work
into Phase 1. See
[Plans Organization Convention §Phase 0 Opens No PR](../../../conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
