---
title: "Learning overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Work through the 52 scenarios in order. Each is a compact decision or mechanism for fictional
Harbor Checkout. The examples are grouped by the question they answer, rather than by tool:

- **Telemetry and service signals** (ex-01 through ex-18) establishes what a user experiences and
  how metrics, logs, and traces provide evidence.
- **Objectives, budgets, and alerting** (ex-19 through ex-36) turns evidence into an SLI, SLO, error
  budget, safe delivery decision, and proportionate alert.
- **Operations, learning, and capacity** (ex-37 through ex-51) completes the operating loop with
  dashboards, incident command, postmortems, toil reduction, and a capacity limit.
- **Capstone** (ex-52) connects all of the pieces in one safe local simulation.

The selected Python material is fully type annotated and dependency-free. It is intentionally small:
do not mistake a teaching script for a production telemetry library. Production instrumentation must
be reviewed for cardinality, sensitive-data handling, cost, retention, and failure behavior.

## A reliable decision sequence

1. Start with a user journey and a measurable good-event definition.
2. Set an SLO with stakeholders, a window, and an error-budget policy.
3. Instrument the golden signals plus enough logs and traces to investigate an observed symptom.
4. Page only when people need prompt action to protect users or the budget; route the rest as tickets.
5. During an incident, coordinate impact, mitigation, communication, and evidence.
6. Learn from system conditions, then remove or automate recurring toil with an owner and rollback.

Every scenario names the concepts it exercises. The scenario tables are deliberately structured so a
reviewer can tell what decision was made, what evidence supports it, and what would prove it wrong.
