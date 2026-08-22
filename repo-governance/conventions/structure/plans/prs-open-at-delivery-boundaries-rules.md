---
title: "PRs Open at Delivery Boundaries, Not Every Phase (HARD RULE)"
description: States the first four of seven rules for when a PR may open.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when deciding if a phase should open a PR.
---

# PRs Open at Delivery Boundaries, Not Every Phase (HARD RULE)

**A PR opens only at a delivery boundary — never at every phase.** A **delivery boundary** is a
phase after which the accumulated work is an independently shippable increment. A **delivery unit**
is the contiguous run of phases ending at a delivery boundary — the unit, not the individual phase,
is what maps to a PR.

The mapping from [Delivery Checklists Express a DAG](./delivery-checklists-express-a-dag.md#delivery-checklists-express-a-dag-hard-rule)
above sharpens: **one branch → one PR → one delivery unit**, not one branch → one PR → one phase. The
**worktree** is a coarser, per-repository unit — capped at one per repo per plan and reused across
every delivery unit landed there, never provisioned fresh per unit — per
[Worktree Cap](./worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule) below.

1. **A PR opens only at a delivery boundary.** Phases inside a delivery unit that are not its
   boundary commit to the unit's branch and must still pass their own `### Phase N Gate`, but they
   open no PR, run no PR-Review Maker→Fixer Cycle, and merge nothing. Pushing the branch to `origin`
   for durability is permitted and opens nothing.
2. **Every plan declares its delivery boundaries explicitly** — see the required declaration format
   in [Delivery Boundaries Declaration and Applicability](./delivery-boundaries-and-applicability.md).
3. **The last change-producing phase is always a delivery boundary.** Otherwise the plan's final
   work never merges.
4. **Phase 0 is never a delivery boundary** — it produces nothing shippable. This is consistent with
   [Phase 0 Opens No PR](./phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule) above, which
   remains the sole authority on Phase 0 itself.

See [PRs Open at Delivery Boundaries — Rules 5-7 and Boundary Test](./prs-open-at-delivery-boundaries-rules-continued.md) for the remaining three rules, the `*-to-pr` scoping note, and the four-part boundary test, and [Bounding PR Size](./prs-open-at-delivery-boundaries-pr-size.md) for how large a PR may be when it opens.
