---
title: "Enter the Designated Worktree — Delivery-Mode Resolution"
description: Defines the three-tier precedence for resolving a plan's delivery mode and the per-repository availability check.
when_to_use: Use when resolving which delivery mode (worktree-to-pr, main-to-origin-main, etc.) a plan executes under.
---

# Enter the Designated Worktree — Delivery-Mode Resolution

**Continues** [Enter the Designated Worktree — Preconditions and Work Branch](./enter-worktree-preconditions-and-work-branch.md).

**Delivery-mode resolution (same three-tier precedence)**: alongside the work-branch precedence above, the executor also resolves the plan's active **delivery mode**, using the identical three-tier pattern: (1) a mode given as an **invocation argument** wins; (2) if none is given, the plan's own `## Delivery Mode` declaration wins; (3) absent either, the default is **`worktree-to-pr`**. See [Plans Organization Convention §Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode) for the full four-mode table and the precedence algorithm. Immediately after resolving, check repository availability: in `ose-public` a resolved `worktree-to-origin-main` or `main-to-origin-main` is an authoring-time error — those modes have no executable path there (branch-protected `main`) — terminate with status `fail` rather than attempt the push; in `ose-private` the same two modes are valid only for an infrastructure-as-code plan. See [Plans Organization Convention §Per-Repository Delivery Mode Restrictions](../../../conventions/structure/plans/per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule). The resolved mode determines which work-location branch below applies:

- `worktree-to-pr` and `worktree-to-origin-main` — work happens in a dedicated **worktree**; follow the worktree provisioning and entry steps below.
- `main-to-origin-main` and `main-to-pr` — work happens directly in the **primary checkout**; skip worktree provisioning entirely per the "Work-branch provisioning vs. entry" note immediately below, and apply the freshness gate (step 5) directly to the primary checkout.

The resolved delivery mode also determines the push target at each phase gate (Steps 2b/2c) and the finalization/archival path (Step 8) — each of those steps documents its mode-specific behavior. Under a `*-to-pr` mode the push target is the delivery unit's branch, but the PR itself opens only at the unit's **delivery boundary** ([§PRs Open at Delivery Boundaries](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule)).

**Work-branch provisioning vs. entry**: when the work branch is a dedicated worktree (the default-when-unspecified case), follow the provisioning and entry steps below. When the user specifies the `main` checkout or another existing branch, skip provisioning (orchestrator-action steps 1–4): confirm you are on that branch, then apply the freshness gate (step 5) directly to it.
