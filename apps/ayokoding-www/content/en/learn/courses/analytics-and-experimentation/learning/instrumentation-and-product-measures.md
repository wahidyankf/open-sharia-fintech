---
title: "Instrumentation and product measures"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

Before asking whether a change helped, make the measurement contract dependable. Lantern Notes has a
three-step sharing journey: view a shared note, begin editing, then save an edit. The unit of a
funnel is usually a distinct user who reached a step, not the number of retried HTTP requests.

## Event contracts and funnels

| Example                           | Decision artifact                                                  | Verify                                                 | Concepts |
| --------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------ | -------- |
| ex-01 · tracking-plan-doc         | A table with event name, owner, purpose, and permitted properties. | Every emitted event has a declared row.                | co-01    |
| ex-02 · event-schema-typed        | A typed union for `View`, `EditStarted`, and `EditSaved`.          | A missing required property cannot construct an event. | co-01    |
| ex-03 · emit-events-to-table      | A reviewed writer for an in-memory `events` table.                 | A row has an event ID, user, name, and timestamp.      | co-01    |
| ex-04 · idempotency-key-dedup     | A stable event ID is the table key.                                | Re-emitting an ID leaves one row.                      | co-02    |
| ex-05 · client-vs-server-event    | Server confirmation is authoritative for a save.                   | Retry duplicates cannot outvote the confirmation.      | co-02    |
| ex-06 · avoid-double-count        | A deduplicated count beside a naive count.                         | The naive count is larger on a retry fixture.          | co-02    |
| ex-07 · count-distinct-users      | `COUNT(DISTINCT user_id)` for funnel steps.                        | Repeated views do not enlarge the first step.          | co-03    |
| ex-08 · conversion-funnel-sql     | Ordered distinct-user step counts.                                 | Each later step is no larger than its predecessor.     | co-03    |
| ex-09 · funnel-step-dropoff       | Step retention and drop-off percentages.                           | Retention plus drop-off is 100% per transition.        | co-03    |
| ex-10 · funnel-overall-conversion | Completed divided by visitors.                                     | It equals the product of step-retention rates.         | co-03    |

### Worked mechanism: an idempotent event is a business fact

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Event:
    event_id: str
    user_id: str
    name: str


EVENTS: Final[tuple[Event, ...]] = (
    Event("save-007", "user-7", "edit_saved"),
    Event("save-007", "user-7", "edit_saved"),  # a safe retry, not a second save
)


def deduplicate(events: tuple[Event, ...]) -> tuple[Event, ...]:
    by_id: dict[str, Event] = {event.event_id: event for event in events}
    return tuple(by_id.values())


assert len(EVENTS) == 2
assert len(deduplicate(EVENTS)) == 1
```

The dictionary is not a complete production pipeline; it exposes the invariant. The stable ID says
what one business action is, so retries cannot rewrite a conversion rate. Do not use a timestamp as
an idempotency key: equal actions can have different times, and retries can have different arrival
times.

## Cohorts and segmentation

| Example                       | Decision artifact                                       | Verify                                                  | Concepts |
| ----------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | -------- |
| ex-11 · cohort-by-signup-week | Each user is assigned to their first signup week.       | A user appears in exactly one cohort.                   | co-04    |
| ex-12 · retention-curve       | Day 1, 7, and 30 active-user proportions.               | Each point names its cohort and denominator.            | co-04    |
| ex-13 · n-day-retention       | A choice between exact-day and bounded-range retention. | The same fixture yields different definitions.          | co-04    |
| ex-14 · segment-by-property   | Conversion split by platform.                           | Weighted segment numerators and denominators reconcile. | co-05    |
| ex-15 · segment-funnel        | Country-specific funnel with an explicit minimum count. | A tiny segment is labeled inconclusive.                 | co-05    |

Retention does not have one universal definition. State whether “day 7” means active exactly on day
7 or active during a chosen window, keep the denominator as the original cohort, and do not quietly
drop users who churned. A segment is a diagnostic question, not permission to mine every property
until something is green.

## Choose a metric that resists gaming

| Example                          | Decision artifact                                                         | Verify                                                  | Concepts |
| -------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------- | -------- |
| ex-16 · north-star-definition    | Weekly active creators as a function over deduplicated events.            | One period returns one stated measure.                  | co-06    |
| ex-17 · north-star-input-tree    | Inputs for activation, repeat creation, and successful sharing.           | Inputs explain value without pretending to sum exactly. | co-06    |
| ex-18 · guardrail-metric-list    | p95 latency and save-error thresholds.                                    | Each has a direction, threshold, and owner.             | co-07    |
| ex-19 · ratio-metric-trap        | Per-user average compared with total clicks divided by total impressions. | The two values disagree on unequal denominators.        | co-08    |
| ex-20 · sample-mean-and-variance | Mean, variance, and standard error.                                       | Repeated larger samples reduce standard error.          | co-14    |
| ex-21 · mean-ci-normal           | A normal-approximation interval for a continuous metric.                  | Simulation coverage is close to its stated level.       | co-14    |
| ex-22 · proportion-ci            | Wald and Wilson intervals near a boundary.                                | Wilson stays inside [0, 1] when Wald does not.          | co-14    |
| ex-23 · effect-size-abs-rel      | Absolute and relative conversion lift.                                    | Relative lift equals absolute lift divided by control.  | co-14    |
| ex-24 · minimum-detectable-diff  | An MDE derived from a fixed sample budget.                                | Increasing N lowers the stated MDE.                     | co-12    |
| ex-25 · hypothesis-statement     | Typed null, alternative, sidedness, and decision bar.                     | Analysis reads—not invents—the pre-written direction.   | co-09    |
| ex-26 · oec-definition           | An OEC that penalizes a retention harm behind a click gain.               | A proxy-gaming fixture loses on the OEC.                | co-09    |

**Key takeaway:** a north-star metric gives a team direction; guardrails preserve constraints; an
OEC makes the experiment's actual decision rule explicit. No single proxy can carry all three jobs.
For a ratio, retain additive numerators and denominators so its uncertainty can be calculated rather
than averaged away.

← Previous: [Learning overview](./overview) · Next:
[Experiment design and analysis](./experiment-design-and-analysis) →
