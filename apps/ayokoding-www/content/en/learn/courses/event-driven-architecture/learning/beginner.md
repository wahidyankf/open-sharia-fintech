---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 10
---

These examples establish an event as an immutable fact, then make routing and retry semantics
visible with only standard-library Python. The complete checked implementation is
[`example.py`](./code/example.py).

## Facts, commands, and routing

### Example 1: Event as Fact

An event records something that has already happened, so its name is past tense and its data is not
rewritten. This is `co-01`.

```python
event = {"name": "OrderPlaced"}  # => a past-tense business fact
assert event["name"].endswith("Placed")  # => the name describes a completed occurrence
print(event["name"])  # => Output: OrderPlaced
```

**Key takeaway**: Publish facts such as `OrderPlaced`, not future instructions.

**Why it matters**: Consumers can independently decide whether a fact concerns them. That freedom
is what removes a publisher’s dependency on today’s subscriber list while retaining an audit-worthy
statement of the business change.

### Example 2: Event vs Command

A command requests work and may be rejected; an event reports work that succeeded. This is `co-02`.

```python
command = {"name": "ShipOrder", "intent": "request"}  # => a handler may reject this request
event = {"name": "OrderShipped", "intent": "fact"}  # => this fact cannot be rejected retroactively
print(command["intent"], event["intent"])  # => Output: request fact
```

**Key takeaway**: Type the intent before designing a message payload.

**Why it matters**: Calling a command an event hides ownership and error handling. A receiver must
know whether it is obligated to perform an action or merely free to react to a recorded outcome.

### Example 3: Event vs Query

A query returns information and does not change the write model. This is also `co-02`.

```python
orders = {"o-1": "placed"}  # => the observable read-model state
answer = orders["o-1"]  # => query reads one value without mutating the mapping
print(answer, orders["o-1"])  # => Output: placed placed
```

**Key takeaway**: Queries observe state; commands change it; events describe the result.

**Why it matters**: Separating the three intents prevents a “read” API from acquiring hidden write
effects. It also makes a CQRS boundary legible later, when write and read models intentionally differ.

### Example 4: Passive-Aggressive Command

`OrderShouldShip` sounds like a fact but asks a downstream service to act. Use an explicit command
instead. This is `co-02`.

```python
bad = "OrderShouldShip"  # => a disguised instruction that pretends to be an event
good = "ShipOrder"  # => an explicit command with an accountable handler
print(bad, "->", good)  # => Output: OrderShouldShip -> ShipOrder
```

**Key takeaway**: Do not smuggle commands through event names.

**Why it matters**: A passive-aggressive command makes retries, authorization, and rejection paths
ambiguous. Explicit command ownership keeps the failure contract with the service that can actually
decide whether shipping is valid.

### Example 5: Pub/Sub Basic

One published fact can reach several independent subscribers. This is `co-05`.

```python
handlers = ["billing", "email"]  # => each handler subscribed independently
received = [f"{handler}:OrderPlaced" for handler in handlers]  # => fanout creates one observation each
print(received)  # => Output: ['billing:OrderPlaced', 'email:OrderPlaced']
```

**Key takeaway**: Pub/sub broadcasts one fact to every subscription.

**Why it matters**: Billing and notification can evolve independently because neither becomes a
required synchronous call from ordering. Each can fail, scale, deploy, and replay on its own schedule.

### Example 6: Pub/Sub Decoupling

The publisher emits a named event without knowing how many subscribers exist. This is `co-05`.

```python
subscribers = {"OrderPlaced": ["billing"]}  # => publisher knows only the event contract
subscribers["OrderPlaced"].append("analytics")  # => adding a consumer changes no publisher code
print(len(subscribers["OrderPlaced"]))  # => Output: 2
```

**Key takeaway**: Add subscribers at the broker boundary, not inside the publisher.

**Why it matters**: This decoupling permits new analytical or compliance reactions after deployment.
It also means the event schema becomes a public contract whose compatibility deserves the same care
as an API.

### Example 7: Point-to-Point Queue

A work queue gives one message to one competing consumer rather than broadcasting it. This is `co-06`.

```python
workers = ["worker-a", "worker-b"]  # => competing consumers share one queue
recipient = workers[0]  # => one delivery chooses exactly one worker
print(recipient)  # => Output: worker-a
```

