---
title: "Decision memo"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 2
---

## Decision

**Do not widen the fictional editor-layout rollout.** The seeded treatment improves the OEC
(save conversion), but it regresses the pre-declared p95 latency guardrail. This is a product
decision, not a claim that the layout has no effect. The next action is to investigate the latency
mechanism and run a newly planned experiment only after changing the treatment or its delivery.

## Pre-committed plan

| Field                     | Value                                                                                           |
| ------------------------- | ----------------------------------------------------------------------------------------------- |
| Hypothesis                | The layout increases completed saves by at least 2 percentage points without worse p95 latency. |
| OEC                       | Deduplicated `edit_saved` users divided by assigned users.                                      |
| Guardrail                 | Treatment p95 latency must remain at or below the 500 ms budget.                                |
| Allocation                | Persistent 50/50 hash of `user_id` and `editor-layout-v1` salt.                                 |
| Minimum detectable effect | 0.02 absolute conversion points.                                                                |
| Sample estimate           | 4,224 users per arm, using the course's approximate 80%-power planning rule.                    |
| Stopping rule             | Fixed horizon; no daily fixed-horizon p-value peeking.                                          |

## Computed result

The values below are the fixed transcript produced by `python3 code/honest_experiment.py`.

| Reading                         | Result                         |
| ------------------------------- | ------------------------------ |
| Control conversion              | 12.00% (96 / 800)              |
| Treatment conversion            | 18.00% (144 / 800)             |
| Absolute lift                   | 6.00 percentage points         |
| 95% CI for lift                 | [2.51, 9.49] percentage points |
| Two-sided p-value               | 0.0007                         |
| SRM p-value                     | 1.0000; pass                   |
| Control / treatment p95 latency | 420 ms / 560 ms                |
| Guardrail                       | Fail                           |
| Decision                        | `NO_SHIP_GUARDRAIL`            |

The script also evaluates a 10% versus 10% known-null fixture. It returns a zero lift, a confidence
interval containing zero, and p-value 1.0000. That check is a regression guard against claiming
significance merely because an analysis path exists.

## Integrity review

- **SRM:** the observed allocation matches the expected 50/50 split, so the analysis may proceed.
  A failed SRM would stop the analysis before the effect is reported.
- **Peeking:** this example uses a fixed-horizon decision. A real team must either wait for the
  committed N or pre-specify an appropriate sequential procedure; it must not repeatedly test and
  stop at the first green value.
- **Multiple comparisons:** save conversion is the one OEC. Latency is a declared guardrail, not an
  opportunistically selected supporting metric. A larger planned metric family needs a correction.
- **Population:** report the assigned cohort, including people who did not save. Do not condition on
  surviving the funnel.
- **Time and delivery:** run through a complete product cycle, state ramp exposure, and preserve a
  holdout if assessing cumulative effect. Do not generalize a novelty spike into steady-state value.

## Evidence-to-action handoff

The owner should profile the synthetic latency path, set a repair acceptance criterion against the
same guardrail, and produce a fresh plan before a retry. Changing the OEC, MDE, allocation, or
stopping rule after seeing this result would turn an experiment into metrics theater. The memo stays
reconciled only because its figures originate from the code's immutable input and calculations.
