---
title: "PRs Open at Delivery Boundaries — Boundary Test and Rationale"
description: Gives the four-part boundary test (coherent, green standalone, defensible on main, reviewable whole) and the rationale for grouping phases into delivery units.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when testing whether a specific phase qualifies as a delivery boundary.
---

# PRs Open at Delivery Boundaries — Boundary Test and Rationale

Continues [PRs Open at Delivery Boundaries — Rules 5-7 and \*-to-pr Scope](./prs-open-at-delivery-boundaries-rules-continued.md).

**The boundary test** — a phase is a delivery boundary when all four hold:

- **(a) Coherent** — the accumulated increment is a complete unit of meaning (a capability, a
  migration step, a governance rule), not half a refactor.
- **(b) Green standalone** — every quality gate passes on the increment alone.
- **(c) Defensible on `main`** — if the plan stopped forever right here, `main` is in a state the
  team would accept: working, or complete-and-inert behind a feature flag.
- **(d) Reviewable whole** — a reviewer can judge it without reading phases that do not exist yet.

A phase that fails any of these is an **intermediate phase**, not a boundary. Typical intermediate
phases: scaffolding a schema nothing reads yet, extracting a helper the next phase consumes, writing
a fixture the next phase asserts on.

**Why this is a hard rule**: a PR per phase spends a full discipline-specialist fan-out, a synthesis
pass, a fixer pass, and up to five CI-gated cycles reviewing scaffolding that the very next phase
rewrites — and the review cannot judge the work's intent, because the intent only becomes visible two
phases later. Grouping to the natural boundary makes each review see one complete thought.

The counterweight is rule 6 in [PRs Open at Delivery Boundaries — Rules 5-7](./prs-open-at-delivery-boundaries-rules-continued.md): the same instinct, over-applied, produces one end-of-plan mega-PR
that no reviewer can hold in their head and that diverges from `main` for the plan's whole lifetime.
Delivery boundaries are the calibration point between those two failure modes.

See [Delivery Boundaries Declaration and Applicability](./delivery-boundaries-and-applicability.md) for the required declaration format and enforcement.
