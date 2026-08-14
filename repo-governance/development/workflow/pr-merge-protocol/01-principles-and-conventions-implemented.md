---
title: "Principles and Conventions Implemented"
description: The principles and companion conventions the PR merge protocol implements and respects.
category: explanation
subcategory: development
tags:
  - pull-request
  - merge
  - quality-gates
  - workflow
  - merge-preconditions
created: 2026-04-04
when_to_use: Use when tracing why the PR merge protocol exists back to the principles and conventions it respects.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Merging a PR is an irreversible integration action that changes the state of the trunk for every contributor. It demands a deliberate readiness judgment -- which this protocol makes explicit and checkable as preconditions, rather than leaving it to an agent's discretion in the moment.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: When quality gates fail, the correct response is to investigate and fix the root cause, not to bypass the gate and merge anyway. This convention ensures that failing gates are treated as problems to solve, not obstacles to circumvent.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Merge authority must rest on explicit, checkable state. "The review cycles felt thorough enough" -- an agent's implicit readiness judgment substituting for the stated preconditions -- is the silent assumption this convention forbids. The merge actor is likewise explicit: `[AI]` by default, `[HUMAN]` only where a plan says so.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Quality gates (typecheck, lint, test:quick, specs:coverage, CI workflows) run automatically, and the merge decision is derived from their outcome rather than re-litigated by hand each time. Encoding readiness as preconditions is what makes automating the merge safe.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Code Quality Convention](../../quality/code.md)**: The quality gates enforced by this protocol (typecheck, lint, test:quick, specs:coverage) are the same gates enforced by the pre-push hook. This convention extends the same standard to the PR merge boundary.

- **[Trunk Based Development Convention](../trunk-based-development.md)**: `worktree-to-pr` -- a short-lived plan branch pushed to a PR -- is the repo-wide default TBD flavor. PRs also exist for `main-to-pr`, code review, and external contributions. This protocol governs the merge step for all of them.

- **[Git Push Safety Convention](../git-push-safety.md)**: Both conventions treat irreversible git operations as gated rather than routine. They differ in the gate: `git push --force` and friends require explicit, per-instance user approval because no automated check can establish their safety, whereas a PR merge's safety **is** mechanically checkable -- so this convention gates on preconditions instead of a prompt.
