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

**Promote out of `backlog/` first — on the local `main` checkout, never inside a worktree.** A plan
still sitting in `plans/backlog/` is never executed directly out of that folder; the promotion below
is a mandatory precondition, not an optional courtesy, and it MUST land as a committed, pushed change
on `origin main` before worktree provisioning or any implementation step begins. See
[plan-execution → Execute Plan from Backlog](../../../workflows/plan/plan-execution/example-usage-and-iteration-example.md#execute-plan-from-backlog).

1. **Move folder** (on local `main`, before any worktree exists): Move plan folder from
   `backlog/[identifier]/` to `in-progress/[identifier]/` — a pure move; neither stage carries a
   date prefix.
2. **Update index**: Update both `backlog/README.md` and `in-progress/README.md`
3. **Git commit and push**: Commit the move and push directly to `origin main` — only after this
   push lands does execution proceed
4. **Provision worktree** (optional — the plan-execution Step 0 gate auto-provisions from the latest `origin/main` when missing): Run `claude --worktree <plan-identifier>` from the repo root — this creates `worktrees/<plan-identifier>/` in the repo root (not `.claude/worktrees/`). See [Worktree Path Convention](../worktree-path.md).
5. **Initialize toolchain**: In the root worktree, run `npm install && npm run doctor -- --fix`. See [Worktree Toolchain Initialization](../../../development/workflow/worktree-setup.md).
6. **Begin execution**: Start implementing according to delivery checklist

## Completing Work

1. **Verify completion**: Ensure all deliverables and acceptance criteria met — for UI-bearing plans, this includes the production visual sign-off (rule 10 of the [User-Facing Delivery Hardening Convention](../../../development/quality/user-facing-delivery-hardening.md))
2. **Add completion date prefix**: Rename folder from `in-progress/[identifier]/` to `done/YYYY-MM-DD__[identifier]/` using today's date (the completion date, not the original creation date)
3. **Move folder**: Move renamed folder to `done/`
4. **Update index**: Update both `in-progress/README.md` and `done/README.md`
5. **Git commit**: Commit the move with completion message
6. **Archive**: Plan is now archived for historical reference

**Checkbox lockstep (rule 13)**: tick each delivery checkbox only after the corresponding code, review, or evidence actually exists — not speculatively. See [User-Facing Delivery Hardening Convention](../../../development/quality/user-facing-delivery-hardening.md) rule 13 for the full checkbox-lockstep requirement.

**Reopen path (rule 14)**: if a production defect surfaces after archival, reopen the plan by moving it back from `done/` to `in-progress/`, stripping the completion-date prefix, and adding a dated note in `README.md` explaining the defect. See [User-Facing Delivery Hardening Convention](../../../development/quality/user-facing-delivery-hardening.md) rule 14 for the full reopen procedure.
