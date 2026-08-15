---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Use a timer and say answers aloud before opening a details block. These drills rehearse interview
communication; they do not replace the depth work in [System Design](../../system-design/overview.md).

## Recall Q&A

**Q1 (co-01).** What does a strong answer make reviewable besides its diagram?

<details><summary>Answer</summary>Its scope, assumptions, estimates, decision rationale, risks, and
trade-offs.</details>

**Q2 (co-02–co-03).** What do you clarify before proposing a component?

<details><summary>Answer</summary>Functional goal, success boundary, users, scale, latency,
availability, consistency, cost, and which slice fits the timebox.</details>

**Q3 (co-04).** What makes an estimate credible in an interview?

<details><summary>Answer</summary>Visible assumptions, units, simple arithmetic, and a stated
decision it informs.</details>

**Q4 (co-16).** What is the minimum complete trade-off statement?

<details><summary>Answer</summary>Choice, benefit, cost, and why the stated product need accepts
that cost.</details>

**Q5 (co-20–co-21).** How do you regain control after a deep question?

<details><summary>Answer</summary>Answer at the requested altitude, summarize its impact, and name
the next spine checkpoint.</details>

## Calculation practice

A fictional service receives 1.8 million reads per day. Estimate average QPS, then an eightfold
peak. At 2 KB per response, estimate peak payload egress.

<details><summary>Worked answer</summary>`1,800,000 / 86,400 ≈ 21` average QPS; peak is about
`168 QPS`; payload egress is roughly `336 KB/s`. Say that cache-hit rate and protocol overhead are
assumptions before using the figure to right-size the discussion.</details>

## Scenario judgment

An interviewer asks for a globally replicated write path, but the prompt only says a local team
publishes weekly schedules. What is the strong response?

<details><summary>Reasoned answer</summary>Clarify geographic and recovery requirements. State a
simple local baseline first; discuss multi-region only as a conditional trade-off. Adding it without
a requirement would hide rather than demonstrate judgment.</details>

## Design exercise

In 35 minutes, design a fictional appointment-reminder service. Write the assumptions, estimate
the peak, draw a high-level request and delivery flow, deep-dive one pressure point, name a
bottleneck, state two trade-offs, and finish with a one-minute recap.

## Automaticity checklist

- [ ] I can state a round agenda before drawing.
- [ ] I can make an estimate with assumptions and units.
- [ ] I can connect one deep dive to an interviewer question and zoom back out.
- [ ] I can name a failure mode and an observable signal.
- [ ] I can state two costs as clearly as two benefits.

## Why / why not prompts

- Why begin with requirements instead of a favored architecture?
- Why is a cache not automatically the answer to a slow read?
- Why might a simpler design be better at the stated scale?
- Why does a staff answer include rollout and ownership, not just components?
- Why should the recap name the largest unresolved risk?
