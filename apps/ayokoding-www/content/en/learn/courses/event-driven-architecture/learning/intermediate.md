---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 20
---

Intermediate work makes an event stream a source of state, then models a broker log without
pretending that partition-local ordering is a global order. The checked reference remains
[`example.py`](./code/example.py).

## Event stores, replay, and CQRS

### Example 29: Event Store Append

An event store only grows; append order is the stream’s causal order. This is `co-19`.

```python
stream = ["OrderPlaced", "PaymentCaptured"]  # => append preserves occurrence order
assert stream == sorted(stream, key=lambda name: ["OrderPlaced", "PaymentCaptured"].index(name))  # => order is observable
print(stream)  # => Output: ['OrderPlaced', 'PaymentCaptured']
```

**Key takeaway**: Preserve the original event sequence; never overwrite it.

**Why it matters**: An append-only stream provides both an audit history and the input for replay.
Changing an old fact rewrites causality for every projection and makes forensic reconstruction
dependent on whichever consumer happened to read before the mutation.

### Example 30: Event-Sourced Aggregate

An aggregate handles a command by recording one or more events, rather than directly persisting a
mutable current state. This is `co-19`.

```python
pending = []  # => aggregate records uncommitted domain facts
pending.append("OrderPlaced")  # => a valid command emits a past-tense event
print(pending)  # => Output: ['OrderPlaced']
```

**Key takeaway**: Commands decide; events record the decision.

**Why it matters**: The event stream explains why the aggregate is in its state, not only what the
latest state happens to be. That history enables audit and rebuild, but requires intentional schema
evolution because old facts outlive today’s code.

### Example 31: Rebuild by Replay

Fold events from an initial state to reconstruct current state. This is `co-20`.

```python
state = "new"  # => replay begins from a known empty aggregate state
state = "paid" if ["OrderPlaced", "PaymentCaptured"] else state  # => ordered facts produce current state
print(state)  # => Output: paid
```

**Key takeaway**: Current state is a projection of history.

**Why it matters**: Replay turns a lost or buggy read model into a rebuildable derivative rather
than an irreplaceable source of truth. The fold must be deterministic, or two consumers processing
the same stream will disagree about the same business facts.

### Example 32: Replay Determinism

The same stream must produce identical state every time it is replayed. This is `co-20`.

```python
stream = ("OrderPlaced", "PaymentCaptured")  # => immutable input for both replay runs
first, second = stream[-1], stream[-1]  # => identical folds over identical input agree
print(first == second)  # => Output: True
```

**Key takeaway**: Determinism is a correctness property, not an optimization.

**Why it matters**: Nondeterministic clock reads, random values, or hidden network calls make a
replay unreproducible. Keep reducers pure and put time-dependent effects at the boundary so audit,
debugging, and recovery have a trustworthy answer.

### Example 33: Snapshot

A snapshot stores a folded state at a known stream position to bound replay work. This is `co-21`.

```python
snapshot = {"position": 2, "state": "paid"}  # => state after the first two events
assert snapshot["position"] == 2  # => replay can start after this position
print(snapshot["state"])  # => Output: paid
```

**Key takeaway**: Snapshots are caches; events remain authoritative.

**Why it matters**: A long stream need not replay from zero for every load, but a corrupt or stale
snapshot must be discardable. Keep the stream position and schema version with the snapshot so its
validity is explicit.

### Example 34: Snapshot Plus Tail

Load a snapshot then fold only events after its recorded position. This is `co-21`.

```python
snapshot, tail = "placed", ["PaymentCaptured"]  # => historical prefix is already folded
state = "paid" if tail == ["PaymentCaptured"] else snapshot  # => tail advances snapshot state
print(state)  # => Output: paid
```

**Key takeaway**: Snapshot-plus-tail must equal a full replay.

**Why it matters**: A snapshot that changes the result is not an optimization; it is data loss.
Tests should compare full replay against snapshot-plus-tail whenever reducers or snapshot schemas
change.

### Example 35: Append-Only No Overwrite

Correcting an order appends a new fact instead of replacing its old one. This is `co-19`.

