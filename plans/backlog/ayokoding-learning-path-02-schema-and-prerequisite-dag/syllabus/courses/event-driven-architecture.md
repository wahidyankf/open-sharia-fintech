# Event-Driven Architecture (By Example, Python)

**Course ID**: `event-driven-architecture` · **Format**: By Example · **Language**: Python.

**Short summary**: Events, message brokers, event-driven design

**Scope note**: designing around events — pub/sub, event sourcing, CQRS, the outbox pattern, dead-letter
queues, idempotent consumers, and sagas for distributed workflows — as runnable Python. The event-driven
_style_ is catalogued in [`42-software-architecture`](./software-architecture.md); domain events come
from [`43-domain-driven-design`](./domain-driven-design.md); the messaging basics from
[`39-backend-at-scale`](./backend-at-scale.md).

## Why this exists · the big idea

- **The problem before the solution**: when services call each other synchronously, one slow or down
  dependency stalls the whole chain, and every caller is bound to the callee's availability and shape.
- **Keep-this-if-you-forget-everything**: turn state changes into events others react to — this decouples
  producers from consumers in time and space, but you trade immediate consistency and simple debugging for
  eventual consistency and at-least-once delivery you must design around.
- **Big ideas touched**: `coupling-vs-cohesion` (events decouple producer from consumer), `taming-state`
  (event sourcing makes the append-only log the source of truth), `consistency-latency-throughput`
  (you buy availability and throughput with eventual consistency).

## Prerequisites

- **Prior topics**: [topic 24 Concurrency & Parallelism](./concurrency-and-parallelism.md) (async
  processing, ordering), [topic 39 Backend at Scale](./backend-at-scale.md) (queues, idempotent
  consumers), and [topic 43 Domain-Driven Design](./domain-driven-design.md) (domain events).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with a pinned CVE-clean broker client;
  a local broker or stream (Valkey/Redis Streams or an in-process bus is fine); a SQL DB for the outbox.
- **Assumed knowledge**: what a message queue is + why idempotency matters (topic 39); domain events
  (topic 43); async processing (topic 24).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: pattern terminology (event sourcing, CQRS, outbox pattern, choreography-vs-
  orchestration sagas, DLQ, idempotent consumers, at-least-once delivery) is stable and matches current
  industry usage (Microsoft Cloud Design Patterns catalog, Confluent event-driven guides). No corrections.
- 2026-07-12 — verified: the "Valkey/Redis Streams or an in-process bus" hedge is itself accurate —
  Valkey is the Linux Foundation community fork after Redis's 2024 relicensing (SSPL/RSALv2); keep the
  hedge (aligns with DD-21 Tier-1-OSS default).

> DD-35 primary-source pass (2026-07-12). Pattern definitions traced to Fowler's articles, Chris
> Richardson's microservices.io, Apache Kafka + RabbitMQ + Confluent docs (all fetched/read). Two
> attribution caveats flagged below to avoid over-crediting a single source.

- **Fowler's four EDA patterns** (all from [Fowler, "What do you mean by 'Event-Driven'?"](https://martinfowler.com/articles/201701-event-driven.html), Jan 2017) — **Event Notification**: "a system sends event
  messages to notify other systems of a change in its domain … the source system doesn't really care much
  about the response," and "an event need not carry much data … often just some id information and a link
  back to the sender." **Event-Carried State Transfer**: "update clients of a system in such a way that they
  don't need to contact the source system … A recipient can then update its own copy of [the] data";
  downside "there's lots of data schlepped around and lots of copies." Plus Event Sourcing and CQRS (below).
- **Event vs command vs query** — Fowler warns of "an event … used as a passive-aggressive command … the
  source system expects the recipient to carry out an action, and ought to use a command message." The
  sharper trichotomy (event = immutable fact / command = rejectable request / query = data request) is
  broader DDD/CQRS community usage (Greg Young lineage), **not** verbatim in Fowler's article —
  `[Needs Verification]` as a single-source quote; attribute to the community, not solely to Fowler.
