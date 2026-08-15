---
title: "Capstone overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Run one honest, local experiment for fictional Lantern Notes: insert typed events into an in-memory
SQLite table; reconcile a funnel and retention cohort; pre-commit an OEC, guardrails, MDE, and sample
size; assign users persistently; validate SRM; calculate conversion lift, confidence interval, and
p-value; and make a decision that a guardrail can veto. The capstone is a reviewable practice loop,
not a deployment or a recommendation about a real product.

## Build order

1. Run `python3 code/honest_experiment.py`. It has fixed synthetic data, standard-library imports,
   assertions, no network calls, no external input, and no persistent file or database writes.
2. Read the typed `TrackingEvent` and `ExperimentPlan` before changing any fixtures. Their fields are
   the tracking and analysis contracts, not optional dashboard labels.
3. Verify the funnel counts from deduplicated events and the retention denominator from the original
   signup cohort.
4. Confirm the plan's sample size was calculated before the result; confirm SRM passes before reading
   the effect; then compare the interval against the practical lift and guardrail.
5. Read [the decision memo](./decision-memo.md). Its numbers are deliberately reconciled to program
   output; revise both only by changing a fixture and rerunning the calculation.

## Concepts exercised

- [x] tracking plan, idempotency, funnel, cohort, and segmentation (co-01 through co-05)
- [x] north-star OEC, guardrails, and ratio-safe conversion inputs (co-06 through co-09)
- [x] persistent allocation, planned MDE/sample size, p-value, and confidence interval (co-10 through co-14)
- [x] pre-committed stopping, SRM gate, and named analysis integrity checks (co-15 through co-18)
- [x] ramp/seasonality/survivorship review and flag/holdout delivery constraints (co-20 through co-26)

## Acceptance criteria

- The event table's primary key drops a deliberate retry, and the funnel is monotonically non-increasing.
- The retention denominator is the original signup cohort, not only later active users.
- The plan prints a concrete per-arm sample-size estimate before the observed outcome.
- The persistent hash mapping is used for every simulated user, and the clean assignment passes SRM.
- The known-null fixture is not significant; the seeded positive lift is still **no ship** because its
  latency guardrail regresses.
- The decision memo's OEC, lift, interval, p-value, SRM, and guardrail readings match the program.

## Done bar

A reviewer can execute one safe script, trace every claim to a stated input, and explain why a
positive conversion result does not override a broken guardrail. Before using this pattern in a real
system, add approved privacy controls, durable storage, a reviewed statistical package, ownership,
and an appropriate sequential or fixed-horizon governance policy.

← Previous: [Honest reads and safe delivery](../honest-reads-and-safe-delivery.md) · Next:
[Drilling](../../drilling/overview.md) →
