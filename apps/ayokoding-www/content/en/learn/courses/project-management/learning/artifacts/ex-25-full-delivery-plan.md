---
title: "Artifact: Full Delivery Plan — Aurora Checkout Redesign"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 65
---

> Aurora Checkout Redesign -- full delivery plan -- exercises co-01, co-03, co-04, co-05, co-07,
> co-09, co-10.

## Work breakdown structure

```text
Checkout Redesign
1.0 Payment Integration
  1.1 Stripe provider adapter
  1.2 PayPal provider adapter
  1.3 Apple Pay provider adapter
2.0 Cart and Order Flow
  2.1 Cart persistence rework
  2.2 Order summary UI
  2.3 Order confirmation email
3.0 Quality and Launch
  3.1 Checkout end-to-end test suite
  3.2 Load test at 3x peak traffic
  3.3 Feature-flag rollout plan
```

## Critical path

**2.1 -> 2.2 -> 3.1 -> 3.2 -> 3.3, 17 working days, zero slack.** This chain, not any single
payment-adapter branch, drives the November 15 launch date.

## Velocity estimate

41 points total, 15-point average velocity (three sprints: 14, 17, 15) -> forecast **3 sprints**.

## Sprint plan

| Sprint   | Committed items                                                                                               | Points |
| -------- | ------------------------------------------------------------------------------------------------------------- | ------ |
| Sprint 1 | 2.1 Cart persistence rework (8), 1.2 PayPal adapter (5)                                                       | 13     |
| Sprint 2 | 1.1 Stripe adapter (5), 1.3 Apple Pay adapter (3), 2.2 Order summary UI (3), 2.3 Order confirmation email (2) | 13     |
| Sprint 3 | 3.1 E2E test suite (8), 3.2 Load test (5), 3.3 Feature-flag rollout (2)                                       | 15     |

Matches the 3-sprint forecast exactly; every task's dependencies are satisfied by an earlier sprint.

## Risk register (current snapshot)

| #   | Risk                                                                                       | Score | Mitigation                                                                                                  | Owner                 |
| --- | ------------------------------------------------------------------------------------------ | ----- | ----------------------------------------------------------------------------------------------------------- | --------------------- |
| 1   | Apple Pay API introduces a breaking change before launch                                   | 12    | Pin the SDK version, subscribe to Apple's developer changelog, smoke-test weekly against the sandbox.       | Dinar (payments lead) |
| 2   | Load test reveals checkout cannot sustain 3x peak traffic                                  | 15    | Run the load test three weeks before launch, reserve autoscaling headroom, keep a feature-flag kill switch. | Priya (SRE)           |
| 3   | Bayu (only engineer who knows legacy cart-persistence code) on scheduled leave in Sprint 2 | 15    | Pair a full walkthrough session before leave starts, document quirks in a runbook.                          | Bayu (tech lead)      |
| 4   | Holiday code-freeze policy shortens the usable schedule by one week                        | 12    | Confirm the exact freeze date now; build the week into the schedule buffer.                                 | Dinar                 |
| 5   | Finance requests a sixth payment provider mid-project                                      | 9     | Route through the change-management decision process.                                                       | PM (Aurora)           |

## Metrics plan

| Metric                       | Decision it informs                                                                     |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| Burndown (per sprint)        | Flatline for 2+ days mid-sprint -> investigate a blocker the same day.                  |
| Cycle time (E2E-suite stage) | Trending up for 2 consecutive weeks -> add QA capacity or lower that stage's WIP limit. |

## Internal consistency

The critical path (17 days) drives the schedule commitment, not any individual payment-adapter
branch. The 3-sprint velocity estimate aligns exactly with the 3-sprint plan. Every metric names a
concrete decision. The risk register's top-ranked risks (by score) have mitigations already in
flight.
