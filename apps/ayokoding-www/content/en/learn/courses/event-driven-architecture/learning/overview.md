---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## How to use these examples

Every example has the same five parts: a focused explanation, a short runnable Python fragment,
a key takeaway, and a production reason. The complete, type-annotated in-process implementations
are under [`learning/code/`](./code/example.py), with tests beside them. Run them with
`python3 example.py` and `python3 -m unittest -v test_example.py` from that directory.

The snippets intentionally model broker behavior in memory. They are not deployment recipes; they
make ordering, replay, acknowledgement, deduplication, and compensation observable without hiding
the invariant behind a vendor client.

## Concepts

The course follows these concept families in dependency order:

1. **Facts and routing** (`co-01` to `co-14`): events versus commands and queries, pub/sub,
   queue delivery, notification versus state transfer, topics, partitions, consumer groups, and
   retention.
2. **Delivery and state** (`co-15` to `co-23`): delivery guarantees, idempotency, event sourcing,
   replay, snapshots, CQRS, and read-model projections.
3. **Reliability and workflows** (`co-24` to `co-33`): the dual-write problem, outbox, saga,
   compensation, DLQ, eventual consistency, schema evolution, and the cases where EDA is not a
   simplification.

### Concept reference

- **co-01 -- event definition**: an immutable statement of a completed fact, named in past tense.
- **co-02 -- event, command, and query**: a fact differs from a rejectable request and a read-only
  request for data.
- **co-03 -- event notification**: a thin event identifies a changed resource for an optional callback.
- **co-04 -- event-carried state transfer**: an event carries the changed data for an independent replica.
- **co-05 -- pub/sub**: a publisher broadcasts one event to every independent subscription.
- **co-06 -- point-to-point queue**: competing consumers share work and one consumer receives one message.
- **co-07 -- broker topology**: processors publish the next fact without one central workflow controller.
- **co-08 -- mediator topology**: one component coordinates a multi-step flow through commands or events.
- **co-09 -- log versus queue broker**: a retained log supports replay; an acknowledged queue removes work.
- **co-10 -- topic, partition, and offset**: a partition is an ordered shard; an offset is a consumer position.
- **co-11 -- partition ordering**: order is guaranteed within one partition, never across all partitions.
- **co-12 -- partition by key**: one aggregate key maps its transitions to one partition and local order.
- **co-13 -- consumer group**: members share partitions, while different groups independently receive records.
- **co-14 -- retention**: record lifetime follows a policy, not one consumer’s acknowledgement.
- **co-15 -- at-most-once**: delivery may be lost but is never retried.
- **co-16 -- at-least-once**: delivery is retried after missing acknowledgement and may duplicate.
- **co-17 -- exactly-once**: practical once-only effects combine transactional boundaries with idempotency.
- **co-18 -- idempotent consumer**: a processed message id makes a redelivery a no-op.
- **co-19 -- event sourcing**: state is represented by an append-only sequence of domain events.
- **co-20 -- event replay**: fold the stream from the start to reconstruct a current state.
- **co-21 -- snapshot**: store state at one stream position, then replay only the later tail.
- **co-22 -- CQRS**: separate the write model that makes decisions from the read model that answers queries.
- **co-23 -- read-model projection**: derive a denormalized query view by handling the event stream.
- **co-24 -- dual-write problem**: a database write and broker publish cannot be assumed atomic.
- **co-25 -- outbox pattern**: persist an unpublished event with local state, then relay it reliably.
- **co-26 -- saga**: a distributed workflow of local transactions with explicit failure handling.
- **co-27 -- choreography versus orchestration**: participants react to facts, or a coordinator directs steps.
- **co-28 -- compensating action**: reverse the completed business effects of a failed workflow in reverse order.
- **co-29 -- dead-letter queue**: route rejected or poison messages aside for inspection and controlled replay.
- **co-30 -- poison-message retry**: use bounded, delayed retry before terminal dead-lettering.
- **co-31 -- eventual consistency**: a projection can temporarily lag its write model and then converge.
- **co-32 -- schema evolution**: compatible versioned payloads let producers and consumers deploy independently.
- **co-33 -- when not EDA**: prefer direct synchronous CRUD when events add no independent-consumer benefit.

