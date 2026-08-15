---
title: "Capstone overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Complete a safe, local SRE loop for fictional Harbor Checkout: turn synthetic request events into
golden-signal summaries, calculate a user-facing availability SLI and error-budget burn, route a
symptom-based alert, then document the simulated incident without blame. The goal is an inspectable
operating decision, not a production monitoring deployment.

## Build order

1. Read and run [`sre_loop.py`](./code/sre_loop.py) from this directory with `python3 code/sre_loop.py`.
   It uses only the Python standard library, fixed in-memory events, and assertions. It makes no
   network calls and writes no files.
2. Change only the synthetic fixtures if you want to explore another outcome. Keep every
   `RequestEvent` fully typed; do not add secrets, personal data, production endpoints, or live load.
3. Explain the returned `PAGE` route in terms of user-visible errors and budget burn, not CPU alone.
4. Review the [postmortem](./postmortem.md), then write a comparable artifact for the changed fixture.
   Preserve the time-ordered facts, system conditions, mitigation, and owned action items.

## Concepts exercised

- [x] user-facing SLI, SLO, and error budget (co-02, co-03, co-05)
- [x] latency, traffic, errors, and saturation (co-08 through co-11)
- [x] instrumentation and a bounded metric summary (co-12, co-16, co-19)
- [x] symptom-based alerting, burn rate, and on-call routing (co-20, co-21, co-23)
- [x] severity, incident command, blameless postmortem, and action items (co-24 through co-27)
- [x] capacity and safe automation follow-up (co-29, co-30)

## Acceptance criteria

- The program computes the good-event ratio from a stated synthetic denominator and returns a
  remaining-budget value between 0 and 1.
- Its alert route pages only for the seeded user-impact fixture; the healthy fixture remains silent.
- The four golden signals appear in its immutable `SignalSummary` output.
- The postmortem identifies impact, timeline, conditions, mitigation, and concrete owned actions
  without attributing the incident to an individual.
- The learner can explain a capacity follow-up that is warranted even if it was not the page trigger.

## Done bar

A reviewer can run the script offline, trace the calculation from request event to alert route, and
read an incident artifact that improves the system rather than assigning personal fault. The learner
can also say what would be needed before a real production deployment: reviewed instrumentation,
privacy and cardinality controls, service-specific windows, ownership, runbooks, and tested failure
handling.

← Previous: [Operations, learning, and capacity](../operations-learning-and-capacity.md) · Next:
[Drilling](../../drilling/overview.md) →