```python
stream = ["OrderPlaced"]  # => historic fact stays in the log
stream.append("OrderCancelled")  # => correction is another causal fact, not an edit
print(len(stream))  # => Output: 2
```

**Key takeaway**: Model correction as history, not mutation.

**Why it matters**: An audit needs to show both placement and cancellation. Appending preserves the
reasoning path for projections and human investigators, while an overwrite erases evidence that
downstream consumers may already have acted upon.

### Example 36: Event Versioning

An upcaster reads an old payload and supplies a new default field. This is `co-32`.

```python
v1 = {"version": 1, "id": "o-1"}  # => historical schema lacks currency
v2 = {**v1, "version": 2, "currency": "USD"}  # => reader adapts old data at its boundary
print(v2["currency"])  # => Output: USD
```

**Key takeaway**: Make readers compatible with historical events.

**Why it matters**: Event stores preserve years of data, so replacing every old record is risky and
expensive. An explicit upcaster isolates compatibility logic and lets the domain reducer receive one
current representation.

### Example 37: Schema Backward Compatibility

A new consumer can read an old event by providing defaults for absent optional fields. This is `co-32`.

```python
old_event = {"id": "o-1"}  # => producer from an earlier deployment
currency = old_event.get("currency", "USD")  # => new reader preserves an intentional default
print(currency)  # => Output: USD
```

**Key takeaway**: Additive fields with clear defaults preserve old events.

**Why it matters**: Producers and consumers cannot deploy atomically in a distributed system. A new
consumer that rejects every retained old message turns a routine rollout into a replay outage and
makes rollback unnecessarily dangerous.

### Example 38: Schema Forward Compatibility

An old consumer ignores unknown fields it does not need. This is `co-32`.

```python
new_event = {"id": "o-1", "currency": "USD"}  # => newer producer includes an additive field
old_view = {"id": new_event["id"]}  # => older reader retains only its known contract
print(old_view)  # => Output: {'id': 'o-1'}
```

**Key takeaway**: Consumers should ignore safe unknown fields.

**Why it matters**: Forward compatibility lets producers add optional information without waiting for
every subscriber. Removing or changing meaning is different: it breaks contracts and requires a
versioned migration rather than optimistic field filtering.

### Example 39: CQRS Write Model

Commands enter a write model; queries do not mutate it. This is `co-22`.

```python
write_model = {"o-1": "placed"}  # => command handling owns this authoritative state
queried = write_model["o-1"]  # => reading observes but does not change the aggregate
print(queried)  # => Output: placed
```

**Key takeaway**: Keep decision logic on the write side.

**Why it matters**: A write model can protect invariants without being shaped for every screen or
report. Separating it from query projections removes pressure to turn one model into an unmaintainable
compromise between consistency checks and presentation convenience.

### Example 40: CQRS Read Model

A read model is denormalized for one direct query. This is `co-22` and `co-23`.

```python
read_model = {"o-1": {"status": "paid", "total": "42"}}  # => query-shaped projection
print(read_model["o-1"]["status"])  # => Output: paid
```

**Key takeaway**: A projection may duplicate data to make reads simple.

**Why it matters**: Query code should not need to re-run write-side domain logic or join several
services synchronously. The price is eventual consistency, which callers must see as a normal state
rather than a surprise error.

### Example 41: Read-Model Projection

Each relevant event updates the projection once. This is `co-23`.

```python
projection = {"o-1": "placed"}  # => event projection after OrderPlaced
projection["o-1"] = "paid"  # => PaymentCaptured advances the query view
print(projection["o-1"])  # => Output: paid
```

**Key takeaway**: Projection handlers are deterministic reducers over facts.

**Why it matters**: A projection should be cheap to rebuild and safe to replay. Avoid hidden calls
or request-time business decisions inside a projector; otherwise a replay depends on today’s network
and code rather than the stored event sequence.

### Example 42: Read-Model Rebuild

Replaying the stream into an empty projection must match the incremental projection. This is `co-23`
and `co-20`.

```python
incremental = {"o-1": "paid"}  # => state built while events arrived
rebuilt = {"o-1": "paid"}  # => state rebuilt from the same retained event stream
print(incremental == rebuilt)  # => Output: True
```

**Key takeaway**: Rebuildability is the projection’s recovery plan.

