---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 1
---

Use this page after finishing the three learning tiers. Answer from memory before opening a linked
example; the goal is to retrieve the invariant, not to recognize familiar vocabulary.

## Recall Q&A

**Q1 (`co-01`).** Why must an event be named in the past tense?

<details>
<summary>Answer</summary>

It states an immutable business fact that already happened. `OrderPlaced` lets any consumer decide
whether and how to react; `PlaceOrder` is a command that needs one accountable handler.

</details>

**Q2 (`co-05`, `co-06`).** What is the delivery-count difference between pub/sub and a work queue?

<details>
<summary>Answer</summary>

Pub/sub sends one fact to every independent subscriber. A queue sends each message to one competing
consumer, which scales one unit of work without duplicating its side effect.

</details>

**Q3 (`co-16`, `co-18`).** Why is duplicate delivery a normal condition?

<details>
<summary>Answer</summary>

After a handler effect succeeds, a process can fail before acknowledgement. Redelivery avoids a lost
message; a durable processed-message identity makes its second effect a no-op.

</details>

**Q4 (`co-19` to `co-23`).** What must match after rebuilding a projection?

<details>
<summary>Answer</summary>

An empty projection replaying the retained stream must equal an incrementally maintained projection.
That comparison proves reducers are deterministic and derived state is recoverable.

</details>

**Q5 (`co-24`, `co-25`).** What hole does an outbox close?

<details>
<summary>Answer</summary>

It closes the gap where a database commit succeeds but a separate broker publish never happens. The
state change and pending event commit together; a relay retries the durable pending row.

</details>

**Q6 (`co-26`, `co-28`).** Why is compensation not rollback?

<details>
<summary>Answer</summary>

Services have separate local transactions and effects may already be visible. Compensation is a new,
idempotent business action, such as releasing reserved inventory after payment failure.

</details>

**Q7 (`co-29`, `co-30`).** When should a message enter the DLQ?

<details>
<summary>Answer</summary>

After bounded retry identifies it as poison or unprocessable. The DLQ preserves it for diagnosis and
controlled replay instead of allowing an infinite retry loop or silent loss.

</details>

## Applied problems

1. A new analytics team wants every `OrderPlaced` event but ordering must not call its service. Draw
   the pub/sub subscription boundary and name the schema compatibility risk introduced by its new
   consumer.
2. A payment worker restarts after charging a provider but before acknowledging its queue message.
   State exactly where the idempotency record must live and what key it must use.
3. A user sees `placed` immediately after payment succeeded. Explain the eventual-consistency window,
   name one user experience that makes it honest, and name one metric that detects an unhealthy window.
4. A Kafka-like topic has six partitions and one order emits `placed`, `paid`, and `fulfilled`.
   Choose the partition key and explain why a random UUID per event is incorrect.
5. A producer adds `currency` to `OrderPlaced`. Describe one backward-compatible reader behavior and
   one migration you would require before removing an existing field.
6. Inventory reservation succeeded, payment failed, and fulfilment never started. List the correct
   compensation actions in order and identify which step has nothing to compensate.
7. A relay published an outbox row then crashed before marking it published. Explain why the consumer,
   rather than the relay alone, must protect the externally visible effect.

## Code katas

### Kata 1: Idempotent projection

Open [`kata.py`](./code/kata.py). Before running it, predict the two booleans and the final
projection. The function must return `True` for the first message id, return `False` for its
redelivery, and preserve exactly one `o-1: paid` effect.

```text
cd apps/ayokoding-www/content/en/learn/courses/event-driven-architecture/drilling/code
python3 kata.py
python3 -m unittest -v test_kata.py
```

### Kata 2: Outbox recovery design

Extend the capstone so `relay` can be called twice after an artificial failure. Write a test that
proves the durable event is eventually projected and that the projection still contains one effect.
Do not solve this by deleting the event before the projected effect is durable.

### Kata 3: Per-order ordering

Add a `partition_for(order_id, partition_count)` function to a scratch file. Test that all events
for one order map to one partition, while different orders may map independently. Explain why this
does not create a global ordering guarantee.

## Self-check checklist

- [ ] I can distinguish an event, command, and query by intent without relying on its transport.
- [ ] I can choose pub/sub, a queue, or independent consumer groups from desired delivery count.
- [ ] I can explain why acknowledgement after an effect permits redelivery and why idempotency is
      required anyway.
- [ ] I can rebuild a read model and identify the acceptable eventual-consistency window.
- [ ] I can explain the dual-write failure and implement an outbox relay plus idempotent consumer.
- [ ] I can choose choreography or orchestration and write reverse-order compensation for failure.
- [ ] I can route poison messages to a DLQ with bounded exponential retry and an owned replay path.
- [ ] I can explain one case where synchronous CRUD is clearer than EDA.

## Elaborative interrogation & self-explanation

1. Why does an event-carried state transfer make replay easier while making schema design harder?
2. Why is a broker transaction insufficient to make a database write and broker publish atomic?
3. Why can a “once only” broker setting not prove a payment provider was charged exactly once?
4. Why is a per-aggregate partition key a correctness boundary as well as a throughput choice?
5. Why must a DLQ be monitored even when no user sees it directly?
6. Why can an orchestrator improve observability while increasing coupling?
7. Why is a snapshot an optimization rather than a replacement for event history?
8. Why does a straightforward read-your-write CRUD operation often not benefit from an event broker?
