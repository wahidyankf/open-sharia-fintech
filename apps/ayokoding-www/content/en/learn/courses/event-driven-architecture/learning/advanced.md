---
title: "Advanced Examples"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 30
---

These examples close the delivery gaps that appear when independent services update state, publish
facts, and recover from partial failure. Their complete executable counterparts are in
[`example.py`](./code/example.py) and the capstone.

## Reliable publication and distributed workflows

### Example 57: Dual-Write Problem

Writing a database row and publishing a message are two separate failure points. This is `co-24`.

```python
database_committed, published = True, False  # => crash or broker failure can split the two effects
print(database_committed, published)  # => Output: True False
```

**Key takeaway**: Two independent writes are not atomic merely because they are adjacent in code.

**Why it matters**: A downstream projection cannot react to a fact it never receives, even though
the source state says it happened. Retrying the entire request may duplicate the database effect,
so the failure needs a durable handoff rather than hopeful retry.

### Example 58: Dual-Write Lost Event

A process can crash after committing state but before publishing its event. This is `co-24`.

```python
state = {"o-1": "paid"}  # => source transaction completed
downstream_seen = []  # => no publish occurred before the simulated crash
print(state["o-1"], downstream_seen)  # => Output: paid []
```

**Key takeaway**: A committed state change does not imply a delivered integration event.

**Why it matters**: The invisible gap causes the most damaging form of integration bug: one service
is correct locally while every dependent service stays stale forever. Detecting it after the fact is
hard because the missing message leaves no natural retry record.

### Example 59: Outbox Write

The outbox records state and an unpublished event in one local transaction. This is `co-25`.

```python
transaction = {"state": "paid", "outbox": "PaymentCaptured"}  # => both rows commit together
assert set(transaction) == {"state", "outbox"}  # => no state-only success is represented
print(transaction["outbox"])  # => Output: PaymentCaptured
```

**Key takeaway**: Persist the event before asking any broker to deliver it.

**Why it matters**: A durable outbox turns an unobservable publish gap into a recoverable pending
record. It does not make delivery exactly once; the relay can crash after publish, so consumers must
still deduplicate by message identity.

### Example 60: Outbox Relay

A relay reads unpublished outbox rows and sends them to the broker. This is `co-25`.

```python
pending, published = ["PaymentCaptured"], []  # => relay owns transport after the transaction commits
published.append(pending.pop(0))  # => one pending row moves to published delivery work
print(published)  # => Output: ['PaymentCaptured']
```

**Key takeaway**: The relay is retryable infrastructure, not business decision logic.

**Why it matters**: Separating publish from the request path lets a temporary broker outage delay
integration without rolling back a valid local transaction. Relays need monitoring for age and
backlog because a growing outbox is a visible consistency delay.

### Example 61: Outbox Crash Safe

After a crash, an unpublished outbox row remains available to a restarted relay. This is `co-25`.

```python
outbox_row = {"event": "OrderPlaced", "published": False}  # => durable pending work survives a process crash
should_relay = not outbox_row["published"]  # => recovery finds the row without guessing what happened
print(should_relay)  # => Output: True
```

**Key takeaway**: Recovery starts from durable pending state.

**Why it matters**: The outbox removes the need to reconstruct missing events from application logs.
It moves correctness from a timing-sensitive window into a queryable table whose retry and alerting
policy can be operated deliberately.

### Example 62: Outbox Idempotent Relay

The relay marks a row published, and consumers still guard against a repeated send. This combines
`co-25` and `co-18`.

```python
row = {"id": "m-1", "published": True}  # => a previous relay attempt completed its local marking
send_again = not row["published"]  # => rerun skips the row; consumer would also deduplicate m-1
print(send_again)  # => Output: False
```

**Key takeaway**: Relay state reduces duplicates; idempotent consumers make duplicates harmless.

**Why it matters**: A crash between broker publish and row marking can still produce redelivery.
Design both sides of the boundary: the relay tracks progress for efficiency, while the consumer owns
the final exactly-once _effect_ through its idempotency record.

### Example 63: Saga Choreography

In choreography, each service reacts to an event and emits the next fact. This is `co-26` and `co-27`.

```python
flow = ["OrderPlaced", "PaymentCaptured", "FulfilmentRequested"]  # => each event triggers the next local action
print(flow[-1])  # => Output: FulfilmentRequested
```

**Key takeaway**: Choreography distributes workflow knowledge among participants.

**Why it matters**: This style keeps services decoupled and works well for short, stable flows.
As branches, timeouts, and visibility needs grow, the implicit workflow can become difficult to
understand because no single component can explain the current overall state.

### Example 64: Saga Orchestration

An orchestrator sends commands in a defined workflow order. This is `co-26` and `co-27`.

```python
commands = ["ReserveInventory", "CapturePayment", "RequestFulfilment"]  # => central coordinator directs next step
print(commands[0])  # => Output: ReserveInventory
```

**Key takeaway**: Orchestration centralizes workflow decisions, not participant data ownership.

**Why it matters**: A central coordinator makes long-running state, timeout, and retry policy easier
to inspect. It can become a coupling point if it absorbs domain logic that rightly belongs to the
service performing each local transaction.

