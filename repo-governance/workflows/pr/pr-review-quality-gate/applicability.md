---
title: "PR-Review Quality Gate — Applicability"
description: "Confirms this workflow is mandatory for every open PR, that it never runs against a plan's Phase 0 (which opens no PR), and that it runs once per delivery boundary, not once per phase."
when_to_use: "Use when checking whether this workflow applies to a specific phase or PR, especially around Phase 0 or non-boundary phases."
---

# Applicability

This workflow's classifier is mandatory for every open PR, regardless of delivery mode or plan
origin. Its specialist loop applies only to the **eligible** route; the noneligible route requires a
green `pr-quality-gate.yml` run and no specialist fan-out.

It also does **not** apply to a plan's **Phase 0** under any mode. Phase 0 is Environment Setup and
Baseline — it opens no PR, so there is no PR for the fan-out to review, no threads for
`pr-review-fixer` to resolve, and no CI run for the per-cycle gate. The earliest phase this workflow
can run against is **Phase 1**. Dispatching the specialist fan-out against a Phase 0 is a defect, not
a thoroughness choice: it spends a full N-cycle loop reviewing a diff that does not exist. See
[Plans Organization Convention §Phase 0 Opens No PR](../../../conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).

Nor does it run once per phase. This workflow binds to a **PR**, and a PR opens at a **delivery
boundary** — the phase after which the accumulated work is independently shippable. Phases inside a
delivery unit that are not its boundary open no PR and therefore run no review cycle; the cycle runs
once, at the boundary, against the unit's complete diff. That is deliberate: reviewing scaffolding
the next phase rewrites spends a full loop on work whose intent is not yet visible. See
[Plans Organization Convention §PRs Open at Delivery Boundaries](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).

See
[Plans Organization Convention §Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)
for the full four-mode table, and
[plan-execution.md Step 8](../../plan/plan-execution/finalization-pre-archival-gates.md#8-finalization-and-archival-sequential) for how
this workflow is wired into plan finalization.
