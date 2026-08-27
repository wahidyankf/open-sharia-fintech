---
title: "The `worktree-to-pr` Terminal Step"
description: The sequence after all commits are pushed under worktree-to-pr - current-head CI, surface gates, archival, and readiness.
category: explanation
subcategory: development
tags:
  - pull-request
  - merge
  - quality-gates
  - workflow
  - merge-preconditions
created: 2026-04-04
when_to_use: Use when a worktree-to-pr plan branch has all its commits pushed and the AI needs to know what "done" requires before the merge.
---

# The `worktree-to-pr` Terminal Step

Under the repo-wide `worktree-to-pr` default (see the
[Plans Organization Convention — Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode) and
the [Trunk Based Development Convention](../trunk-based-development/default-delivery-mode-worktree-to-pr.md#default-delivery-mode-worktree-to-pr)),
the AI's work on a plan branch does not end at "all commits pushed." The terminal step, run by `[AI]`,
is:

1. Confirm the **done-definition** is met:
   - The `Quality gate` check is green for the exact current PR head and base.
   - One authenticated `ose-pr-leak-review:v1` record passes for that exact head.
   - Every review conversation is resolved or explicitly dismissed by the user.
   - Every applicable finite surface gate passed, with an explicit exemption when no reachable
     surface exists.
   - Archival-in-PR is committed (ose-public only -- the plan folder's archival move lands in the same
     PR, since the plan folder lives solely in this repo).
2. If the user explicitly requested [`pr-review`](../../../workflows/pr/pr-review.md) or
   [`pr-review-cycle`](../../../workflows/pr/pr-review-cycle.md), complete that bounded request and
   resolve any conversations it created. Its absence is valid.
3. Flip the PR from draft to ready for review (`gh pr ready`).

**This done-definition is the AI's done-boundary.** Meeting it means the AI's work on the plan is
complete -- it does **not** by itself mean the plan is merged. The merge is a separate, subsequent
action gated on the five preconditions in [The Rule](./the-rule.md#the-rule) above and performed by `[AI]`.
"Done" is not "merged" -- the merge sits outside the done-boundary entirely.