### Example 65: Saga Compensation

When a later local transaction fails, compensate completed earlier transactions. This is `co-26`
and `co-28`.

```python
completed, compensated = ["reserve"], []  # => inventory was the only completed local action
compensated.append("undo-reserve")  # => failure triggers a business undo event
print(compensated)  # => Output: ['undo-reserve']
```

**Key takeaway**: Compensation is a new business action, not a database rollback.

**Why it matters**: Services do not share one transaction manager, so a workflow cannot undo time.
Compensation must be idempotent and domain-valid: releasing inventory is plausible, but “unsending”
an email may require a different corrective action.

### Example 66: Saga Compensation Order

Compensate completed steps in reverse order of their effects. This is `co-28`.

```python
completed = ["reserve", "charge"]  # => causal execution order of completed local transactions
undo = [f"undo-{step}" for step in reversed(completed)]  # => reverse order preserves dependencies
print(undo)  # => Output: ['undo-charge', 'undo-reserve']
```

**Key takeaway**: Reverse order protects the assumptions of earlier steps.

**Why it matters**: Releasing inventory before undoing a dependent payment can expose an invalid
intermediate state. Treat compensation sequencing as a tested part of the workflow definition, not
as an emergency script written after the first failure.

### Example 67: Saga Partial Failure

Only completed actions need compensation; an unstarted step has no effect to undo. This is `co-28`.

```python
completed = ["reserve"]  # => payment never completed, so it has no compensating action
undo = ["undo-" + step for step in reversed(completed)]  # => compensation targets exactly completed work
print(undo)  # => Output: ['undo-reserve']
```

**Key takeaway**: Record completion before attempting the next step.

**Why it matters**: Ambiguous progress leads to accidental compensation of work that never happened
or missed compensation of work that did. Durable saga state and idempotent commands let recovery
continue safely after a coordinator restart.

## Topology, dead letters, delivery, and the integrated slice

### Example 68: Mediator Topology

A mediator observes an input event and sequences several subordinate actions. This is `co-08`.

```python
steps = {"OrderPlaced": ["reserve", "charge", "fulfil"]}  # => one mediator owns the multi-step routing policy
print(steps["OrderPlaced"])  # => Output: ['reserve', 'charge', 'fulfil']
```

**Key takeaway**: Mediators make central workflow order explicit.

**Why it matters**: Central visibility is valuable when a business process has branches, deadlines,
and compensation. The mediator should publish commands or events through contracts rather than
reach into participant databases, preserving service autonomy.

### Example 69: Broker Topology

In broker topology, processors form a chain by publishing the next event. This is `co-07`.

```python
chain = ["OrderPlaced", "InventoryReserved", "PaymentCaptured"]  # => no central component owns every transition
print(chain[-1])  # => Output: PaymentCaptured
```

**Key takeaway**: Broker chains favor decoupled, locally owned reactions.

**Why it matters**: The chain remains extensible because a new processor can subscribe without
modifying earlier ones. Its distributed flow is harder to visualize, so correlation ids, tracing,
and event naming discipline become essential operational tools.

### Example 70: Broker vs Mediator

Broker chaining maximizes decoupling; a mediator maximizes central control. This compares `co-07`
and `co-08`.

```python
broker_cost, mediator_cost = "distributed visibility", "central coupling"  # => each topology has a distinct price
print(broker_cost, mediator_cost)  # => Output: distributed visibility central coupling
```

**Key takeaway**: Choose topology by workflow complexity and ownership, not fashion.

**Why it matters**: A two-step independent reaction rarely needs an orchestrator, while a regulated
multi-step business process benefits from explicit progress and timeout policy. Both choices require
clear message contracts and recovery behavior.

### Example 71: DLQ Poison

A message that repeatedly fails stops retrying and lands in the DLQ. This is `co-29` and `co-30`.

```python
attempts, limit = 3, 3  # => retry budget has been exhausted
destination = "dlq" if attempts >= limit else "retry"  # => poison work leaves the hot path
print(destination)  # => Output: dlq
```

**Key takeaway**: Terminal routing protects healthy traffic from poison loops.

**Why it matters**: A malformed event can otherwise consume every worker forever and obscure the
real incident. Dead-lettering preserves the original payload and error context so a fixed consumer
can inspect, correct, and replay it under controlled conditions.

### Example 72: DLQ Inspect Replay

After correcting the fault, inspect a dead letter and replay it into the normal path. This is `co-29`.

```python
dlq, processed = ["m-1"], []  # => failed message remains available for an operator-approved replay
processed.append(dlq.pop(0))  # => repaired handler receives the original message identity
print(processed)  # => Output: ['m-1']
```

**Key takeaway**: Replay is a deliberate repair operation, not automatic deletion.

**Why it matters**: Operators need the error, attempt count, correlation id, and payload to decide
whether replay is safe. The consumer must remain idempotent because a prior attempt may have applied
some local effect before failing.

### Example 73: Exactly-Once Illusion

At-least-once transport plus idempotent effects delivers the practical outcome commonly called
exactly once. This is `co-17` and `co-18`.

