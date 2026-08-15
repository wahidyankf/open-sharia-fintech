---
title: "Honest reads and safe delivery"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

The easiest experiment to misread is one that reports a pleasing number early. The following examples
make common artifacts visible. Their purpose is not cynicism; it is to leave a team with a result it
can defend after the novelty fades, the calendar changes, and a reviewer asks who was excluded.

## Preserve the promised error rate

| Example                             | Decision artifact                                         | Verify                                                | Concepts |
| ----------------------------------- | --------------------------------------------------------- | ----------------------------------------------------- | -------- |
| ex-55 · peeking-simulation          | A null experiment inspected after each batch.             | Stopping on first p < .05 exceeds 5% false positives. | co-15    |
| ex-56 · peeking-false-positive-rate | Realized alpha across number of looks.                    | More looks produce more inflation.                    | co-15    |
| ex-57 · fixed-sample-fixes-peeking  | One analysis at the committed N.                          | Long-run false-positive rate returns near alpha.      | co-15    |
| ex-58 · always-valid-sequential     | A documented e-value or always-valid procedure.           | Continuous monitoring retains its stated control.     | co-15    |
| ex-59 · alpha-spending              | A cumulative alpha budget across planned looks.           | Spent alpha never exceeds target alpha.               | co-15    |
| ex-60 · simpsons-paradox-demo       | Segment rates and aggregate rate in one table.            | Treatment wins per segment but loses in aggregate.    | co-17    |
| ex-61 · simpsons-segment-weighting  | Reweighted comparison with an explicit target population. | Equal exposure restores the within-segment direction. | co-17    |

The correction for peeking is decided before the first look: use a fixed horizon or a validated
sequential method. Likewise, segmenting is not automatically more honest; causal structure tells
which conditioning is relevant. Aggregate and segment results must show their denominators and
population mix.

## Separate product change from time and selection

| Example                           | Decision artifact                                      | Verify                                             | Concepts |
| --------------------------------- | ------------------------------------------------------ | -------------------------------------------------- | -------- |
| ex-62 · novelty-effect-decay      | Daily effect series that spikes then settles.          | Day-one lift exceeds the steady-state value.       | co-20    |
| ex-63 · primacy-effect            | Daily effect series that dips then recovers.           | An early read would reject a later-neutral change. | co-20    |
| ex-64 · seasonality-weekly        | Weekday/weekend baseline series.                       | A partial-week comparison misreads the calendar.   | co-21    |
| ex-65 · ramp-up-exposure          | Exposure percentage by day.                            | Pooling ramp days changes the intended estimate.   | co-21    |
| ex-66 · survivorship-bias-demo    | Intent-to-treat cohort beside end-of-funnel survivors. | Survivor-only analysis flatters the change.        | co-22    |
| ex-67 · correlation-not-causation | Observational association with a confounder.           | Naive regression finds a spurious association.     | co-23    |
| ex-68 · confounder-randomization  | The same outcome under random allocation.              | The spurious association disappears.               | co-23    |

Run long enough to cover a stated full cycle, and report ramp exposure rather than treating partial
delivery as an ordinary stationary arm. The analysis population is the assigned cohort: users who
leave are evidence, not inconvenient rows to remove.

## Deliver value, not a dashboard victory

| Example                              | Decision artifact                                      | Verify                                                                   | Concepts            |
| ------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------- |
| ex-69 · goodhart-proxy-harm          | Click gain beside declining retained creation.         | Proxy rises while the valued outcome falls.                              | co-24               |
| ex-70 · metrics-theater-dashboard    | Green vanity cards plus OEC and guardrail.             | The OEC/guardrail pair catches the harm.                                 | co-24               |
| ex-71 · guardrail-catches-regression | A significant OEC result with a latency breach.        | The typed gate returns no-ship.                                          | co-07               |
| ex-72 · underpowered-test-noise      | Repeated low-N experiments.                            | Intervals are wide and conclusions vary.                                 | co-12               |
| ex-73 · when-not-to-ab-test          | Reachable traffic versus required N.                   | The tool recommends judgment and qualitative work when N is unreachable. | co-12               |
| ex-74 · bayesian-decision-rule       | Expected-loss threshold and stopping rule.             | It can differ from a frequentist decision.                               | co-25               |
| ex-75 · feature-flag-ramp-experiment | 1% to 50% ramp with persistent assignment.             | Eligible users retain their original arm.                                | co-26               |
| ex-76 · holdout-group                | Long-running unexposed group.                          | The holdout preserves a cumulative comparison.                           | co-26               |
| ex-77 · end-to-end-honest-experiment | Instrument, assign, pre-commit, SRM-check, and decide. | A known null does not become a ship claim.                               | co-09, co-10, co-18 |
| ex-78 · decision-memo-reconcile      | Memo fields read from analysis output.                 | Every stated figure equals its computed source.                          | co-09, co-07        |

### Worked decision rule

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionInput:
    ci_low: float
    practical_lift: float
    guardrail_passes: bool
    srm_passes: bool


def may_ship(result: DecisionInput) -> bool:
    return result.srm_passes and result.guardrail_passes and result.ci_low >= result.practical_lift


assert not may_ship(DecisionInput(0.03, 0.02, False, True))
assert not may_ship(DecisionInput(0.03, 0.02, True, False))
```

The decision rule is intentionally conservative: a positive-looking estimate cannot compensate for
invalid randomization or a harmed guardrail. If traffic cannot support the planned MDE, do not run a
performative A/B test; make a reversible judgment call, gather qualitative evidence, or change the
question.

← Previous: [Experiment design and analysis](./experiment-design-and-analysis) · Next:
[Capstone](./capstone/overview) →
