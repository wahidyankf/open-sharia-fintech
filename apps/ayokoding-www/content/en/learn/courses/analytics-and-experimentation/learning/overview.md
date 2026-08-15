---
title: "Learning overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Work through 78 compact examples in order. Each example names its concepts, decision artifact, and
verification. They use the same fictional Lantern Notes product so the numbers remain connected:
an event schema affects a funnel; a funnel informs an OEC; an OEC is protected by guardrails; and a
ship decision is invalid if allocation or stopping was dishonest.

- **Instrumentation and product measures** (ex-01 through ex-26) makes event collection, product
  measures, funnels, cohorts, segmentation, and metric choices inspectable.
- **Experiment design and analysis** (ex-27 through ex-54) turns a product hypothesis into persistent
  allocation, power, effect estimates, integrity checks, and a disciplined comparison.
- **Honest reads and safe delivery** (ex-55 through ex-78) models the traps that make a result look
  better than it is, then connects a flag, ramp, holdout, and decision memo.
- **Capstone** combines the sequence in one safe local program and one reconciled written artifact.

The selected Python is standard-library-only and fully type-annotated. A real production analysis
would add privacy review, ownership, data retention, query review, and an approved statistics stack;
it would not copy a short teaching calculation unreviewed.

## Reading a worked example

Each table is intentionally a design review in miniature. The **artifact** is what a team writes or
computes; **verify** is the smallest falsifiable check; **concepts** provides a route back to the
register. Do the verification before accepting the interpretation. A statistically detectable
number is not automatically a product decision, and an appealing product story is not evidence.

← Previous: [Course overview](../overview) · Next:
[Instrumentation and product measures](./instrumentation-and-product-measures) →