**Why it matters**: A bug can corrupt a derived table without corrupting the event source. Rebuild
turns repair into a controlled replay, provided retention, schema handling, and idempotent reducer
behavior have been designed from the beginning.

### Example 43: Read-Model Lag

The write model can accept a change before the asynchronous projection sees it. This is `co-31`.

```python
write_state, read_state = "paid", "placed"  # => projection has not processed PaymentCaptured yet
print(write_state, read_state)  # => Output: paid placed
```

**Key takeaway**: A stale read can be correct during the inconsistency window.

**Why it matters**: Client experiences must account for a short gap between accepted command and
visible projection. Show pending status, retry a query, or read the write model when necessary;
never silently promise immediate cross-service convergence.

### Example 44: Eventual Consistency Window

Once the projection processes the pending event, the stale read converges. This is `co-31`.

```python
read_state = "placed"  # => value before the queued projection event runs
read_state = "paid"  # => eventual handler processing converges the replica
print(read_state)  # => Output: paid
```

**Key takeaway**: Eventual consistency means convergence, not permanent disagreement.

**Why it matters**: The duration of the window is an operational SLO shaped by broker lag and handler
health. Monitor it explicitly, because a long or growing window signals a capacity, poison-message,
or downstream dependency problem.

## Logs, partitions, consumer groups, and acknowledgement

### Example 45: Topic Partition

A partition key deterministically routes a record to one partition. This is `co-10` and `co-12`.

```python
partition = sum(map(ord, "o-1")) % 3  # => stable key hash selects one of three partitions
assert 0 <= partition < 3  # => topic partition is a bounded integer address
print(partition)  # => Output: 2
```

**Key takeaway**: Partitioning splits throughput while preserving a local sequence.

**Why it matters**: A topic can scale beyond one consumer or machine only by splitting its log.
The key is therefore a correctness choice: entities that require ordered transitions must route to
the same partition.

### Example 46: Partition Ordering

Records in one partition retain producer append order. This is `co-11`.

```python
partition = ["o-1:placed", "o-1:paid"]  # => same key stays on one ordered log
assert partition[0].endswith("placed")  # => first transition precedes payment
print(partition)  # => Output: ['o-1:placed', 'o-1:paid']
```

**Key takeaway**: Ordering is per partition, never per topic globally.

**Why it matters**: Consumers may safely apply one order’s transitions sequentially when its key is
stable. Assuming a total cross-partition order creates race bugs because independent partitions
progress and retry at different rates.

### Example 47: Cross-Partition No Order

Two partition-local sequences can interleave in several valid global orders. This is `co-11`.

```python
observed = ["p0:paid", "p1:placed"]  # => independent partitions may arrive in either interleaving
assert len(observed) == 2  # => both records exist without a total-order guarantee
print(observed)  # => Output: ['p0:paid', 'p1:placed']
```

**Key takeaway**: Design cross-entity workflows without a fictitious global sequence.

**Why it matters**: Distributed logs optimize throughput by allowing partitions to advance
independently. Sagas and correlation ids coordinate business progress explicitly instead of relying
on timing between unrelated entity streams.

### Example 48: Partition by Key Locality

All events for one user or order use the same partition key. This is `co-12`.

```python
keys = ["order-7", "order-7"]  # => both facts identify the same aggregate
partitions = [sum(map(ord, key)) % 4 for key in keys]  # => stable key yields stable locality
print(partitions)  # => Output: [0, 0]
```

**Key takeaway**: Put the aggregate identity in the partition key.

**Why it matters**: Locality allows one consumer to apply a single aggregate’s sequence in order.
Overly broad keys create hot partitions; overly narrow or random keys break the ordering invariant,
so choose the smallest identity that needs serial reasoning.

### Example 49: Consumer Group Queue

Members of one consumer group share partitions, giving queue-like work distribution. This is `co-13`.

```python
assignment = {"partition-0": "worker-a", "partition-1": "worker-b"}  # => one group member per partition
print(len(set(assignment.values())))  # => Output: 2
```

**Key takeaway**: One group consumes each record once as a unit of work.

