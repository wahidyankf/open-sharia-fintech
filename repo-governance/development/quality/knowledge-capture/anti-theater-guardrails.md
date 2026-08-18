---
title: "Anti-Theater Guardrails"
description: "Guardrails against performative knowledge capture."
category: explanation
subcategory: development
tags:
  - knowledge-capture
  - learnings
  - plans
  - triage
  - safety-gates
  - post-mortems
created: 2026-07-05
when_to_use: "Use when a learnings.md entry looks performative."
---

# Anti-Theater Guardrails

A knowledge-capture practice can fail in two opposite directions, and this convention guards against
both:

- **Under-capture** (nothing is ever recorded): the mandatory phase + the explicit "none" escape +
  the MEDIUM-severity checker finding on silent absence together make skipping the practice visible
  and flagged, not silently tolerated.
- **Over-capture** (everything is logged and nothing is ever triaged): the litmus test discards
  non-generalizable noise up front; archival being blocked on triage completion means an untriaged
  backlog of entries cannot simply accumulate forever inside a live plan.

Beyond that balance, the mechanism itself must avoid becoming theater:

- **Single named owner**: the plan executor who accrues `learnings.md` is also the one who runs the
  triage pass at the end of the same plan — no separate role, no hand-off, no committee.
- **Lives in a tool already opened**: `learnings.md` sits in the plan folder the executor already has
  open for `delivery.md`; this is deliberately NOT a new dashboard, ticketing system, or standalone
  tracker that requires a separate tool to maintain.
- **Fixed-cadence review**: the triage pass happens once, at a fixed point in the plan lifecycle (the
  final substantive phase, immediately before archival) — not on an ad-hoc or indefinitely deferred
  schedule.
