---
title: "Termination Criteria and Grilling Contract"
description: Defines the composite's pass/partial/fail outcomes and summarizes its three mandatory hard-gated grill sessions.
when_to_use: Use when determining the composite's final status, or confirming which grill sessions are required before proceeding.
---

# Termination Criteria

- **Success** (`pass`): every plan gated to double-zero, executed to zero findings, archived,
  pushed, CI green in every repo; sibling links repaired; every worktree cleaned up or retained
  by explicit user choice
- **Partial** (`partial`): planning phase succeeded but at least one repo's execution ended
  `partial`/`fail`, or a delivery target was not reached; completed repos remain archived,
  failing repos keep their plan in `plans/in-progress/` and their worktree intact
- **Failure** (`fail`): the planning phase failed, the phase gate found a repo not
  execution-ready, or the invoker abandoned any of the three grills

**Per-repo Delivery Mode note**: "archived, pushed" above means a different concrete outcome per
repo depending on that repo's resolved
[`## Delivery Mode`](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode) — a direct push of the
archival commit to `origin main` for the direct-push modes (`worktree-to-origin-main`,
`main-to-origin-main`), or a green, fully-reviewed PR with the archival move committed inside it,
awaiting the merge outside the AI done-boundary, for the `*-to-pr` modes
(`worktree-to-pr`, `main-to-pr`) — see the
[PR-Review Maker→Fixer Cycle](../../pr/pr-review-quality-gate.md) done-definition. Because each
repo resolves its delivery mode independently, a single composite run may end with some repos
merged directly and others handed off as open PRs.

## Grilling Contract

This composite is intentionally exhaustive: **three grill sessions, all hard gates**.

1. **Matrix grill** (planning Step 3): every cross-repo deviation decided and justified — no
   authoring with undecided cells.
2. **Post-research grill** (planning Step 5): research findings validated against the decisions —
   no authoring on stale assumptions.
3. **Pre-execution grill** (composite Step 3): execution order, failure policy, open design
   decisions, `[HUMAN]` availability, and worktree cleanup preference — no execution on
   unconfirmed operational decisions.

Every question follows the
[Grilling-With-Options Convention](../../../development/workflow/grilling-with-options.md). "We
didn't discuss it" is a workflow failure at every gate.
