---
title: "Termination Criteria and Grilling Contract"
description: Defines the composite's pass/partial/fail outcomes and summarizes its three mandatory hard-gated grill sessions.
when_to_use: Use when determining the composite's final status, or confirming which grill sessions are required before proceeding.
---

# Termination Criteria

- **Success** (`pass`): every plan gated to double-zero and delivered its archival change; replacement
  exact-head proof is green, the delivered-head terminal audit passes in every repo, sibling links
  are repaired, and each exact identity-recorded worktree is removed only after `pass` plus all
  cleanup safety proofs.
- **Partial** (`partial`): planning phase succeeded but at least one repo's execution ended
  `partial`/`fail`, or a delivery target was not reached; completed repos remain archived,
  failing repos retain their current plan/worktree state with evidence and escalation. A terminal
  audit or cleanup-precondition failure is never a user-choice `pass` path and reopens execution.
- **Failure** (`fail`): the planning phase failed, the phase gate found a repo not
  execution-ready, or the invoker abandoned any of the three grills

**Per-repo Delivery Mode note**: "archived, pushed" above means a different concrete outcome per
repo depending on that repo's resolved
[`## Delivery Mode`](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode):
public OSE repositories use `worktree-to-pr`, with exact-head CI/leak proof and merge under default
`[AI]` authority before terminal audit. Direct-push modes, `main-to-pr`, and
`worktree-to-origin-main` are unavailable in this public composite. See the
[PR Merge Protocol](../../../development/workflow/pr-merge-protocol.md).

## Grilling Contract

This composite is intentionally exhaustive: **three grill sessions, all hard gates**.

1. **Matrix grill** (planning Step 3): every cross-repo deviation decided and justified — no
   authoring with undecided cells.
2. **Post-research grill** (planning Step 5): research findings validated against the decisions —
   no authoring on stale assumptions.
3. **Pre-execution grill** (composite Step 3): execution order, failure policy, open design
   decisions, and `[HUMAN]` availability — no execution on unconfirmed operational decisions.
   Cleanup is not grilled: after delivered-head terminal audit and `pass`, eligible exact
   identity-recorded worktrees are removed immediately; failed preconditions retain evidence,
   reopen execution, and escalate.

Every question follows the
[Grilling-With-Options Convention](../../../development/workflow/grilling-with-options.md). "We
didn't discuss it" is a workflow failure at every gate.
