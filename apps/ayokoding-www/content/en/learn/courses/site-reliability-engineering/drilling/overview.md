---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Use these five sections after the learning track. All situations are fictional. For a real service,
involve its product, security, privacy, and operational owners before changing instrumentation,
objectives, alerting, or capacity.

## Recall Q&A

**Q1 (co-01 through co-06).** What is the relationship among an SLI, SLO, and error budget?

<details>
<summary>Answer</summary>

An SLI measures a defined user-facing outcome. An SLO is its target over a stated window. The error
budget is the allowed gap between perfection and that target; it informs a pre-agreed reliability
and delivery policy. An SLA is different: it is an external commitment with consequences.

</details>

**Q2 (co-08 through co-15).** Why are metrics, logs, and traces complementary?

<details>
<summary>Answer</summary>

Metrics show aggregate behavior and trends; structured logs retain event detail; traces connect work
across boundaries. One slow or failing journey can be detected in a metric, investigated with logs,
and followed through dependencies with a trace. None replaces careful event semantics.

</details>

**Q3 (co-20 through co-23).** What makes an alert worthy of a page?

<details>
<summary>Answer</summary>

It signals a user-facing symptom or dangerous, sustained budget burn, needs timely human action,
and links to a useful first response. A diagnostic condition such as high CPU with healthy users can
be a ticket or dashboard signal instead. Pages without action create alert fatigue.

</details>

**Q4 (co-24 through co-27).** What makes a postmortem blameless and useful?

<details>
<summary>Answer</summary>

It records impact, timeline, evidence, system conditions, decisions, mitigation, and owned follow-up
work. It asks how defenses and context allowed the outcome rather than identifying a person to blame.

</details>

**Q5 (co-28 through co-30).** Why can automation itself create reliability work?

<details>
<summary>Answer</summary>

Automation has inputs, dependencies, failure modes, ownership, and maintenance cost. Automate
repetitive, reversible work first, validate input, preserve a fallback, and measure whether the
manual toil actually disappeared.

</details>

## Scenario judgment

Harbor receives a CPU alert at 95%, but checkout success, latency, and budget burn are healthy. The
on-call engineer wants to page immediately “just in case.”

<details>
<summary>Reasoned answer</summary>

Do not page from CPU alone. Create or retain a diagnostic ticket with the observed saturation, time
window, capacity assumption, and owner. Review headroom and likely growth, while preserving a
separate symptom- or SLO-burn page for genuine customer impact. This avoids both complacency and
alert fatigue.

</details>

## Design exercise

For a fictional appointment-booking journey, write a one-page reliability brief:

1. Define one availability or latency SLI, including numerator, denominator, threshold, and window.
2. Choose an SLO and translate its error budget into an explicit release decision policy.
3. Name the four golden signals and identify one structured-log field plus one trace boundary needed
   to investigate a bad SLI.
4. Specify one page condition, one ticket condition, and the first three runbook actions for the page.
5. Draft a blameless postmortem action with an owner, review date, expected evidence, and a safe
   fallback if automation is involved.

Review the brief against the capstone acceptance criteria. A reader should be able to distinguish a
customer symptom from a diagnostic signal and a learning action from a personal admonition.

## Code kata

Without adding dependencies or I/O, add a fully type-annotated `classify_severity` function to a
copy of `sre_loop.py`. It should accept a percentage of affected fictional users and a duration in
minutes, validate both inputs, and return a finite enum. Then write assertions for a low-impact,
short event and a broad, long event. Do not connect it to a pager or a production system.

## Automaticity checklist

- [ ] I can define a user-facing SLI and distinguish it from an internal diagnostic metric.
- [ ] I can negotiate an SLO window and calculate the corresponding error budget.
- [ ] I can explain why availability nines imply a concrete trade-off rather than a prestige rank.
- [ ] I can use latency, traffic, errors, and saturation to orient an investigation.
- [ ] I can use logs and traces without collecting sensitive values or unbounded-cardinality labels.
- [ ] I can route an impactful, sustained burn to a page and lower-urgency evidence to a ticket.
- [ ] I can assign incident command roles and write a factual, blameless timeline.
- [ ] I can identify toil, evaluate automation's failure mode, and plan capacity before saturation harms users.
