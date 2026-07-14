---
title: "Artifact: Story-Point Estimate — Checkout Redesign"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 46
---

> Aurora Checkout Redesign -- story-point estimate -- exercises co-05.

Reference story: **1.2 PayPal adapter = 5 points** (near-identical to a prior integration the team
has already built).

| Backlog item                   | Points | Reasoning relative to the reference (1.2 = 5)                    |
| ------------------------------ | ------ | ---------------------------------------------------------------- |
| 1.1 Stripe adapter             | 5      | Same shape of work as the reference story.                       |
| 1.2 PayPal adapter (reference) | 5      | The reference story itself.                                      |
| 1.3 Apple Pay adapter          | 3      | Smaller -- reuses the adapter interface the first two establish. |
| 2.1 Cart persistence rework    | 8      | Bigger -- touches shared state across the whole checkout flow.   |
| 2.2 Order summary UI           | 3      | Similar size to the smaller adapter story.                       |
| 2.3 Order confirmation email   | 2      | Smallest item in the backlog.                                    |
| 3.1 Checkout E2E test suite    | 8      | Bigger -- spans all three payment paths.                         |
| 3.2 Load test                  | 5      | Same rough size as an adapter story.                             |
| 3.3 Feature-flag rollout plan  | 2      | Small, well-understood mechanism.                                |
| **Total**                      | **41** |                                                                  |