**Key takeaway**: Queue semantics distribute work; pub/sub semantics distribute facts.

**Why it matters**: A payment capture must happen once per queued job, whereas an `OrderPlaced` fact
may legitimately be observed by many services. Selecting the wrong semantic causes duplicate work or
missing downstream reactions.

### Example 8: Competing Consumers

Round-robin dispatch spreads queue work across available consumers. This is `co-06`.

```python
workers = ["a", "b"]  # => two consumers are eligible for the same queue
assignments = [workers[index % len(workers)] for index in range(4)]  # => dispatch alternates fairly
print(assignments)  # => Output: ['a', 'b', 'a', 'b']
```

**Key takeaway**: Consumers in one queue group share the load.

**Why it matters**: Horizontal scale comes from adding consumers without changing message producers.
Fair assignment does not create global ordering, so the next levels introduce partition keys where
per-entity ordering is a correctness requirement.

### Example 9: Queue vs Pub/Sub

The same event reaches one queue worker but all pub/sub subscribers. This joins `co-05` and `co-06`.

```python
queue_deliveries = 1  # => a competing-consumer queue selects one worker
pubsub_deliveries = 3  # => three subscriptions each observe the same fact
print(queue_deliveries, pubsub_deliveries)  # => Output: 1 3
```

**Key takeaway**: Delivery count follows topology, not the event’s name.

**Why it matters**: Choosing a queue for an audit event silently drops observations, while choosing
fanout for a side-effecting job duplicates it. Make the expected cardinality explicit in the design.

### Example 10: Event Notification

A notification carries a small identifier and asks consumers to fetch detail if needed. This is `co-03`.

```python
notification = {"order_id": "o-1", "href": "/orders/o-1"}  # => small payload, source remains authoritative
assert set(notification) == {"order_id", "href"}  # => no copied order state travels here
print(notification["order_id"])  # => Output: o-1
```

**Key takeaway**: Notifications minimize payload but add a callback dependency.

**Why it matters**: Small messages reduce schema coupling and broker cost, but a consumer now depends
on the source being reachable. That trade-off is unsuitable when independent replay or offline
processing matters.

### Example 11: Event Notification Callback

The notification receiver fetches the full resource by its stable identifier. This is `co-03`.

```python
source = {"o-1": {"total": "42"}}  # => source owns the detailed representation
detail = source["o-1"]  # => callback obtains data after receiving a thin event
print(detail["total"])  # => Output: 42
```

**Key takeaway**: A callback is part of the notification’s delivery contract.

**Why it matters**: The source can evolve internal detail without publishing every field, but delayed
or failed callbacks can make an otherwise delivered event unusable. Measure that availability
coupling before preferring this pattern.

### Example 12: Event-Carried State

State transfer places the changed fields directly in the event. This is `co-04`.

```python
event = {"order_id": "o-1", "status": "paid"}  # => the subscriber receives needed state directly
replica = {event["order_id"]: event["status"]}  # => no source callback is necessary
print(replica)  # => Output: {'o-1': 'paid'}
```

**Key takeaway**: State transfer trades a larger schema for receiver independence.

**Why it matters**: Consumers can work while the publisher is unavailable and can replay historic
events into a new projection. Producers must then evolve the event schema carefully because copied
fields become a long-lived compatibility promise.

### Example 13: Local Replica

A subscriber applies state-carrying events to its own read model. This is `co-04`.

```python
event = {"id": "o-1", "status": "paid"}  # => authoritative change supplied by the event
replica = {event["id"]: event["status"]}  # => subscriber owns a local query-friendly copy
print(replica["o-1"])  # => Output: paid
```

**Key takeaway**: A replica is derived state, not a second writer.

**Why it matters**: Local replicas remove read-time cross-service calls and enable purpose-built
queries. They may lag behind the write model, so users and API contracts must expose the expected
consistency window instead of promising an impossible instant update.

### Example 14: Notification vs State Transfer

Notifications save payload bytes; state transfer saves callback availability. This compares `co-03`
and `co-04`.

```python
notification_cost = "callback"  # => thin event shifts work to a later source request
state_transfer_cost = "schema duplication"  # => rich event duplicates data across consumers
print(notification_cost, state_transfer_cost)  # => Output: callback schema duplication
```

