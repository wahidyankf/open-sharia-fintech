---
title: "Artifact: Sprint and Backlog Plan — Checkout Redesign"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 49
---

> Aurora Checkout Redesign -- sprint and backlog plan -- exercises co-07.

| Sprint               | Committed items                                                                                               | Points | Dependency check                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------- |
| Sprint 1             | 2.1 Cart persistence rework (8), 1.2 PayPal adapter (5)                                                       | 13     | Neither item has an unmet prerequisite.                                                  |
| Sprint 2             | 1.1 Stripe adapter (5), 1.3 Apple Pay adapter (3), 2.2 Order summary UI (3), 2.3 Order confirmation email (2) | 13     | 2.2 and 2.3 depend on 2.1, which finished in Sprint 1; 1.1 and 1.3 have no prerequisite. |
| (Sprint 3, forecast) | 3.1 E2E test suite (8), 3.2 Load test (5), 3.3 Feature-flag rollout (2)                                       | 15     | All three depend on the payment adapters and 2.2, all complete by end of Sprint 2.       |

Velocity ceiling: 15 points/sprint (three-sprint average). Neither Sprint 1 nor Sprint 2 exceeds it,
and no committed task precedes a dependency not scheduled in an earlier sprint.
