---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Analytics turns product behavior into inspectable evidence; experimentation turns a proposed change
into a fair comparison. This course follows fictional **Lantern Notes**, a note-sharing product:
define events before emitting them, reconcile a funnel and cohort, select an outcome and guardrails,
then decide whether a randomized change earns a wider rollout. The durable habit is simple: a metric
is only as honest as its collection, comparison, and stopping rule.

This is a **By Example** course. Its compact Python mechanisms are fully type-annotated, deterministic,
and offline. They model event contracts, bucketing, calculations, and decisions without analytics
SDKs, a live feature-flag service, customer data, credentials, network calls, or writes outside an
in-memory database. They are teaching mechanisms, not production analytics infrastructure.

## Prerequisites

- [SQL Essentials](/en/learn/courses/sql-essentials) supplies aggregation, joins, and grouping over an
  event table.
- [Software Testing](/en/learn/courses/software-testing) supplies the controlled-comparison mindset:
  state the claim and the pass bar before looking at the result.

## Scope boundary

`statistics-for-evaluation` is this course's scope-boundary sibling. It teaches **evals-only**
uncertainty, sampling, judge concordance, and significance testing for deciding whether an AI
evaluation result is trustworthy. This course teaches **classical product metrics and A/B testing**:
event instrumentation, funnels, retention, guardrails, randomized product delivery, and an honest
ship/no-ship decision. Both courses use intervals and hypothesis tests; neither substitutes for the
other. In particular, judge concordance belongs in
[Statistics for Evaluation](/en/learn/courses/statistics-for-evaluation), not in this product
experimentation course.

## The decision loop

1. Specify event names, property types, ownership, and a stable event ID before code emits data.
2. Measure a user journey with distinct-user funnels, cohorts, and appropriately sized segments.
3. Pre-commit a hypothesis, OEC, guardrails, allocation, exposure window, minimum detectable effect,
   and sample size.
4. Randomize persistently and independently, validate the assignment split, and analyze effect size
   with its uncertainty rather than a dashboard color alone.
5. Reject misleading reads: optional stopping, many unplanned comparisons, unequal segment mix,
   novelty, seasonality, survivorship, correlation, and proxy optimization.
6. Deliver through a flag with a deliberate ramp and holdout; write the decision memo from computed
   evidence.

## Concept register

- **co-01 to co-05 · collection and behavior** — tracking plans, idempotent events, conversion
  funnels, retention cohorts, and segmentation.
- **co-06 to co-08 · metric design** — north-star/input trees, guardrails, and ratio-metric
  treachery.
- **co-09 to co-14 · pre-committed comparison** — hypothesis/OEC, persistent randomized assignment,
  error and power, sample size/MDE, p-values, and confidence intervals.
- **co-15 to co-19 · analysis integrity** — optional stopping, multiple comparisons, Simpson's
  paradox, sample-ratio mismatch (SRM), and CUPED variance reduction.
- **co-20 to co-26 · interpretation and delivery** — novelty and primacy, seasonality and ramp,
  survivorship, correlation versus causation, Goodhart's law, inference frameworks, and feature flags.

## Primary-source reading

- [Kohavi et al., _Controlled experiments on the web_](https://link.springer.com/article/10.1007/s10618-008-0114-1)
  — OECs, persistent randomization, sample-size planning, ramp-up, and novelty effects.
- [ASA statement on p-values](https://doi.org/10.1080/00031305.2016.1154108) — what a p-value does
  and does not establish.
- [NIST e-Handbook: hypothesis testing](https://www.itl.nist.gov/div898/handbook/prc/section1/prc13.htm)
  and [sample sizes](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm) — Type I/II
  error, power, and design inputs.
- [Deng et al., CUPED](https://dl.acm.org/doi/10.1145/2433396.2433413) — pre-experiment covariates
  as variance reduction.
- [Fabijan et al., SRM diagnosis](https://dl.acm.org/doi/10.1145/3292500.3330722) — why a broken
  assignment split invalidates an experiment.
- [Johari, Pekelis, and Walsh, always-valid inference](https://arxiv.org/abs/1512.04922) — why a
  fixed-horizon p-value cannot be repeatedly inspected and stopped at significance.
- [Stanford Encyclopedia: Simpson's Paradox](https://plato.stanford.edu/entries/paradox-simpson/) —
  aggregation reversals and causal conditioning.

## Accuracy and safety notes

The statistical spine is deliberately vendor-neutral and durable. No hosted analytics provider,
SDK version, or feature-flag product is required; Segment's Python SDK is not used because its
maintenance status makes it a poor teaching dependency. A Bayesian treatment is conceptual only:
it must use a coherent prior, loss, and stopping rule rather than translating a frequentist p-value
into a posterior probability. Never put personal data, secrets, full URLs with query strings, or
unbounded identifiers into analytics properties; use reviewed, minimal, purpose-bound schemas.

Next: [Learning overview](./learning/overview.md) →

## Legacy relation

Superseded by: this canonical course replaces the overlapping legacy analytics material; the historical
material remains available during the transition.