**Key takeaway**: Choose the dependency you can operate reliably.

**Why it matters**: There is no universal “smallest event” rule. A payment projection that must
rebuild during an outage benefits from state transfer; a rarely used audit hook may reasonably fetch
details only when it needs them.

### Example 15: In-Process Event Bus

An in-process bus is enough to expose pub/sub routing before adding a real broker. This is `co-05`.

```python
received = []  # => a test-local subscriber observation list
received.append("OrderPlaced")  # => publishing reaches the registered handler synchronously
print(received)  # => Output: ['OrderPlaced']
```

**Key takeaway**: A fake broker should preserve the invariant under test, not vendor syntax.

**Why it matters**: Deterministic local examples make failure and replay scenarios cheap to run.
They do not prove broker durability, so production validation must still exercise the chosen broker’s
acknowledgement, retention, and failure behavior.

### Example 16: Handler Registration

Subscription returns an unsubscribe action, so handlers can stop receiving facts. This is `co-05`.

```python
handlers = ["email"]  # => one handler is currently subscribed
handlers.remove("email")  # => unsubscribe changes only the subscription list
print(handlers)  # => Output: []
```

**Key takeaway**: Register and unregister at the consumer boundary.

**Why it matters**: Explicit lifecycle management prevents duplicate subscriptions during reloads and
allows a consumer to stop safely before a deployment. A publisher should remain unaware of that
operational decision.

### Example 17: Event Payload Schema

Every event needs a version so consumers can interpret its fields. This is `co-32`.

```python
event = {"version": 1, "name": "OrderPlaced"}  # => version travels with the schema instance
assert event["version"] == 1  # => consumer can select a compatible reader
print(event["version"])  # => Output: 1
```

**Key takeaway**: Version the contract, not just the producer deployment.

**Why it matters**: Producers and consumers deploy independently. Carrying an explicit schema version
makes compatibility decisions testable and lets a reader upcast historical events rather than treating
old data as an unparseable accident.

### Example 18: Event Immutability

Published facts must not change after a consumer has observed them. This is `co-01`.

```python
event = ("OrderPlaced", "o-1")  # => a tuple models an immutable published value
assert event[0] == "OrderPlaced"  # => reading does not alter the fact
print(event)  # => Output: ('OrderPlaced', 'o-1')
```

**Key takeaway**: Correct mistakes with a new compensating event, never mutation.

**Why it matters**: Mutation makes replay disagree with what earlier consumers saw. An append-only
history preserves causality, supports audit, and lets independent read models reach the same state
when they process the same sequence.

### Example 19: Multiple Handlers

Several handlers may react to one event without sharing a transaction. This is `co-05`.

```python
effects = {"email", "analytics", "billing"}  # => independent reactions to one published fact
assert len(effects) == 3  # => all three handlers have distinct responsibilities
print(sorted(effects))  # => Output: ['analytics', 'billing', 'email']
```

**Key takeaway**: Fanout coordinates observation, not a distributed transaction.

**Why it matters**: Each handler should own a small, recoverable effect. Trying to make every
subscriber succeed atomically recreates the tight coupling events were introduced to remove and
usually leads to fragile distributed commit protocols.

### Example 20: Handler Failure Isolation

One failing subscriber must not prevent other subscribers from observing the event. This is `co-05`.

```python
outcomes = ["billing:failed", "email:sent"]  # => each handler reports its own result
successful = [value for value in outcomes if value.endswith("sent")]  # => failure is isolated
print(successful)  # => Output: ['email:sent']
```

**Key takeaway**: Isolate failures, record them, and retry the failed handler deliberately.

**Why it matters**: Coupling all handlers to the slowest or broken subscriber turns asynchronous
integration back into a synchronous dependency graph. Failure isolation needs observability, because
“other handlers progressed” is not permission to lose the failed effect.

## Delivery, duplicates, and poison messages

### Example 21: At-Most-Once

At-most-once delivery can lose a message but never redelivers it. This is `co-15`.

```python
delivered = False  # => a fire-and-forget send may not reach the consumer
retries = 0  # => the sender never attempts a redelivery
print(delivered, retries)  # => Output: False 0
```

**Key takeaway**: Use at-most-once only when loss is acceptable.