## Examples by Level

### Beginner (Examples 1–28)

- [Example 1: Event as Fact](./beginner.md#example-1-event-as-fact)
- [Example 2: Event vs Command](./beginner.md#example-2-event-vs-command)
- [Example 3: Event vs Query](./beginner.md#example-3-event-vs-query)
- [Example 4: Passive-Aggressive Command](./beginner.md#example-4-passive-aggressive-command)
- [Example 5: Pub/Sub Basic](./beginner.md#example-5-pubsub-basic)
- [Example 6: Pub/Sub Decoupling](./beginner.md#example-6-pubsub-decoupling)
- [Example 7: Point-to-Point Queue](./beginner.md#example-7-point-to-point-queue)
- [Example 8: Competing Consumers](./beginner.md#example-8-competing-consumers)
- [Example 9: Queue vs Pub/Sub](./beginner.md#example-9-queue-vs-pubsub)
- [Example 10: Event Notification](./beginner.md#example-10-event-notification)
- [Example 11: Event Notification Callback](./beginner.md#example-11-event-notification-callback)
- [Example 12: Event-Carried State](./beginner.md#example-12-event-carried-state)
- [Example 13: Local Replica](./beginner.md#example-13-local-replica)
- [Example 14: Notification vs State Transfer](./beginner.md#example-14-notification-vs-state-transfer)
- [Example 15: In-Process Event Bus](./beginner.md#example-15-in-process-event-bus)
- [Example 16: Handler Registration](./beginner.md#example-16-handler-registration)
- [Example 17: Event Payload Schema](./beginner.md#example-17-event-payload-schema)
- [Example 18: Event Immutability](./beginner.md#example-18-event-immutability)
- [Example 19: Multiple Handlers](./beginner.md#example-19-multiple-handlers)
- [Example 20: Handler Failure Isolation](./beginner.md#example-20-handler-failure-isolation)
- [Example 21: At-Most-Once](./beginner.md#example-21-at-most-once)
- [Example 22: At-Least-Once](./beginner.md#example-22-at-least-once)
- [Example 23: Duplicate Delivery Demo](./beginner.md#example-23-duplicate-delivery-demo)
- [Example 24: Idempotent Consumer](./beginner.md#example-24-idempotent-consumer)
- [Example 25: Idempotent Upsert](./beginner.md#example-25-idempotent-upsert)
- [Example 26: Idempotency Key](./beginner.md#example-26-idempotency-key)
- [Example 27: Dead-Letter Basic](./beginner.md#example-27-dead-letter-basic)
- [Example 28: Poison Retry Limit](./beginner.md#example-28-poison-retry-limit)

### Intermediate (Examples 29–56)

- [Example 29: Event Store Append](./intermediate.md#example-29-event-store-append)
- [Example 30: Event-Sourced Aggregate](./intermediate.md#example-30-event-sourced-aggregate)
- [Example 31: Rebuild by Replay](./intermediate.md#example-31-rebuild-by-replay)
- [Example 32: Replay Determinism](./intermediate.md#example-32-replay-determinism)
- [Example 33: Snapshot](./intermediate.md#example-33-snapshot)
- [Example 34: Snapshot Plus Tail](./intermediate.md#example-34-snapshot-plus-tail)
- [Example 35: Append-Only No Overwrite](./intermediate.md#example-35-append-only-no-overwrite)
- [Example 36: Event Versioning](./intermediate.md#example-36-event-versioning)
- [Example 37: Schema Backward Compatibility](./intermediate.md#example-37-schema-backward-compatibility)
- [Example 38: Schema Forward Compatibility](./intermediate.md#example-38-schema-forward-compatibility)
- [Example 39: CQRS Write Model](./intermediate.md#example-39-cqrs-write-model)
- [Example 40: CQRS Read Model](./intermediate.md#example-40-cqrs-read-model)
- [Example 41: Read-Model Projection](./intermediate.md#example-41-read-model-projection)
- [Example 42: Read-Model Rebuild](./intermediate.md#example-42-read-model-rebuild)
- [Example 43: Read-Model Lag](./intermediate.md#example-43-read-model-lag)
- [Example 44: Eventual Consistency Window](./intermediate.md#example-44-eventual-consistency-window)
- [Example 45: Topic Partition](./intermediate.md#example-45-topic-partition)
- [Example 46: Partition Ordering](./intermediate.md#example-46-partition-ordering)
- [Example 47: Cross-Partition No Order](./intermediate.md#example-47-cross-partition-no-order)
- [Example 48: Partition by Key Locality](./intermediate.md#example-48-partition-by-key-locality)
- [Example 49: Consumer Group Queue](./intermediate.md#example-49-consumer-group-queue)
- [Example 50: Consumer Group Pub/Sub](./intermediate.md#example-50-consumer-group-pubsub)
- [Example 51: Offset Commit](./intermediate.md#example-51-offset-commit)
- [Example 52: Offset Rewind Replay](./intermediate.md#example-52-offset-rewind-replay)
- [Example 53: Retention Not Delete on Consume](./intermediate.md#example-53-retention-not-delete-on-consume)
- [Example 54: Log vs Queue Broker](./intermediate.md#example-54-log-vs-queue-broker)
- [Example 55: Exchange Binding](./intermediate.md#example-55-exchange-binding)
- [Example 56: Ack and Nack](./intermediate.md#example-56-ack-and-nack)

### Advanced (Examples 57–80)

- [Example 57: Dual-Write Problem](./advanced.md#example-57-dual-write-problem)
- [Example 58: Dual-Write Lost Event](./advanced.md#example-58-dual-write-lost-event)
- [Example 59: Outbox Write](./advanced.md#example-59-outbox-write)
- [Example 60: Outbox Relay](./advanced.md#example-60-outbox-relay)
- [Example 61: Outbox Crash Safe](./advanced.md#example-61-outbox-crash-safe)
- [Example 62: Outbox Idempotent Relay](./advanced.md#example-62-outbox-idempotent-relay)
- [Example 63: Saga Choreography](./advanced.md#example-63-saga-choreography)
- [Example 64: Saga Orchestration](./advanced.md#example-64-saga-orchestration)
- [Example 65: Saga Compensation](./advanced.md#example-65-saga-compensation)
- [Example 66: Saga Compensation Order](./advanced.md#example-66-saga-compensation-order)
- [Example 67: Saga Partial Failure](./advanced.md#example-67-saga-partial-failure)
- [Example 68: Mediator Topology](./advanced.md#example-68-mediator-topology)
- [Example 69: Broker Topology](./advanced.md#example-69-broker-topology)
- [Example 70: Broker vs Mediator](./advanced.md#example-70-broker-vs-mediator)
- [Example 71: DLQ Poison](./advanced.md#example-71-dlq-poison)
- [Example 72: DLQ Inspect Replay](./advanced.md#example-72-dlq-inspect-replay)
- [Example 73: Exactly-Once Illusion](./advanced.md#example-73-exactly-once-illusion)
- [Example 74: Transactional Producer](./advanced.md#example-74-transactional-producer)
- [Example 75: State-Transfer Rebuild](./advanced.md#example-75-state-transfer-rebuild)
- [Example 76: Ordering with Key](./advanced.md#example-76-ordering-with-key)
- [Example 77: Retry with Backoff](./advanced.md#example-77-retry-with-backoff)
- [Example 78: Event-Sourcing Audit](./advanced.md#example-78-event-sourcing-audit)
- [Example 79: When Not to Use EDA](./advanced.md#example-79-when-not-to-use-eda)
- [Example 80: EDA Slice](./advanced.md#example-80-eda-slice)

## Verification contract

The prose pages cite every settled `ex-01` through `ex-80` item from the syllabus. The companion
implementation proves the core invariants: deterministic replay, an independently rebuilt read
model, outbox recovery, idempotent redelivery, reverse-order compensation, and DLQ routing for a
poison message. Run the supplied test command before adapting any fragment.

Next: [Beginner Examples](./beginner.md) →
