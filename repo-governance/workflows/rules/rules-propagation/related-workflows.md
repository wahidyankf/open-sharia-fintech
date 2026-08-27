---
title: "Related Workflows"
description: What runs before this workflow, what it composes, and what it hands off to.
when_to_use: Use when deciding whether propagation is the right workflow, or what should follow it.
---

# Related Workflows

## Composed By This Workflow

- **[rules-quality-gate](../rules-quality-gate.md)** — runs at Step 8 as the verifier.
  It owns repository-wide duplication, contradiction, and traceability detection; this workflow
  deliberately does not duplicate that scope.

## Runs Before

- **A grilling or design session.** Propagation places a decided rule. Deciding it is upstream
  work, and a rule arriving here still under debate will halt at Step 0.
- **[harness-compatibility-quality-gate](../../harness/harness-compatibility-quality-gate.md)** —
  where a rule change is expected to affect bindings, running compatibility first establishes a
  clean baseline, so Step 8 findings are attributable to this run.

## Runs After

- **The sibling repository's own propagation.** Step 9 records the obligation; discharging it is a
  separate run in that repository, not a continuation of this one.
- **[rules-quality-gate](../rules-quality-gate.md), scheduled.** The composed run at
  Step 8 is scoped to the run's `mode`; the periodic full sweep remains the repository's standing
  health check.

## Not This Workflow

- **Auditing existing rules.** That is the quality gate, run on its own.
- **Bumping a dependency or changing a toolchain pin.** Those have their own planning workflow, and
  a rule about them propagates here only once the decision is made.
- **Writing a plan.** A rule is not a plan. A rule binds until changed; a plan expires on archival.

## Related Documents

- [Purpose and Scope](./purpose-and-scope.md) — the boundary these comparisons draw on.
