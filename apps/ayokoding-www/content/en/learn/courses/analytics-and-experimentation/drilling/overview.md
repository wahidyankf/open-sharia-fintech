---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Use these five sections after the learning track. Every case is fictional. For a real experiment,
involve product, engineering, data, privacy, and any affected operational owners before collecting
events, exposing a flag, or communicating a decision.

## Recall Q&A

**Q1 (co-01, co-02).** Why must a tracking plan be written before instrumentation, and what makes
an event idempotent?

<details>
<summary>Answer</summary>

A tracking plan makes event name, purpose, owner, properties, types, and privacy constraints a
reviewable contract instead of an accidental data exhaust. An idempotent event has a stable ID for
one business action, so a retry can be stored or processed again without adding a second action to a
metric. The key must represent the business fact, not merely its arrival time.

</details>

**Q2 (co-03 through co-05).** What denominator belongs in a funnel, a retention cohort, and a
segment comparison?

<details>
<summary>Answer</summary>

A funnel normally counts distinct users who reached each ordered step. Retention keeps the original
entry cohort as its denominator even when users disappear later. A segment comparison keeps each
segment's own numerator and denominator, then reconciles those additive counts to the whole. Never
average segment rates without their weights.

</details>

**Q3 (co-06 through co-09).** How do a north-star metric, OEC, guardrail, and ratio metric differ?

<details>
<summary>Answer</summary>

A north-star metric aligns long-run delivered value; an OEC is the experiment's pre-selected outcome;
a guardrail is a result that must not regress even when the OEC improves. A ratio metric is a random
numerator divided by a random denominator, so it needs numerator/denominator-aware uncertainty rather
than an unweighted average of individual ratios.

</details>

**Q4 (co-10 through co-14).** What makes an A/B comparison causal, and what does a p-value not say?

<details>
<summary>Answer</summary>

Persistent, treatment-independent, approximately uniform random assignment makes the arms comparable
in expectation. Before exposure, commit the hypothesis, alpha, MDE, power, sample size, and decision
rule. A p-value is not the probability that the null is true and not the probability treatment works;
pair it with an effect size, confidence interval, practical bar, and guardrails.

</details>

**Q5 (co-15 through co-19).** What stops analysis before a winner can be reported?

<details>
<summary>Answer</summary>

A failed SRM stops analysis because the allocation mechanism may be broken. Fixed-horizon p-values
cannot be checked repeatedly and stopped at significance; honor the planned N or use a planned
sequential method. For a declared family, control multiplicity with an appropriate procedure.
CUPED may reduce variance only with a pre-treatment covariate.

</details>

**Q6 (co-20 through co-26).** Name four non-treatment explanations for an attractive metric move.

<details>
<summary>Answer</summary>

Novelty or primacy can change early behavior; weekly or holiday seasonality can change the baseline;
ramp exposure can mix populations; survivor-only analysis can exclude harmed users; confounding can
create observational correlation; and a proxy can rise while user value falls. A flag and holdout
help delivery, but they do not make any of those explanations disappear automatically.

</details>

## Scenario judgment

Lantern Notes reports 8% treatment conversion versus 7% control after two days. The analyst checked
each morning, tried conversion by device, country, and editor version, and found one device slice
with `p < .05`. The treatment arm is 54% of users. The product lead asks for a launch announcement.

<details>
<summary>Reasoned answer</summary>

Do not announce or ship from this evidence. First, the 54/46 allocation needs an SRM check; a failed
check aborts analysis. The repeated looks inflate false positives unless a valid sequential method
was precommitted. The many slices create a multiple-comparisons family, and the selected green slice
is exploratory until independently confirmed. Check denominators, exposure, seasonality, retention,
and guardrails; then either finish the original valid plan or write a new plan whose primary question
and correction are explicit.

</details>

## Design exercise

Write a one-page experiment brief for a fictional “suggest a title” editor improvement.

1. Write a tracking plan for view, suggestion shown, suggestion accepted, save, and latency/error
   events. State the idempotency key, allowed properties, owner, and privacy exclusions.
2. Define a funnel, a week-based retention cohort, and one segment whose question is justified in
   advance. Include each numerator and denominator.
3. State one north-star metric, OEC, two guardrails, null/alternative, allocation unit, MDE, alpha,
   power, sample estimate, and stopping rule.
4. Specify persistent flag assignment, ramp behavior, a holdout, full-cycle duration, SRM gate, and
   a policy for planned multiple metrics.
5. Draft the decision memo template with effect, interval, p-value or framework-equivalent evidence,
   guardrails, integrity checks, and a reversible next action.

Review it against the capstone acceptance criteria. A reviewer should be able to tell what counts
once, what population the claim applies to, and what result would block a rollout.

## Code kata

Copy `learning/capstone/code/honest_experiment.py` and add a fully type-annotated
`segment_conversion` function that accepts a sequence of `TrackingEvent` values and a platform. It
must return an additive numerator and denominator, reject an empty denominator, and never log or
accept personal data. Add a synthetic Android fixture and assertions that its counts reconcile to the
unsegmented aggregate. Do not add dependencies, network I/O, a production database, or a live flag.

## Automaticity checklist

- [ ] I can write a tracking plan and choose a stable idempotency key for a business action.
- [ ] I can compute a distinct-user funnel, original-cohort retention, and weighted segment comparison.
- [ ] I can distinguish a north-star metric, OEC, guardrail, proxy, and ratio metric.
- [ ] I can pre-commit a hypothesis, allocation, MDE, sample size, power, duration, and stopping rule.
- [ ] I can explain why randomized, persistent, treatment-independent assignment is required for a causal claim.
- [ ] I can report effect size with an interval and avoid treating a p-value as a posterior probability.
- [ ] I can stop an analysis for SRM, protect a metric family from multiplicity, and keep CUPED covariates pre-treatment.
- [ ] I can recognize peeking, Simpson's paradox, novelty, seasonality, survivorship, confounding, and Goodhart pressure.
- [ ] I can use a feature flag, ramp, and holdout as one controlled-delivery mechanism.
- [ ] I can write a decision memo whose figures reconcile to reproducible analysis output.