- **Event Sourcing** — "Capture all changes to an application state as a sequence of events"; "we can
  discard the application state completely and rebuild it by re-running the events from the event log."
  Audit benefit: "we now have a log of all the changes." Source: [Fowler, EventSourcing](https://martinfowler.com/eaaDev/EventSourcing.html) (2005, fetched).
- **CQRS** — "you can use a different model to update information than the model you use to read
  information"; independent from event sourcing ("balanced against the additional complexity of having
  separate models"). Source: [Fowler, CQRS](https://martinfowler.com/bliki/CQRS.html) (2011, fetched).
- **Broker vs mediator topology** — Mediator: "useful for events that have multiple steps and require some
  level of orchestration"; the mediator "orchestrates that event by sending additional asynchronous events."
  Broker: "no central event mediator; the message flow is distributed across the event processor components
  in a chain-like fashion." Source: [Mark Richards, Software Architecture Patterns — EDA](https://www.oreilly.com/content/software-architecture-patterns/) (O'Reilly Radar, 2015).
- **Pub/sub vs point-to-point** — fanout "broadcasts all the messages it receives to all the queues";
  work-queue "will send each message to the next consumer, in sequence … called round-robin." Source:
  [RabbitMQ Tutorials 2 & 3](https://www.rabbitmq.com/tutorials/tutorial-three-python) (fetched).
- **Log broker vs queue broker** — RabbitMQ: a positive ack means the message "can be discarded"
  (delete-on-ack); Kafka: "Log data is discarded after a fixed period of time or when the log reaches some
  predetermined size" and a consumer can "deliberately rewind back to an old offset and re-consume data."
  Sources: [RabbitMQ — Confirms](https://www.rabbitmq.com/docs/confirms); [Apache Kafka design docs](https://github.com/apache/kafka-site/blob/markdown/content/en/43/design/design.md) (fetched via the site's own markdown source; kafka.apache.org is JS-rendered).
- **Kafka topics/partitions/offsets/ordering** — "Topics are partitioned … spread over a number of
  'buckets' … on different Kafka brokers"; "Kafka guarantees that any consumer of a given topic-partition
  will always read that partition's events in exactly the same order as they were written" (**ordering only
  within a partition**); "if the key chosen was a user id then all data for a given user would be sent to
  the same partition." Source: [Kafka 4.3 intro/design docs](https://github.com/apache/kafka-site/blob/markdown/content/en/43/getting-started/introduction.md). Caveat: the classic "consumer groups = queue
  (same group) / pub-sub (different groups)" paragraph was **removed** from current v4.3 docs — treat as
  accepted domain knowledge, `[Needs Verification]` as a live-doc quote.
- **Delivery guarantees** — at-most-once: "messages may be lost … not redelivered"; at-least-once:
  "never lost, but they may be delivered more than once"; exactly-once: "delivered once and only once,"
  via idempotent/transactional producers (Kafka ≥ 0.11.0.0). "By default Kafka guarantees at-least-once
  delivery." Source: [Confluent — Message Delivery Guarantees](https://docs.confluent.io/kafka/design/delivery-semantics.html) (fetched).
- **Idempotent consumer** — "Make a consumer idempotent by having it record the IDs of processed messages
  in the database"; a `PROCESSED_MESSAGES` table keyed on `(subscriberId, messageID)`. Source: [microservices.io — Idempotent Consumer](https://microservices.io/patterns/communication-style/idempotent-consumer.html) (Richardson, fetched).
- **Saga** — "a sequence of local transactions … Each local transaction updates the database and publishes
  a message/event to trigger the next"; on failure "executes a series of compensating transactions that undo
  the changes." Choreography ("each local transaction publishes domain events that trigger local
  transactions in other services") vs orchestration ("an orchestrator tells the participants what local
  transactions to execute"). Source: [microservices.io — Saga](https://microservices.io/patterns/data/saga.html) (Richardson, fetched); pattern originates with Garcia-Molina & Salem (1987).
- **Transactional outbox / dual-write** — "How to atomically update the database and send messages … 2PC is
  not an option"; solution: "store the message in the database as part of the transaction … A separate
  process then sends the messages," so "messages are guaranteed to be sent if and only if the database
  transaction commits." The label "dual-write problem" is community usage, `[Needs Verification]` as
  Richardson's own term. Source: [microservices.io — Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html) (fetched).
- **Schema evolution** — Schema Registry is "a centralized repository for managing and validating schemas";
  **backward** compat = "consumers using the new schema can read data produced with the last schema";
  **forward** compat = "data produced with a new schema can be read by consumers using the last schema."
  Source: [Confluent Schema Registry — Schema Evolution](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html) (fetched).
- **Dead-letter queue** — messages are dead-lettered when negatively acknowledged with `requeue=false`,
  expired by TTL, dropped by a length limit, or (quorum queues) returned past the `delivery-limit`. Source:
  [RabbitMQ — Dead Letter Exchanges](https://www.rabbitmq.com/docs/dlx) (fetched).
- **Eventual consistency** — nodes "process updates independently … having temporarily inconsistent
  versions … they should converge toward the same state"; the read-your-writes hazard: "your update was
  received by the pink node, but your get request was handled by the green node." Sources: [Kleppmann, "Convergence" (CACM 2022)](https://martin.kleppmann.com/2022/11/01/convergence-cacm.html); [Fowler, Microservice Trade-Offs](https://martinfowler.com/articles/microservice-trade-offs.html) (2015).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · event-definition** — an event is an immutable statement of a fact that already happened, named in the past tense.
- **co-02 · event-vs-command-vs-query** — a fact (event) differs from a request-to-do (command, rejectable) and a request-for-data (query).
- **co-03 · event-notification** — a thin event notifies of a change; the receiver calls back to the source for details (Fowler).
- **co-04 · event-carried-state-transfer** — the event carries the changed data so the receiver keeps its own local replica (Fowler).
- **co-05 · pub-sub** — a publisher broadcasts to many independent subscribers (fanout); the publisher is unaware of them.
- **co-06 · point-to-point-queue** — competing consumers share a queue round-robin; each message goes to exactly one.
- **co-07 · broker-topology** — no central mediator; a chain of processors each emits the next event (Richards).
- **co-08 · mediator-topology** — a central mediator orchestrates a multi-step event flow (Richards).
- **co-09 · log-vs-queue-broker** — a log broker (Kafka) keeps messages for replay; a queue broker (RabbitMQ) deletes on ack.
- **co-10 · topic-partition-offset** — a Kafka topic is split into partitions; each consumer tracks an integer offset.
- **co-11 · partition-ordering** — ordering is guaranteed only within a partition, never across partitions.
- **co-12 · partition-by-key** — a partition key routes an entity's events to one partition, giving per-key order and locality.
- **co-13 · consumer-group** — consumers in the same group share partitions (queue semantics); different groups each get all messages (pub/sub).
- **co-14 · retention** — the log is discarded by time/size, not on consume; a consumer replays by rewinding its offset.
- **co-15 · at-most-once** — fire-and-forget: a message may be lost, never duplicated.
- **co-16 · at-least-once** — the default guarantee: never lost, but may be delivered more than once.
- **co-17 · exactly-once** — once-and-only-once, achieved via idempotent/transactional producers plus idempotent consumers.
- **co-18 · idempotent-consumer** — dedup by recording processed message ids so a redelivery is a no-op (Richardson).
- **co-19 · event-sourcing** — persist state as an append-only sequence of events, never overwriting (Fowler).
- **co-20 · event-replay** — rebuild current state by folding the event stream from the beginning.
- **co-21 · snapshot** — a periodic state snapshot bounds replay cost (load snapshot + replay the tail).
- **co-22 · cqrs** — separate the write model from the read model (Fowler); independent from event sourcing.
- **co-23 · read-model-projection** — a denormalized read model built by projecting the event stream.
- **co-24 · dual-write-problem** — atomically updating the DB and publishing to a broker is unsafe; 2PC is undesirable.
- **co-25 · outbox-pattern** — store the message in the DB transaction; a separate relay publishes it (Richardson).
- **co-26 · saga** — a distributed workflow as a sequence of local transactions with compensating actions (Garcia-Molina).
- **co-27 · choreography-vs-orchestration** — events trigger the next step (choreography) vs a central orchestrator directing it.
- **co-28 · compensating-action** — undo the effects of completed steps, in reverse order, when a later step fails.
- **co-29 · dead-letter-queue** — poison/expired/rejected messages are routed aside for inspection (RabbitMQ DLX).
- **co-30 · poison-message-retry** — retry a failing message a bounded number of times (with backoff) before dead-lettering.
- **co-31 · eventual-consistency** — the read model lags the write model inside an inconsistency window, then converges.
- **co-32 · schema-evolution** — versioned event schemas kept backward/forward compatible so producers and consumers can drift (Schema Registry).
- **co-33 · when-not-eda** — a synchronous request/response CRUD flow gains nothing from a broker and loses straight-line debuggability.

## Tensions & trade-offs — when NOT to reach for this

- **The eventual-consistency tax**: decoupling via events means the read model lags, "did it work?" has no
  synchronous answer, and debugging spans logs across services. A synchronous call is simpler and
  correct-now — use events only when the decoupling is worth losing that.
- **Event sourcing is not free**: replayable logs and audit history are powerful, but schema evolution of
  old events, snapshotting, and rebuild time are real burdens. Most systems want plain state plus a few
  domain events, not full event sourcing.
- **When NOT to use it**: a simple request/response CRUD flow gains nothing from a broker and loses its
  straight-line debuggability. Reach for EDA when you have genuine async workflows, multiple independent
  consumers, or audit/replay needs.

## Lineage — why it beat the alternative

- EDA generalized from message-queue middleware (JMS; the enterprise-integration patterns of Hohpe & Woolf, 2003) and from the CQRS + event-sourcing work (Fowler, Young, ~2010) that answered high-throughput domains
  where the write and read shapes diverged. Kafka (2011) made durable, replayable logs cheap and normalized
  "the log as source of truth." Each step traded synchronous simplicity for decoupling and scale — so adopt
  the piece whose decoupling you actually need. It builds on the domain events of
  [`43-domain-driven-design`](./domain-driven-design.md) and the messaging basics of
  [`39-backend-at-scale`](./backend-at-scale.md).

## Worked examples

Colocated under `event-driven-architecture/learning/code/` as typed, pyright-clean Python; each runnable
against a local in-process bus or broker fake (DD-20/DD-30). Contiguous `ex-01..ex-80`. Every example cites
the `co-NN` it exercises; concepts are taught before the examples that use them.

### Beginner

- **ex-01 · event-as-fact** — model `OrderPlaced` as an immutable, past-tense event — verify the class is frozen and named as a fact. (co-01)
- **ex-02 · event-vs-command** — contrast `ShipOrder` (command) with `OrderShipped` (event) — verify each is typed by intent. (co-02)
- **ex-03 · event-vs-query** — a query returns data without changing state — verify no state mutation occurs. (co-02)
- **ex-04 · passive-aggressive-command** — an event misused as a command, then fixed to a command — verify the intent is now explicit. (co-02)
- **ex-05 · pub-sub-basic** — one publisher, two subscribers both receive — verify both handlers fire. (co-05)
- **ex-06 · pub-sub-decouple** — the publisher is unaware of subscriber count — verify adding a subscriber needs no publisher change. (co-05)
- **ex-07 · point-to-point-queue** — one message → one of N consumers — verify a single consumer handles it. (co-06)
- **ex-08 · competing-consumers** — work spread round-robin across consumers — verify each gets a fair share. (co-06)
- **ex-09 · queue-vs-pubsub** — the same message: queue delivers once, pub/sub to all — verify the two delivery counts. (co-05, co-06)
- **ex-10 · event-notification** — a thin event with an id + a callback link — verify the payload is minimal. (co-03)
- **ex-11 · event-notification-callback** — the receiver queries the source for details — verify the callback fetches the rest. (co-03)
- **ex-12 · event-carried-state** — the event carries the changed fields — verify the receiver needs no callback. (co-04)
- **ex-13 · local-replica** — a subscriber updates its own copy from the event — verify the replica matches after handling. (co-04)
- **ex-14 · notification-vs-state-transfer** — trade minimal payload vs data duplication — verify each approach's cost is named. (co-03, co-04)
- **ex-15 · in-process-event-bus** — a simple synchronous in-process bus — verify publish reaches all handlers. (co-05)
- **ex-16 · handler-registration** — subscribe and unsubscribe handlers — verify an unsubscribed handler stops firing. (co-05)
- **ex-17 · event-payload-schema** — a typed event dataclass with a version field — verify the version is carried. (co-32)
- **ex-18 · event-immutability** — a frozen event cannot be mutated after publish — verify `FrozenInstanceError`. (co-01)
- **ex-19 · multiple-handlers** — one event, several independent handlers — verify all run. (co-05)
- **ex-20 · handler-failure-isolation** — one handler failing does not block others — verify the rest still run. (co-05)
- **ex-21 · at-most-once** — fire-and-forget; a lost message is not retried — verify no redelivery. (co-15)
- **ex-22 · at-least-once** — redeliver on missing ack; may duplicate — verify a redelivery occurs. (co-16)
- **ex-23 · duplicate-delivery-demo** — the same message processed twice — verify the double effect appears. (co-16)
- **ex-24 · idempotent-consumer** — dedup by a processed-id set — verify a redelivery is a no-op. (co-18)
- **ex-25 · idempotent-upsert** — a naturally idempotent upsert handler — verify repeated apply yields one row. (co-18)
- **ex-26 · idempotency-key** — a per-message idempotency key gates processing — verify a duplicate key is skipped. (co-18)
- **ex-27 · dead-letter-basic** — reject a bad message to a DLQ — verify it lands in the dead-letter store. (co-29)
- **ex-28 · poison-retry-limit** — retry N times then dead-letter — verify it dead-letters after the limit. (co-30)

### Intermediate

- **ex-29 · event-store-append** — append events to an ordered log — verify order is preserved. (co-19)
- **ex-30 · event-sourced-aggregate** — an aggregate records events on commands — verify each command emits its event. (co-19)
- **ex-31 · rebuild-by-replay** — fold the event stream to reconstruct state — verify replayed state matches. (co-20)
- **ex-32 · replay-determinism** — replay yields identical state each time — verify two replays are equal. (co-20)
- **ex-33 · snapshot** — snapshot state to bound replay — verify the snapshot equals folded state. (co-21)
- **ex-34 · snapshot-plus-tail** — load a snapshot + replay only newer events — verify the tail-replay result matches full replay. (co-21)
- **ex-35 · append-only-no-overwrite** — assert state is never overwritten — verify the log only grows. (co-19)
- **ex-36 · event-versioning** — upcast a v1 event to v2 on read — verify the old event loads under the new schema. (co-32)
- **ex-37 · schema-backward-compat** — a new consumer reads old events — verify no field is missing. (co-32)
- **ex-38 · schema-forward-compat** — an old consumer reads new events — verify it ignores unknown fields. (co-32)
- **ex-39 · cqrs-write-model** — commands go through the write aggregate — verify reads never mutate it. (co-22)
- **ex-40 · cqrs-read-model** — a denormalized read model separate from the write model — verify it answers a query directly. (co-22, co-23)
- **ex-41 · read-model-projection** — project the event stream into the read model — verify each event updates the projection. (co-23)
- **ex-42 · read-model-rebuild** — rebuild the read model from scratch by replay — verify it matches the incremental one. (co-23, co-20)
- **ex-43 · read-model-lag** — the read model lags the write model — verify a just-written value isn't visible yet. (co-31)
- **ex-44 · eventual-consistency-window** — a stale read inside the inconsistency window — verify it converges after processing. (co-31)
- **ex-45 · topic-partition** — partition a topic; keys route to partitions — verify a key maps to one partition. (co-10, co-12)
- **ex-46 · partition-ordering** — ordering guaranteed within a partition only — verify per-partition order holds. (co-11)
- **ex-47 · cross-partition-no-order** — no total order across partitions — verify interleaving is possible. (co-11)
- **ex-48 · partition-by-key-locality** — one user's events all go to one partition — verify their order is preserved. (co-12)
- **ex-49 · consumer-group-queue** — same group = work-queue semantics — verify each message goes to one member. (co-13)
- **ex-50 · consumer-group-pubsub** — different groups = pub/sub semantics — verify every group gets every message. (co-13)
- **ex-51 · offset-commit** — commit the consumer offset after processing — verify a restart resumes past it. (co-10)
- **ex-52 · offset-rewind-replay** — rewind the offset to reprocess — verify old messages are re-read. (co-14)
- **ex-53 · retention-not-delete-on-consume** — a consumed message stays for retention — verify a second consumer still reads it. (co-14)
- **ex-54 · log-vs-queue-broker** — Kafka replay vs RabbitMQ delete-on-ack — verify the log allows re-read, the queue does not. (co-09)
- **ex-55 · exchange-binding** — a fanout exchange to bound queues — verify each bound queue receives a copy. (co-05, co-09)
- **ex-56 · ack-nack** — ack removes, nack requeues — verify a nacked message reappears. (co-09, co-16)

### Advanced

- **ex-57 · dual-write-problem** — show the DB-commits-but-publish-fails hole — verify the event can be lost. (co-24)
- **ex-58 · dual-write-lost-event** — a crash between commit and publish loses the event — verify the downstream never sees it. (co-24)
- **ex-59 · outbox-write** — store the event in the same DB transaction — verify it commits atomically with the state. (co-25)
- **ex-60 · outbox-relay** — a relay polls the outbox and publishes — verify pending rows are published. (co-25)
- **ex-61 · outbox-crash-safe** — a crash between write and publish still delivers — verify the relay recovers and publishes. (co-25)
- **ex-62 · outbox-idempotent-relay** — the relay marks published rows — verify a re-run does not double-publish. (co-25, co-18)
- **ex-63 · saga-choreography** — services react to each other's events — verify the workflow advances without an orchestrator. (co-26, co-27)
- **ex-64 · saga-orchestration** — a central orchestrator sequences steps — verify it directs each participant. (co-26, co-27)
- **ex-65 · saga-compensation** — a downstream failure triggers compensation — verify the prior step is undone. (co-26, co-28)
- **ex-66 · saga-compensation-order** — compensations run in reverse order — verify the undo sequence. (co-28)
- **ex-67 · saga-partial-failure** — compensate only the completed steps — verify uncompleted steps aren't compensated. (co-28)
- **ex-68 · mediator-topology** — a mediator orchestrates a multi-step event — verify it sequences the sub-events. (co-08)
- **ex-69 · broker-topology** — chained processors each emit the next event — verify the chain advances with no central control. (co-07)
- **ex-70 · broker-vs-mediator** — trade central control vs decoupling — verify each topology's cost is named. (co-07, co-08)
- **ex-71 · dlq-poison** — a repeatedly failing message lands in the DLQ — verify it stops retrying. (co-29, co-30)
- **ex-72 · dlq-inspect-replay** — inspect and replay a DLQ message after a fix — verify it processes on replay. (co-29)
- **ex-73 · exactly-once-illusion** — at-least-once + idempotency ≈ exactly-once — verify duplicates have no net effect. (co-17, co-18)
- **ex-74 · transactional-producer** — a transactional publish is all-or-nothing — verify a rollback publishes nothing. (co-17)
- **ex-75 · state-transfer-rebuild** — rebuild a downstream replica from state-carrying events — verify the replica reconstructs. (co-04)
- **ex-76 · ordering-with-key** — per-entity ordering via a partition key — verify one entity's events stay ordered. (co-12)
- **ex-77 · retry-with-backoff** — exponential backoff before dead-lettering — verify delays grow between retries. (co-30)
- **ex-78 · event-sourcing-audit** — the event log is an audit trail — verify past changes are reconstructable. (co-19)
- **ex-79 · when-not-eda** — a CRUD flow where a synchronous call is simpler — verify the sync version is shorter and correct-now. (co-33)
- **ex-80 · eda-slice** — order → payment → fulfillment: event sourcing + a CQRS read model + the outbox + an idempotent consumer + a saga with compensation + a DLQ — verify replay is deterministic, the read model stays consistent, redelivery applies once, the saga compensates, and poison messages reach the DLQ. (co-19, co-22, co-25, co-18, co-26, co-29)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build an event-driven slice of a domain (e.g. order → payment → fulfillment) using event
  sourcing for the write model, a CQRS read model rebuilt from events, the outbox pattern for reliable
  publish, idempotent consumers, a saga with a compensating action, and a dead-letter queue for poison
  messages — all runnable and tested against a local broker.
- **Concepts exercised**: [ ] pub/sub (co-05) [ ] event sourcing — append + replay + snapshot (co-19,
  co-20, co-21) [ ] a CQRS read model (co-22, co-23) [ ] the outbox pattern (co-24, co-25) [ ] an
  idempotent consumer (co-16, co-18) [ ] a saga + compensation (co-26, co-28) [ ] a DLQ (co-29, co-30).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — an event-sourced aggregate: append events + rebuild state by replay.
     Verify replay reconstructs identical state and a snapshot speeds it up.
  2. Add a CQRS read model projected from the event stream. Verify the read model matches the write
     model's state after processing.
  3. Add the outbox pattern (atomic write + relay publish) + an idempotent consumer. Verify a crash between
     write and publish still delivers, and a redelivery processes once.
  4. Add a saga with a compensating action + a DLQ. Verify a downstream failure triggers compensation and a
     poison message lands in the DLQ.
- **Acceptance criteria**: event replay is deterministic; the read model stays consistent; no lost or
  double-applied messages under redelivery; the saga compensates on failure; poison messages reach the DLQ.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Designing Event-Driven Systems** — Ben Stopford (2018). Free O'Reilly-published primer connecting Kafka, event sourcing, and CQRS into a coherent architecture story. <https://www.confluent.io/resources/ebook/designing-event-driven-systems/>
- **Building Event-Driven Microservices** — Adam Bellemare (2020). Standard modern treatment of stream-based, event-first microservice architecture.
- **Enterprise Integration Patterns** — Gregor Hohpe, Bobby Woolf (2003). The classic pattern catalog for asynchronous messaging that predates and underlies most event-driven architecture vocabulary.

**Papers & articles**

- **Event Sourcing** — Martin Fowler (2005). The widely cited article that named and popularized the event-sourcing pattern. <https://martinfowler.com/eaaDev/EventSourcing.html>
- **CQRS** — Martin Fowler (2011). Canonical explanation of Command Query Responsibility Segregation and its relationship to event sourcing. <https://martinfowler.com/bliki/CQRS.html>
- **Kafka: a Distributed Messaging System for Log Processing** — Jay Kreps, Neha Narkhede, Jun Rao (2011), NetDB. The original paper describing Kafka's log-centric design, now the reference architecture for event streaming.

## In which paths

- `interview-ready/software-engineer` — Go deeper · Architecture, distributed & internals builds — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Architecture, distributed & internals builds — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 7 · Networking, architecture & distributed systems.

> _Content originated in the now-closed FS-SE plan (topic 45); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
