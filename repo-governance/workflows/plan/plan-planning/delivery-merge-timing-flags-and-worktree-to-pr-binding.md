---
title: "Delivery-Unit Merge Timing, Feature Flags, and worktree-to-pr Binding"
description: States when a delivery unit's PR merges, the feature-flag default and removal rule, and how the worktree-to-pr default binds at plan-authoring vs. plan-execution time.
when_to_use: Use when deciding when a PR should merge, whether a phase needs a feature flag, or how the worktree-to-pr default applies while authoring vs. executing a plan.
---

# Delivery-Unit Merge Timing, Feature Flags, and worktree-to-pr Binding

## Merge at Delivery Boundaries — Not Every Phase, and Not One Batch

Each delivery unit's PR is **opened and merged** as that unit's **delivery boundary** is reached. It
is neither opened early at every intermediate phase, nor held open for a **batch merge** at plan end.

Both failure modes cost something different. Opening a PR per phase spends PR CI and integration overhead on
scaffolding the next phase rewrites, and the review cannot judge intent that only lands two phases
later. Holding PRs for a batch merge serialises work the DAG already declared independent, and grows
the divergence each PR must reconcile against `main`.

Grouping **dependent** phases into one delivery unit is not batching. The prohibition targets
holding **independent, already-open** PRs — never the decision to review a dependent chain as one
complete thought.

The **merge actor** follows the inverted default in
[Plans Organization Convention §Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode):
`[AI]` merges once the hardened preconditions hold, and `[HUMAN]` applies **only** where a plan's
own step states that gate explicitly.

## Feature Flags: Default, Escape, Removal

Partial work reaches `main` **merged but dark** behind a feature flag rather than waiting on a
long-lived branch. Flagging is the **default**.

- **Escape**: a phase lands **unflagged** only when it ships no **user-reachable** behaviour change
  — pure docs, governance, refactor, or test-only work — and the delivery step names which
  exemption applies. An unflagged phase with no named exemption is a defect.
- **Removal**: every flag introduced carries a named **flag removal step** in the plan's final
  phase. A flag with no removal step is an unbounded commitment, not a rollout mechanism.

## How the `worktree-to-pr` Default Binds at Each Plan Path

The default binds differently depending on what is being done:

- **Creating or updating a plan** binds it as a **design obligation**. The authoring edit itself may
  push direct to `main`, but the plan's phases MUST be authored so they group into **independently
  PR-able delivery units**, with each unit's boundary named in the `### Delivery Boundaries` table.
  A plan that genuinely cannot be decomposed that way records **why** in its chosen technical form — the
  constraint is documented, not silently absorbed.
- **Executing a plan** binds it as the actual delivery route: worktree → PR, per the
  delivery-unit-to-PR mapping above.
