---
title: "Learning Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

The system-design interview rewards a reviewable design conversation rather than a memorized
component list. These 22 concepts are the rubric; the following pages apply them to constructed
prompts. The architecture depth belongs in [System Design](../../system-design/overview.md).

## Concepts

### co-01 · what-the-round-scores

Score structured reasoning, breadth, targeted depth, communication, and defensible trade-offs—not
a single canonical diagram.

### co-02 · requirements-clarification

Separate functional needs from scale, latency, availability, consistency, and cost constraints.

### co-03 · scope-negotiation

Turn an open prompt into a stated core that fits the timebox before drawing components.

### co-04 · back-of-envelope-estimation

Use explicit assumptions and units to make an order-of-magnitude estimate decision-useful.

### co-05 · high-level-design-first

Show major responsibilities and request flow before choosing a component's internals.

### co-06 · api-contract-sketch

Sketch the key operations and map each to a functional requirement.

### co-07 · data-model-and-storage-choice

State entities, access patterns, and why a storage choice follows from those patterns.

### co-08 · scaling-the-web-tier

Explain how stateless request handling can add capacity without moving session state into a server.

### co-09 · load-balancing

Name the balancing decision, health signal, and traffic shape it serves.

### co-10 · caching-strategy

Choose cache placement and explain freshness, invalidation, and miss behavior.

### co-11 · database-scaling

Connect read replicas or partitions to the named read/write pressure and their costs.

### co-12 · consistency-vs-availability

Choose consistency behavior from product harm, rather than treating a distributed-systems slogan as
an answer.

### co-13 · asynchronous-processing

Use durable handoff and idempotent work when a slow operation should leave the request path.

### co-14 · rate-limiting-and-backpressure

Protect a bounded resource and state what the client or caller sees under pressure.

### co-15 · bottleneck-identification

Name the first likely limit, its evidence, and the next measurement or mitigation.

### co-16 · trade-off-articulation

For each consequential choice, say what it buys and what it costs.

### co-17 · reliability-and-failure-modes

Walk failure behavior, timeouts, retries, idempotency, and recovery rather than assuming success.

### co-18 · observability-in-design

Tie metrics, logs, traces, and alerts to a question or failure mode.

### co-19 · non-functional-drivers

Let latency, throughput, availability, durability, and cost alter the proposed scope or design.

### co-20 · altitude-control

Move from the whole-system view to one useful deep dive and back when the interviewer signals it.

### co-21 · driving-the-conversation

State an agenda and checkpoints; do not wait passively for every next question.

### co-22 · senior-vs-staff-expectations

At senior and staff altitude, own ambiguity and cross-cutting concerns such as migration, cost,
security, and team ownership.

Each worked scenario has a standalone artifact in [artifacts](./artifacts/), with a prompt,
observable check, and the concept labels it exercises.
