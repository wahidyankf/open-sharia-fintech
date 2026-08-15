---
title: "Telemetry and service signals"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

Telemetry is useful only when it explains a decision about a user journey. Harbor's checkout is a
good teaching target because a slow or failed payment attempt is observable by the user. A CPU graph
alone is not an SLI; it may be useful diagnostic evidence after a user-facing signal changes.

## Instrument the four golden signals

| Scenario                      | Decision artifact                                            | Verification                                                 | Concepts     |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------ |
| ex-01 · instrument-latency    | Record checkout duration in milliseconds.                    | A 120 ms request produces a 120 ms observation.              | co-08, co-16 |
| ex-02 · instrument-traffic    | Increment a request counter for each checkout attempt.       | Three attempts yield a count of three.                       | co-09, co-16 |
| ex-03 · instrument-errors     | Count a failed checkout separately from all traffic.         | A synthetic 5xx increments failures.                         | co-10, co-16 |
| ex-04 · instrument-saturation | Record a bounded worker-queue utilization ratio.             | Eight busy of ten slots reports 0.80.                        | co-11, co-16 |
| ex-05 · metrics-endpoint      | Define an endpoint contract containing named numeric series. | The contract lists latency, traffic, errors, and saturation. | co-12, co-18 |
| ex-06 · prometheus-scrape     | Specify pull collection at a stable metrics endpoint.        | The collector, path, and interval are explicit.              | co-18        |
| ex-07 · counter-metric        | Use a monotonically increasing request total.                | The value never decreases across observations.               | co-12        |
| ex-08 · gauge-metric          | Use a current in-flight-request value.                       | The value may rise and fall.                                 | co-12        |
| ex-09 · histogram-latency     | Bucket request durations for percentile estimation.          | A slow request lands in an upper bucket.                     | co-08, co-12 |

**Key takeaway:** the golden signals are a compact shared vocabulary: latency tells whether the
journey is timely, traffic whether demand changed, errors whether it succeeds, and saturation
whether a finite resource is near its limit. They are not a mandate to page on every internal
fluctuation.

## Preserve context across the three signal types

| Scenario                   | Decision artifact                                                        | Verification                                                            | Concepts     |
| -------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------- | ------------ |
| ex-10 · structured-log     | Emit fields for event, status, duration, and correlation ID.             | The line is machine-queryable without parsing prose.                    | co-13        |
| ex-11 · log-correlation-id | Give all records for one checkout the same request ID.                   | A search joins related records by ID.                                   | co-13        |
| ex-12 · trace-span         | Model a bounded checkout operation with start and end time.              | Duration is end minus start.                                            | co-14        |
| ex-13 · trace-propagation  | Carry one trace ID from checkout to payment dependency.                  | Two spans share a trace ID.                                             | co-14        |
| ex-14 · otel-sdk-setup     | Select vendor-neutral instrumentation boundaries.                        | Signal names and attributes are documented before export.               | co-17        |
| ex-15 · otel-collector     | Separate application emission from backend export policy.                | A collector boundary permits a backend change without app logic change. | co-17        |
| ex-16 · three-pillars      | Correlate metric change, structured log, and trace for one slow request. | All three name the same request ID or time window.                      | co-15        |
| ex-17 · nines-table        | Translate 99.9% and 99.99% into allowed time in a stated 30-day window.  | The calculation shows the window and units.                             | co-07        |
| ex-18 · availability-calc  | Divide good checkout events by total valid events.                       | 998 good of 1,000 yields 99.8%.                                         | co-02, co-10 |

## Worked mechanism: synthetic signal ledger

The capstone's [local Python program](./capstone/code/sre_loop.py) records a bounded in-memory
ledger. The design is deliberately safer than a real agent: it accepts no external input, makes no
network connection, and returns immutable summaries. Its `RequestEvent` dataclass gives every field
a concrete type, which makes an SLI denominator and numerator reviewable before any alert is added.

**Why it matters:** observability is the ability to form and answer useful questions from emitted
evidence. That requires careful event semantics and correlation, not merely installing a dashboard.
Avoid high-cardinality identifiers and sensitive payment or personal data in labels or logs; a
correlation ID must be opaque and non-secret.

← Previous: [Learning overview](./overview) · Next:
[Objectives, budgets, and alerting](./objectives-budgets-and-alerting) →
