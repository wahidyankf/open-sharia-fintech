---
title: "Blameless postmortem"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 2
---

## Incident summary

**Date:** fictional 2026-08-15. **Service:** Harbor Checkout. **Impact:** synthetic payment
requests returned errors above the 99.9% availability objective during the simulated evaluation
window. **Severity:** SEV-2 in this exercise because the checkout journey was materially affected,
but recovery and communication were still manageable within one service team.

This is a teaching artifact based only on the fixed fixture in
[`sre_loop.py`](./code/sre_loop.py). It describes no real outage, account, customer, or production
system.

## Timeline

| Time  | Observation or decision                                                                              |
| ----- | ---------------------------------------------------------------------------------------------------- |
| 10:00 | Synthetic checkout traffic begins; baseline requests are successful.                                 |
| 10:02 | The fixture introduces four failed checkouts and higher latency.                                     |
| 10:03 | The availability SLI falls below the target and the calculated burn rate exceeds the page threshold. |
| 10:04 | Incident commander confirms user impact; operations lead checks the bounded signal summary.          |
| 10:06 | Communications lead records the known impact and next update time.                                   |
| 10:10 | The exercise removes the failing fixture; later requests are successful.                             |
| 10:15 | Team reviews the timeline and chooses prevention work.                                               |

## What happened and why

The synthetic failure sequence concentrated bad events in a small window. The SLI's definition
correctly counted those events as user-visible failures, so the alert's symptom condition was met.
The simulation also reported high worker utilization. That saturation signal supported a capacity
investigation, but it was not treated as the incident's sole cause: the fixture does not prove a
causal relationship. This distinction prevents a convenient internal graph from displacing evidence
of what users experienced.

The system had useful defenses: a defined SLI, an objective, an alert route, and clearly assigned
roles. It lacked a reviewed capacity-headroom policy for the simulated worker pool and a concise
first-response runbook for separating payment-dependency errors from local saturation.

## Action items

| Action                                                                           | Owner role                  | Review date             | Success evidence                                                                  |
| -------------------------------------------------------------------------------- | --------------------------- | ----------------------- | --------------------------------------------------------------------------------- |
| Add a service-specific capacity-headroom policy and test it with synthetic load. | Operations lead             | Next reliability review | Policy names a saturation threshold, window, and capacity action.                 |
| Write a short symptom-page runbook for checkout errors.                          | Service owner               | Next on-call rotation   | A responder can identify the SLI, diagnostic signals, mitigation, and escalation. |
| Add a regression fixture for a short non-impacting saturation spike.             | Reliability engineer        | Next code review        | The fixture routes to a ticket or silence, never an unnecessary page.             |
| Review alert noise and missed symptoms monthly.                                  | Incident commander rotation | Monthly                 | Review notes show changes, retained alerts, and rationale.                        |

## Blamelessness check

The postmortem names conditions, evidence, interfaces, and decisions. It does not name a person as
the cause or prescribe “be more careful.” If a real incident reveals a human action, investigate the
system that made that action plausible—information, tooling, review, defaults, workload, and
guard-rails—then improve that system.