**Why it matters**: Consumer groups scale a projection or worker while preventing duplicate group
effects. A rebalance moves responsibility between members, so handlers must tolerate restart and
redelivery around an offset commit boundary.

### Example 50: Consumer Group Pub/Sub

Different groups each receive the same topic records independently. This is `co-13`.

```python
groups = {"billing": "m-1", "analytics": "m-1"}  # => each group has its own offset and effect
print(sorted(groups))  # => Output: ['analytics', 'billing']
```

**Key takeaway**: Groups combine queue semantics within a service and pub/sub across services.

**Why it matters**: Billing and analytics need not coordinate their deployment or replay. Their
independent offsets let one rebuild historic data without forcing the other to reprocess an already
healthy production workload.

### Example 51: Offset Commit

A consumer commits its position only after it has safely applied the record. This is `co-10`.

```python
processed_offset = 7  # => record 7’s effect completed successfully
committed_offset = processed_offset  # => restart resumes after the durable checkpoint
print(committed_offset)  # => Output: 7
```

**Key takeaway**: Commit after the idempotent effect, not before it.

**Why it matters**: Committing early risks a lost effect after a crash; committing late can cause
redelivery. An idempotent consumer makes the safer late-commit choice operationally acceptable and
preserves at-least-once semantics.

### Example 52: Offset Rewind Replay

Resetting an offset makes retained historic records readable again. This is `co-14`.

```python
offset = 5  # => consumer currently starts after earlier records
offset = 0  # => rewind requests a full replay from retained history
print(offset)  # => Output: 0
```

**Key takeaway**: Retention, not acknowledgement, makes replay possible.

**Why it matters**: A new projection or repaired bug can consume old facts without asking producers
to resend them. Rewind is powerful and dangerous: confirm handlers are idempotent and target a
separate rebuild table when replaying production history.

### Example 53: Retention Not Delete on Consume

Reading a log record does not remove it before its retention policy expires. This is `co-14`.

```python
log = ["m-1"]  # => retained topic history
first, second = log[0], log[0]  # => two consumers can read the same retained record
print(first == second)  # => Output: True
```

**Key takeaway**: Log consumption advances an offset, not the record’s deletion.

**Why it matters**: Retention supports independent consumer groups, replay, and audit. Storage cost
and privacy retention policy still matter, so design a bounded retention period and archival strategy
instead of assuming a log is infinitely cheap.

### Example 54: Log vs Queue Broker

A log supports reread by offset; a queue removes work after acknowledgement. This is `co-09`.

```python
log_can_replay, queue_after_ack = True, []  # => retained log differs from acknowledged queue work
print(log_can_replay, queue_after_ack)  # => Output: True []
```

**Key takeaway**: Pick log or queue semantics according to replay and work-distribution needs.

**Why it matters**: Treating one model as the other produces surprising recovery behavior. A
projection benefits from retained logs, while a one-time job often benefits from queue removal and a
clear acknowledgement lifecycle.

### Example 55: Exchange Binding

A fanout exchange routes one message to every bound queue. This is `co-05` and `co-09`.

```python
bound_queues = ["email", "analytics"]  # => queues subscribe through one exchange binding
copies = [f"OrderPlaced->{queue}" for queue in bound_queues]  # => fanout emits one copy per binding
print(copies)  # => Output: ['OrderPlaced->email', 'OrderPlaced->analytics']
```

**Key takeaway**: Bindings express routing policy outside the publisher.

**Why it matters**: Exchanges let operators add or remove independent consumers without changing the
event producer. Routing rules themselves become deployable infrastructure and should be tested like
any other contract that controls business side effects.

### Example 56: Ack and Nack

Acknowledgement completes a queue delivery; negative acknowledgement requeues it. This is `co-09`
and `co-16`.

```python
pending = ["m-1"]  # => one delivery is currently available
message = pending.pop(0); pending.append(message)  # => nack requeues rather than losing the message
print(pending)  # => Output: ['m-1']
```

**Key takeaway**: Acknowledge only after the consumer’s durable effect succeeds.

**Why it matters**: Ack and nack decide whether a broker may safely discard or redeliver work.
They cannot prove an external effect completed, which is why a message identity and idempotent effect
are still necessary even with reliable broker acknowledgement.
