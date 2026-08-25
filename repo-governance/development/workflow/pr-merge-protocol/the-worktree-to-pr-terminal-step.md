---
title: "The `worktree-to-pr` Terminal Step"
description: The sequence an AI runs after all commits are pushed under worktree-to-pr - the review/fix cycle, the done-definition, and flipping the PR to ready.
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

1. Run the **PR-Review Maker→Fixer Cycle**
   (`repo-governance/workflows/pr/pr-review-quality-gate.md`) -- first classify the open PR. Run
   sequential specialist review/fix cycles only for the eligible route; a noneligible route verifies
   the named `pr-quality-gate.yml` workflow instead.
2. Confirm the **done-definition** is met:
   - The eligible route targeted cycles 1–3 and, if needed, completed focused recovery within five
     cycles without starting cycle 6; or the
     noneligible route has recorded classifier evidence and its `pr-quality-gate.yml` run is green.
   - Every inline review comment has a reply (resolved or explicitly addressed).
   - All quality gates are GREEN -- both local (pre-push hook) and CI.
   - Archival-in-PR is committed (ose-public only -- the plan folder's archival move lands in the same
     PR, since the plan folder lives solely in this repo).
3. Flip the PR from draft to ready for review (`gh pr ready`).

**This done-definition is the AI's done-boundary.** Meeting it means the AI's work on the plan is
complete -- it does **not** by itself mean the plan is merged. The merge is a separate, subsequent
action gated on the five preconditions in [The Rule](./the-rule.md#the-rule) above and performed by `[AI]`.
"Done" is not "merged" -- the merge sits outside the done-boundary entirely.
