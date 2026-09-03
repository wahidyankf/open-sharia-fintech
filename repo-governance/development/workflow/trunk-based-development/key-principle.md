---
title: "Key Principle"
description: The three-tier precedence that deterministically resolves the active delivery mode, and the environment-branch carve-out.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use as the final authority on which delivery mode wins when multiple signals are present.
---

# Key Principle

The active delivery mode is resolved deterministically, never inferred from execution context alone:

- **Tier 1 (highest)**: an explicit invocation argument naming a valid mode.
- **Tier 2**: a `## Delivery Mode` field declared in the plan's own docs.
- **Tier 3 (default)**: `worktree-to-pr`.

See the [Plans Organization Convention — Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)
for the full algorithm and the [plan-execution workflow](../../../workflows/plan/plan-execution.md) for
how each mode changes Step 0 (worktree entry), the push target at each phase gate, and Step 8
(finalization and merge hand-off). Under a `*-to-pr` mode the PR itself opens only at a **delivery
boundary**, not at every phase — see
[Plans Organization Convention §PRs Open at Delivery Boundaries](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).

Draw each boundary at a natural cohesive seam, never from a numeric LOC or file count. Merge only
when the exact resulting `main` state is safe to deploy to production immediately, and integrate the
ready unit promptly. See
[Natural Seams and Deployable State](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-natural-seams.md).

Note: this does **not** affect environment branches (`prod-ayokoding-www`, `prod-ose-www`, `stag-organiclever-app-web`, `stag-organiclever-be`). Those follow their own documented deployment workflows. The OrganicLever app staging branches (`stag-organiclever-app-web`, `stag-organiclever-be`) are CI-automated by `organiclever-app-test-local-deploy-stag.yml`. Production promotion for the OrganicLever app is **deferred** to a separate plan — no production-CD workflow exists yet.
