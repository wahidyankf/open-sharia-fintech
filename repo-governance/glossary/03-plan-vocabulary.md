---
title: "Plan Vocabulary"
description: Definitions for plan, phase, delivery unit, delivery boundary, delivery mode, and worktree, and how they nest.
when_to_use: Use when scoping a plan, deciding where a PR opens, or arguing about whether two pieces of work are one delivery unit or two.
category: explanation
subcategory: governance
tags:
  - governance
  - glossary
  - plans
  - workflow
created: 2026-08-16
---

# Plan Vocabulary

These six terms nest, and conflating any two of them produces either a PR per phase or a single PR
for a whole quarter.

| Term                  | What it is                                                          |
| --------------------- | ------------------------------------------------------------------- |
| **Plan**              | One piece of intended work, held in `plans/` as a document set      |
| **Phase**             | One step of a plan's delivery checklist                             |
| **Delivery unit**     | A contiguous run of phases that is independently shippable          |
| **Delivery boundary** | The point where a delivery unit ends and its PR opens               |
| **Delivery mode**     | Where work happens and how it reaches the integration target        |
| **Worktree**          | A work location — an isolated checkout, not an integration decision |

## How They Nest

A plan holds many phases. A delivery unit groups contiguous phases up to the point where the work
stands on its own; that point is the delivery boundary. **One delivery unit maps to exactly one
branch and one PR** — not one per phase, and not one per plan.

Phase 0 is always environment setup and baseline. It opens no PR, pushes no branch, and runs no
review cycle, because there is nothing yet to review.

## Mode Versus Location

Delivery mode and worktree answer different questions. A worktree is _where the work happens_;
delivery mode additionally fixes _the integration target_ and _merge authority_. The repo-wide
default is `worktree-to-pr` — isolated worktree, draft PR against the trunk, merged by the agent
once preconditions hold.

A plan provisions at most one worktree per repository, reused across delivery units by switching
branches. The branch and the PR stay one-per-delivery-unit.

## Related Documents

- [Glossary](../glossary.md) — the other term clusters.
- [Delivery Mode](../conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode) —
  the four modes and how the active one is resolved.
- [Planning Granularity](../workflows/plan/plan-planning/03-planning-granularity-and-one-branch-rule.md) —
  the one-branch rule and the worktree cap.
- [Plans Organization Convention](../conventions/structure/plans.md) — folder lifecycle and
  document set.
