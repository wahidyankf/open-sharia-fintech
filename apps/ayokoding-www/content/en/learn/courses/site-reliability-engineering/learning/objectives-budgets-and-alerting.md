---
title: "Objectives, budgets, and alerting"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

An SLO is not a number selected for prestige. Harbor first defines a good checkout as one completed
without a server error within 500 ms, then agrees how that indicator supports its users and release
decisions. An SLA may use related evidence, but adds an external commitment and consequences; it is
not a substitute for the team's internal SLO.

## Turn a user journey into an objective

| Scenario                       | Decision artifact                                                      | Verification                                               | Concepts     |
| ------------------------------ | ---------------------------------------------------------------------- | ---------------------------------------------------------- | ------------ |
| ex-19 · define-sli             | `good checkout events / valid checkout events` over 30 days.           | Both numerator and denominator exclude no events silently. | co-02        |
| ex-20 · sli-availability       | Treat 5xx checkout responses as not good.                              | More failures lower the ratio.                             | co-02, co-10 |
| ex-21 · sli-latency            | Count only requests at or below 500 ms as timely.                      | A 700 ms success is not good for this SLI.                 | co-02, co-08 |
| ex-22 · define-slo             | Target 99.9% good events over a rolling 30-day window.                 | Target, window, and owner are stated.                      | co-03        |
| ex-23 · error-budget-calc      | Calculate `1 - 0.999 = 0.001` allowed bad-event fraction.              | 99.9% creates a 0.1% budget.                               | co-05        |
| ex-24 · budget-consumed        | Compare observed bad fraction with the allowed fraction.               | A 0.08% bad fraction leaves 20% of budget.                 | co-05        |
| ex-25 · budget-velocity        | Pause risky releases after budget exhaustion, with an exception owner. | The policy names both the gate and recovery condition.     | co-06        |
| ex-26 · sla-vs-slo             | Record SLO as internal target and SLA as external consequence.         | The two statements have different audiences and effects.   | co-03, co-04 |
| ex-27 · burn-rate              | Divide observed bad-event rate by the budget rate.                     | A 1% bad rate against 0.1% budget burns at 10x.            | co-21        |
| ex-28 · multiwindow-burn-alert | Pair short and long windows before paging.                             | A brief spike alone does not meet both conditions.         | co-21        |

**Key takeaway:** an error budget is neither permission to break users nor a reason to freeze every
change. It is a jointly owned constraint that converts a recurring argument into an observable
policy. Higher availability can cost more in architecture, testing, operations, and slower delivery;
the target must be justified by the journey's consequences.

## Page on impact; investigate with diagnostics

| Scenario                        | Decision artifact                                                     | Verification                                           | Concepts     |
| ------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------ | ------------ |
| ex-29 · symptom-alert-rule      | Page on sustained failing or too-slow checkouts.                      | The condition contains user impact, not CPU alone.     | co-20        |
| ex-30 · cause-alert-antipattern | Mark high CPU with normal SLI as diagnostic, not a page.              | It opens investigation without waking on-call.         | co-20        |
| ex-31 · page-vs-ticket          | Route rapid budget burn to a page and low-priority drift to a ticket. | Each route has urgency and owner.                      | co-20, co-23 |
| ex-32 · alert-fatigue-prune     | Retire a recurring non-actionable page after confirming coverage.     | Page volume drops without hiding user impact.          | co-22        |
| ex-33 · slo-based-page          | Page when multi-window burn risks consuming budget quickly.           | A seeded failure meets the declared threshold.         | co-20, co-21 |
| ex-34 · quiet-under-normal      | Keep the page closed during normal synthetic traffic.                 | A healthy fixture returns `False`.                     | co-20        |
| ex-35 · alert-runbook-link      | Link each page to a short first-response runbook.                     | The runbook states check, mitigation, and escalation.  | co-23        |
| ex-36 · budget-policy           | Publish the release policy alongside the SLO.                         | Product and engineering owners can find the same rule. | co-05, co-06 |

## Worked mechanism: explicit alert routing

In the capstone, `classify_alert` accepts a measured burn rate and returns an `AlertRoute` enum. A
page requires a high sustained rate; lower but actionable drift becomes a ticket; healthy traffic is
silent. This is a teaching simplification, not a copied production alert rule. A real policy needs
service-specific windows, notification ownership, escalation coverage, and regular review of both
missed incidents and noisy pages.

**Why it matters:** alert fatigue is a reliability risk. A page asks a person to interrupt their
life; the system must earn that interruption with clear user impact and a useful action.

← Previous: [Telemetry and service signals](./telemetry-and-service-signals) · Next:
[Operations, learning, and capacity](./operations-learning-and-capacity) →