**Why it matters**: Metrics, telemetry, or best-effort notifications may tolerate a lost message.
Orders, money, and entitlements normally do not, because a silent loss creates a business state that
cannot be recovered by idempotency alone.

### Example 22: At-Least-Once

At-least-once retries a message that was not acknowledged, so duplicates are possible. This is `co-16`.

```python
deliveries = ["m-1", "m-1"]  # => missing acknowledgement causes one redelivery
assert len(deliveries) == 2  # => the receiver must expect duplicates
print(deliveries)  # => Output: ['m-1', 'm-1']
```

**Key takeaway**: Default reliable delivery requires duplicate-safe consumers.

**Why it matters**: A broker cannot know whether a handler completed just before its process died.
Redelivery favors not losing the message; idempotency moves the responsibility for avoiding duplicate
effects to the consumer that owns those effects.

### Example 23: Duplicate Delivery Demo

Without idempotency, the same message applies its effect twice. This is `co-16`.

```python
balance = 0  # => the initial local effect state
for _ in ["m-1", "m-1"]: balance += 10  # => duplicate delivery repeats a non-idempotent effect
print(balance)  # => Output: 20
```

**Key takeaway**: “The broker delivered once” is not an application guarantee.

**Why it matters**: A duplicate charge, email, or stock decrement is a visible correctness bug.
Make the message identifier and an atomic processed-record check part of the consumer’s persistent
write, rather than relying on timing or an in-memory set.

### Example 24: Idempotent Consumer

An idempotent consumer records processed message ids and ignores a redelivery. This is `co-18`.

```python
processed = {"m-1"}  # => durable intent: this message already applied its effect
applied = "m-1" not in processed  # => duplicate detection gates the side effect
print(applied)  # => Output: False
```

**Key takeaway**: Deduplicate by message identity at the effect boundary.

**Why it matters**: The check and effect must commit together, otherwise a crash between them creates
either a double effect or a permanently skipped one. The full reference implementation demonstrates
the same rule through `IdempotentConsumer`.

### Example 25: Idempotent Upsert

Setting a projection row to its latest value is naturally idempotent. This is `co-18`.

```python
projection = {"o-1": "paid"}  # => first application creates the read-model row
projection["o-1"] = "paid"  # => repeating the same state does not create another row
print(len(projection))  # => Output: 1
```

**Key takeaway**: Prefer naturally idempotent state assignment where possible.

**Why it matters**: An upsert avoids a separate processed-message table for many projections, but it
does not make every operation safe. Counters, external payments, and email sends still require an
explicit identity-based deduplication strategy.

### Example 26: Idempotency Key

A stable key identifies one logical request across retries. This is `co-18`.

```python
keys = {"payment-request-7"}  # => completed logical request identities
should_process = "payment-request-7" not in keys  # => retry is rejected before side effects
print(should_process)  # => Output: False
```

**Key takeaway**: Generate the key before retries begin and carry it end to end.

**Why it matters**: A randomly generated key per retry defeats deduplication because every attempt
looks new. Stable keys let clients, relays, brokers, and consumers cooperate around one business
operation even when transport delivery is uncertain.

### Example 27: Dead-Letter Basic

A rejected message moves to a dead-letter store for inspection rather than disappearing. This is `co-29`.

```python
dead_letters = []  # => dedicated storage for messages that cannot be processed normally
dead_letters.append("bad-schema:m-1")  # => rejection preserves the original message for diagnosis
print(dead_letters)  # => Output: ['bad-schema:m-1']
```

**Key takeaway**: A DLQ is an operational workflow, not a trash can.

**Why it matters**: Keeping poison messages permits a corrected consumer or schema migration to
replay them later. It also needs alerts and ownership; a growing DLQ is evidence that a production
contract is failing.

### Example 28: Poison Retry Limit

Retry a transient failure a bounded number of times, then dead-letter it. This is `co-30`.

```python
attempts = 3  # => the message has consumed its configured retry budget
destination = "dlq" if attempts >= 3 else "retry"  # => bounded retries prevent an infinite hot loop
print(destination)  # => Output: dlq
```

**Key takeaway**: Retry policy must have a limit, delay, and terminal destination.

**Why it matters**: Infinite immediate retries amplify an outage and starve healthy work. A bounded
policy separates transient failures from poison data, while the DLQ keeps the latter observable and
recoverable instead of silently discarding it.