```python
deliveries, effects = ["m-1", "m-1"], {"m-1"}  # => two deliveries create one recorded effect identity
print(len(deliveries), len(effects))  # => Output: 2 1
```

**Key takeaway**: Count durable business effects, not packets, when discussing exactly once.

**Why it matters**: Network retries and crashes cannot be wished away by a broker label. Idempotency
at the database or external-provider boundary gives users one visible outcome even while the system
correctly tolerates repeated message delivery.

### Example 74: Transactional Producer

A transactional producer either publishes all records in a unit or none. This is `co-17`.

```python
staged, committed = ["InventoryReserved"], []  # => records are hidden until transaction commit
rollback = True  # => simulated failure chooses rollback rather than partial publish
print(committed if rollback else staged)  # => Output: []
```

**Key takeaway**: Transactional publish protects a broker-local batch, not every external effect.

**Why it matters**: Atomic broker records help consumers avoid seeing a half-written sequence. They
do not solve the database-to-broker dual write, which still needs an outbox or a deliberately shared
transactional boundary.

### Example 75: State-Transfer Rebuild

A downstream replica can rebuild from state-carrying events alone. This is `co-04`.

```python
events = [("o-1", "placed"), ("o-1", "paid")]  # => each fact includes the state a projection needs
replica = {key: value for key, value in events}  # => replay reconstructs the latest local copy
print(replica)  # => Output: {'o-1': 'paid'}
```

**Key takeaway**: Rich events make independent rebuild possible.

**Why it matters**: A new projection can consume retained history even if the source service is
offline. Schema size and privacy classification grow with copied state, so transfer only the fields
that consumers genuinely need for stable local decisions.

### Example 76: Ordering with Key

A stable entity key keeps that entity’s event sequence in one partition. This is `co-12`.

```python
events = ["o-9:placed", "o-9:paid"]  # => both transitions use the same order id as partition key
ordered = events == sorted(events, key=lambda value: ["o-9:placed", "o-9:paid"].index(value))  # => per-key order holds
print(ordered)  # => Output: True
```

**Key takeaway**: Per-entity ordering is designed through the key.

**Why it matters**: A random key may improve load distribution while allowing `paid` to overtake
`placed` for one order. A stable aggregate key preserves the transition invariant and still allows
unrelated orders to process in parallel.

### Example 77: Retry with Backoff

Exponential backoff increases delay between failed attempts before dead-lettering. This is `co-30`.

```python
delays = [2**attempt for attempt in range(3)]  # => retry delay grows instead of hammering a broken dependency
assert delays == [1, 2, 4]  # => growth is explicit and testable
print(delays)  # => Output: [1, 2, 4]
```

**Key takeaway**: Backoff protects dependencies and leaves room for recovery.

**Why it matters**: Immediate retries create a feedback loop during outages, consuming workers and
making the dependency less likely to recover. Combine capped backoff with jitter in production and a
DLQ after the bounded retry budget.

### Example 78: Event-Sourcing Audit

An append-only stream answers how a state changed over time. This is `co-19`.

```python
audit = ["OrderPlaced", "PaymentCaptured", "OrderCancelled"]  # => each historical transition remains visible
print(" -> ".join(audit))  # => Output: OrderPlaced -> PaymentCaptured -> OrderCancelled
```

**Key takeaway**: Audit is a natural consequence of preserving facts.

**Why it matters**: An audit trail is useful only when events carry stable meaning, identity, and
causal order. Avoid treating it as an excuse to log sensitive data indiscriminately; retention and
privacy controls still apply to durable event history.

### Example 79: When Not to Use EDA

A synchronous CRUD update can be simpler and immediately correct for one owner. This is `co-33`.

```python
profile = {"name": "Ada"}  # => one service owns one straightforward resource
profile["name"] = "Ada Lovelace"  # => direct update gives an immediate read-your-write result
print(profile["name"])  # => Output: Ada Lovelace
```

**Key takeaway**: Do not pay asynchronous complexity without an independent-consumer benefit.

**Why it matters**: Brokers add operational cost, schema compatibility, retries, and stale reads.
When no other service needs an asynchronous fact, a direct transaction is easier to reason about,
debug, secure, and explain to users.

### Example 80: EDA Slice

An integrated order slice combines event sourcing, CQRS, outbox relay, idempotency, compensation,
and a DLQ. This exercises `co-19`, `co-22`, `co-25`, `co-18`, `co-26`, and `co-29`.

```python
facts = ["OrderPlaced", "PaymentCaptured"]  # => event store supplies deterministic write history
read_model = {"o-1": "paid"}  # => projection exposes query state after processing those facts
print(facts[-1], read_model["o-1"])  # => Output: PaymentCaptured paid
```

**Key takeaway**: Reliable EDA is a set of cooperating invariants, not one feature.

**Why it matters**: The capstone proves the full slice under redelivery and failure: the read model
rebuilds from the event stream, the outbox survives a publish gap, consumer effects apply once,
compensation runs on failure, and poison messages reach the DLQ. Continue with the complete
[capstone](./capstone/overview.md).
