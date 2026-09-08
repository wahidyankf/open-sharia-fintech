---
description: When plan-maker adds a Delivery Mode field, what plan-checker flags, and how plan-quality-gate and plan-execution resolve the mode.
when_to_use: Use when authoring, checking, or fixing a plan's `## Delivery Mode` field.
---

# Standard 3: Plans Must Declare a Delivery Mode Only to Override the Default

When `plan-maker` authors a plan, it does not need to add a `## Delivery Mode` field for the default
case — `worktree-to-pr` applies automatically. `plan-maker` adds an explicit `## Delivery Mode` field
only when the plan calls for a different mode (`worktree-to-origin-main`, `main-to-origin-main`, or
`main-to-pr`), and must state the justification alongside it.

`plan-checker` must flag any plan whose delivery checklist assumes a direct push to `origin main`
without a corresponding `## Delivery Mode` field declaring one of the direct-push modes. The gate's repair pass
must either add the missing field (if a direct-push mode is genuinely warranted) or correct the
checklist to the `worktree-to-pr` default.

The plan-execution workflow resolves the active mode once, at Step 0, per the three-tier precedence,
and uses that resolution for every subsequent git-mechanical step in the plan.
