---
title: "Artifact: Full Product Brief Consistency Check — Kestrel Swap Approval"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 70
---

> A compact product brief assembled and checked for consistency -- exercises co-01, co-07, co-12,
> co-15, co-17. Kestrel is a fictional product; every quoted number, question, or finding here is
> an illustrative, constructed example, not real data or a real transcript.

**Problem/outcome**: managers currently lose track of routine swap requests for hours; the outcome
sought is routine swaps resolved within minutes, not a new "approval screen" feature for its own
sake.

**MVP scope**: fast-path SMS approval for routine, same-role, same-shift-length swaps only (the
riskiest-assumption test), with a per-team disable toggle; explicitly not a general workflow engine
and not cross-location swaps.

**RICE-ranked mini-backlog**:

| Item                           | Reach (per quarter) | Impact | Confidence | Effort (person-months) | RICE                        |
| ------------------------------ | ------------------- | ------ | ---------- | ---------------------- | --------------------------- |
| Fast-path SMS approval         | 500                 | 2      | 0.8        | 3                      | (500×2×0.8)÷3 = **266.7**   |
| Per-team disable toggle        | 500                 | 0.5    | 1.0        | 0.5                    | (500×0.5×1.0)÷0.5 = **500** |
| Approval-queue screen redesign | 300                 | 1      | 0.5        | 2                      | (300×1×0.5)÷2 = **75**      |

Ranked: disable toggle (500) > fast-path approval (266.7) > queue redesign (75) -- consistent with
the pitch's circuit-breaker, which keeps the toggle and the fast-path flow and cuts the queue
redesign first if time runs short.

**Metrics**: this feature is one of the north-star's three input-metric levers (shift-swap
completion rate) -- success here should move that input metric directly.

**Experiment**: hypothesis -- fast-path approval reduces median swap-request-to-decision time
without increasing manager-reported wrong-approvals. Primary metric (OEC): median time from swap
request to a final decision. Guardrail: manager-reported incorrect approvals (a swap that
shouldn't have qualified as "routine" but was auto-approved) must not increase.
