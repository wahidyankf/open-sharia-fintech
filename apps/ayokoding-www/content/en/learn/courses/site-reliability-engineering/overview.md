---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Site reliability engineering (SRE) treats reliability as an engineering and product decision. A
service will fail; the useful question is how much user-visible failure is acceptable, how it will be
measured, and what the team will change when the measurement says the target is at risk. This course
uses the fictional **Harbor Checkout** service to make that loop concrete: observe user experience,
set an objective, spend an error budget deliberately, respond to an incident, and learn from it.

This is an **Annotated-concept** course with small, fully type-annotated Python examples. They are
offline, deterministic teaching mechanisms, not a production monitoring stack. They make formulas,
alert routing, and incident decisions inspectable without credentials, network access, infrastructure
changes, or real customer data.

## Prerequisites

- [Containers and Orchestration](/en/learn/courses/containers-and-orchestration.md.md) supplies the runtime
  context in which a service exposes health and telemetry.
- [System Design](/en/learn/courses/system-design.md.md) is an explicit prerequisite: use its load,
  capacity, dependency, and failure-mode reasoning when choosing an SLI or interpreting saturation.

## The mental model

An SLI measures a user-facing outcome; an SLO is the target for that measure over a stated window;
the error budget is the allowed distance between perfection and that target. The budget makes the
reliability-versus-change trade visible. Metrics, structured logs, and traces supply complementary
evidence. Alerts should page on a user-facing symptom or dangerous budget burn, while diagnostic
signals help investigation without waking someone unnecessarily. An incident is then a coordinated
response to impact, followed by a blameless explanation of system conditions and owned improvements.

## Scope boundary

This course teaches service-level reliability decisions and small local mechanisms. It does not
replace production architecture, a Kubernetes operations course, a vendor dashboard tutorial, or an
SLA negotiated with counsel. It also does not promise that an SLO prevents incidents: an objective is
an agreement for detecting and managing risk, not a guarantee. Never paste production credentials,
customer records, tokens, or incident-sensitive logs into the examples.

## How verification works

Each worked scenario ends in a visible test: a ratio, an alert-routing decision, a role assignment,
or an artifact field a reviewer can inspect. The capstone Python program uses only the standard
library, fixed synthetic events, and explicit assertions. It intentionally simulates an incident;
it does not send a page, call an API, start a server, or modify a system.

## Concept register

- **co-01 · reliability-as-feature** — reliability is negotiated and budgeted, not a claim of 100%.
- **co-02 · SLI** and **co-03 · SLO** — a user-facing indicator and its target.
- **co-04 · SLA**, **co-05 · error-budget**, **co-06 · budget-velocity-tradeoff**, and **co-07 · nines**.
- **co-08 through co-11 · golden signals** — latency, traffic, errors, and saturation.
- **co-12 through co-19 · observability** — metrics, logs, traces, observability, instrumentation,
  OpenTelemetry, Prometheus scraping, and dashboards.
- **co-20 through co-23 · alerting and on-call** — symptom-based alerting, burn alerts, fatigue, and
  page-versus-ticket judgment.
- **co-24 through co-27 · incident learning** — severity, command, blameless postmortems, and action items.
- **co-28 through co-30 · sustainable operations** — toil, safe automation, and capacity planning.

## Primary-source reading

- [Google SRE Book: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
  — SLIs, SLOs, error budgets, and availability targets.
- [Google SRE Book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
  — the four golden signals and monitoring intent.
- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
  — symptom-oriented and burn-rate alerting.
- [Google SRE Book: Eliminating Toil](https://sre.google/sre-book/eliminating-toil/) — a practical
  definition of toil and the case for removing it.
- [Google SRE Book: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) and
  [Managing Incidents](https://sre.google/sre-book/managing-incidents/) — learning culture and roles.
- [OpenTelemetry documentation](https://opentelemetry.io/docs/) and
  [Prometheus documentation](https://prometheus.io/docs/introduction/overview/) — interoperable
  telemetry and pull-based metrics collection.
