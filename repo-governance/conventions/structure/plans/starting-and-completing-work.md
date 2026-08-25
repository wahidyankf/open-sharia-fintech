---
title: "Starting and Completing Work"
description: Details the steps to promote a plan from backlog/ to in-progress/ and provision its worktree, and the steps to complete and archive it to done/.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when moving a plan from backlog/ to in-progress/, or from in-progress/ to done/.
---

# Starting and Completing Work

## Starting Work

Never execute a plan directly from `plans/backlog/`. Its pure promotion must reach `origin/main`
before implementation begins.

1. **Resolve the delivery mode first.** Apply the
   [three-tier precedence](./delivery-mode-merge-authority-and-precedence.md#delivery-mode--merge-authority-and-resolution-precedence),
   then check the [per-repository restrictions](./per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule).
2. **Choose the permitted landing route.** For `worktree-to-pr`, `main-to-pr`, or whenever the
   repository forbids direct push, sync `origin/main`, create or enter the plan's dedicated
   worktree branch, and use the PR route below. Use direct push only when the resolved mode is
   `worktree-to-origin-main` or `main-to-origin-main` **and** the repository permits that mode;
   perform the move from the mode's declared work location.
3. **Make a pure move.** Move `plans/backlog/<identifier>/` to
   `plans/in-progress/<identifier>/` without a date prefix, and update only the required
   `backlog/README.md` and `in-progress/README.md` indexes. Do not include implementation or other
   ride-along changes.
4. **Land the promotion.** On the PR route, commit and push the worktree branch, open the
   pure-move PR, complete the [PR Review Quality Gate](../../../workflows/pr/pr-review-quality-gate.md),
   and merge it into `origin/main`. On a permitted direct-push route, commit and push the pure move
   to `origin main`.
5. **Verify and continue.** Confirm the promotion exists on `origin/main`, refresh or provision the
   implementation work branch from that commit, resolve the plan at its new `plans/in-progress/`
   path, initialize the toolchain, and only then execute its delivery checklist. The promotion PR
   and implementation are separate delivery units.

For the worked route, see [Execute Plan from Backlog](../../../workflows/plan/plan-execution/example-usage-and-iteration-example.md#execute-plan-from-backlog).

## Completing Work

1. **Verify completion**: Ensure all deliverables and acceptance criteria met — for UI-bearing plans, this includes the production visual sign-off (rule 10 of the [User-Facing Delivery Hardening Convention](../../../development/quality/user-facing-delivery-hardening.md))
2. **Add completion date prefix**: Rename folder from `in-progress/[identifier]/` to `done/YYYY-MM-DD__[identifier]/` using today's date (the completion date, not the original creation date)
3. **Move folder**: Move renamed folder to `done/`
4. **Update index**: Update both `in-progress/README.md` and `done/README.md`
5. **Git commit**: Commit the move with completion message
6. **Archive**: Plan is now archived for historical reference

**Checkbox lockstep (rule 13)**: tick each delivery checkbox only after the corresponding code, review, or evidence actually exists — not speculatively. See [User-Facing Delivery Hardening Convention](../../../development/quality/user-facing-delivery-hardening.md) rule 13 for the full checkbox-lockstep requirement.

**Reopen path (rule 14)**: if a production defect surfaces after archival, reopen the plan by moving it back from `done/` to `in-progress/`, stripping the completion-date prefix, and adding a dated note in `README.md` explaining the defect. See [User-Facing Delivery Hardening Convention](../../../development/quality/user-facing-delivery-hardening.md) rule 14 for the full reopen procedure.
