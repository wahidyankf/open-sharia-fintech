---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Why is constructor injection preferred?**

<details><summary>Answer</summary>It makes required collaborators explicit, supports immutability,
and allows a service to be tested without a container.</details>

**What operational problem does Actuator address?**

<details><summary>Answer</summary>It exposes health and metrics so an operator can observe the
running service rather than infer behavior from an HTTP error alone.</details>

## Calculation practice

If a 200 MB heap grows to 600 MB during a load window, record allocation rate, live-set estimate,
and pause time before changing a collector. A collector name alone is not a diagnosis.

## Scenario judgment

A controller needs a database lookup and business decision. Keep the controller focused on HTTP
binding, place the decision in a constructor-injected service, and keep persistence in a repository.

## Design exercise

Design a small catalog service with a validated create request, service transaction, repository,
structured not-found response, and health endpoint. State the metric that would reveal an N+1 issue.

## Automaticity checklist

- [ ] I can explain why a bean exists and who injects it.
- [ ] I can choose a whole-context or slice test.
- [ ] I can recognize an ORM query-count symptom.
- [ ] I can name a transaction boundary.
- [ ] I can distinguish warm-up from a memory leak.

## Why / why not prompts

- Why not field injection for a required service dependency?
- Why not return a JPA entity directly from every endpoint?
- Why not enable every actuator endpoint publicly?
- Why not optimize JIT/GC before measuring a workload?
- Why can an auto-configured framework still need explicit boundaries?
