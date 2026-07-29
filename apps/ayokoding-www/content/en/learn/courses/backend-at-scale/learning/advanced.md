---
title: "Advanced Examples"
date: 2026-07-29T00:00:00+07:00
draft: false
weight: 30
---

Examples 57-80 cover queues, messaging, and resilience: at-least-once delivery, idempotent consumers, dead-letter queues, backpressure via a bounded queue, the dual-write problem and the transactional outbox (sent iff the transaction commits), an idempotent outbox relay, HMAC-signed webhooks (send, verify, retry), WebSocket echo vs SSE streaming, a broker pub/sub backplane for fanout, the circuit breaker, retry exponential backoff and full jitter, timeout guards and bulkhead isolation, connection pooling and the N+1 query, Pact consumer-driven contracts, testcontainers, and a closing scale-ready-service assembly. Every example is complete, self-contained, originally-authored standard-library Python. Run each with `python3 example.py`; every printed line below is a real captured run.

---

### Example 57: Queue -- Produce a Job, Consume It Once

_ex-57 &middot; exercises co-28_

A simple in-process queue: a producer enqueues a job, a worker consumes it and acks. The job runs exactly once in the happy path -- setting up the at-least-once failure mode of Example 58.

**`learning/code/ex-57-queue-produce-consume/example.py`**

```python
# pyright: strict
"""Example 57: Queue -- produce a job, consume it once. (co-28)

A simple in-process queue: a producer enqueues a job, a worker consumes it
and acks. The job runs exactly once in the happy path. This sets up the
at-least-once redelivery failure mode of Example 58.
"""

from collections import deque  # => deque: a simple FIFO queue
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-28: one unit of background work
class Job:
    id: int  # => the job's id
    payload: str  # => what the worker should do


@dataclass  # => co-28: a tiny broker + worker
class Queue:
    pending: deque[Job] = field(default_factory=deque[Job])  # => jobs waiting to be consumed
    processed: list[int] = field(default_factory=list[int])  # => ids of jobs the worker acked

    def produce(self, job: Job) -> None:  # => enqueue a job
        self.pending.append(job)  # => FIFO: to the back

    def consume_once(self) -> int | None:  # => the worker pulls ONE job and acks it
        if not self.pending:  # => nothing to do
            return None  # => idle
        job = self.pending.popleft()  # => pull the front job
        self.processed.append(job.id)  # => co-28: the ACK -- records this job as done
        return job.id  # => the job that ran


q = Queue()  # => co-28: one queue + worker
q.produce(Job(1, "send email"))  # => enqueue job 1
q.produce(Job(2, "resize image"))  # => enqueue job 2
print(f"pending before consume: {[j.id for j in q.pending]}")  # => Output: [1, 2]

ran = q.consume_once()  # => co-28: the worker runs job 1 and acks it
print(f"ran job: {ran}, processed: {q.processed}")  # => Output: 1, [1]
print(f"pending after one consume: {[j.id for j in q.pending]}")  # => Output: [2]

assert ran == 1 and q.processed == [1]  # => co-28: the job ran exactly once (happy path)
```

**Run**: `python3 example.py`

**Output**:

```text
pending before consume: [1, 2]
ran job: 1, processed: [1]
pending after one consume: [2]
```

**Key takeaway**: In the happy path a job is produced, consumed, and acked exactly once.

**Why it matters**: This is the baseline against which at-least-once redelivery (next) is measured.

---

### Example 58: At-Least-Once Delivery -- a Failed Ack Triggers Redelivery

_ex-58 &middot; exercises co-28_

At-least-once means the broker REDELIVERS a message if the consumer does not ack. Here the worker CRASHES before acking, so the broker redelivers the SAME message.

**`learning/code/ex-58-at-least-once-redeliver/example.py`**

```python
# pyright: strict
"""Example 58: At-least-once delivery -- a failed ack triggers redelivery. (co-28)

At-least-once means the broker REDELIVERS a message if the consumer does not
ack. Here the worker CRASHES before acking (simulated), so the broker puts
the message BACK on the queue for redelivery. The consumer can therefore see
the same message more than once.
"""

from collections import deque  # => deque: a simple FIFO queue
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-28: one message on the queue
class Message:
    id: int  # => the message id
    body: str  # => the payload


@dataclass  # => co-28: a broker that redelivers unacked messages
class Queue:
    ready: deque[Message] = field(default_factory=deque[Message])  # => messages waiting to be delivered
    in_flight: list[Message] = field(default_factory=list[Message])  # => delivered but not yet acked
    acked: list[int] = field(default_factory=list[int])  # => ids the consumer acknowledged
    redeliveries: list[int] = field(default_factory=list[int])  # => ids that were redelivered

    def enqueue(self, msg: Message) -> None:  # => add a message to the ready queue
        self.ready.append(msg)  # => to the back

    def deliver(self) -> Message | None:  # => hand one message to the consumer (in-flight)
        if not self.ready:  # => nothing ready
            return None  # => idle
        msg = self.ready.popleft()  # => take the front message
        self.in_flight.append(msg)  # => mark it in-flight (not yet acked)
        return msg  # => the delivered message

    def ack(self, msg_id: int) -> None:  # => the consumer confirms processing
        self.in_flight = [m for m in self.in_flight if m.id != msg_id]  # => remove from in-flight
        self.acked.append(msg_id)  # => recorded as done

    def redeliver_unacked(self) -> list[int]:  # => co-28: re-queue every in-flight message NOT yet acked
        redelivered: list[int] = []  # => ids that will be sent again
        still_in_flight: list[Message] = []  # => messages that survive (already acked, kept aside)
        for msg in self.in_flight:  # => inspect every in-flight message
            if msg.id in self.acked:  # => was acked -> drop it (do not redeliver)
                continue  # => already done
            self.ready.append(msg)  # => co-28: NOT acked -> put it BACK on the ready queue
            redelivered.append(msg.id)  # => record the redelivery
        self.in_flight = still_in_flight  # => clear in-flight (acked ones are dropped)
        return redelivered  # => the ids the consumer will see AGAIN


q = Queue()  # => co-28: one broker
q.enqueue(Message(1, "send email"))  # => add message 1 to the ready queue
delivered = q.deliver()  # => hand message 1 to the consumer (in-flight, NOT acked)
assert delivered is not None  # => type-narrow
print(f"delivered message: id={delivered.id}, acked: {q.acked}")  # => Output: id=1, acked=[]

# The consumer CRASHES before acking message 1 -> the broker redelivers it.
redelivered = q.redeliver_unacked()  # => co-28: message 1 was never acked -> put back on the ready queue
print(f"redelivered (crash before ack): {redelivered}")  # => Output: [1]

# Now the consumer acks on the second delivery -> no further redelivery.
again = q.deliver()  # => redelivered message 1 handed over again
assert again is not None  # => type-narrow
q.ack(1)  # => the consumer succeeds the second time
final = q.redeliver_unacked()  # => nothing unacked remains
print(f"redelivered after ack: {final}")  # => Output: []

assert redelivered == [1]  # => co-28: the unacked message was redelivered
assert final == []  # => co-28: once acked, no further redelivery
```

**Run**: `python3 example.py`

**Output**:

```text
delivered message: id=1, acked: []
redelivered (crash before ack): [1]
redelivered after ack: []
```

**Key takeaway**: A crash before ack means the broker redelivers the same message -- the consumer may see it twice.

**Why it matters**: At-least-once is WHY an idempotent consumer (co-29) is mandatory, not optional.

---

### Example 59: Idempotent Consumer -- Dedup by Message Id

_ex-59 &middot; exercises co-29_

An idempotent consumer records every processed message id and DISCARDS duplicates, so a redelivery has no effect (microservices.io -- Idempotent Consumer).

**`learning/code/ex-59-idempotent-consumer-dedup/example.py`**

```python
# pyright: strict
"""Example 59: Idempotent consumer -- dedup by message id. (co-29)

At-least-once delivery (co-28) means a consumer can see the SAME message
more than once. An idempotent consumer records every processed message id
and DISCARDS duplicates, so a redelivery has no effect. Source:
microservices.io -- Idempotent Consumer.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-29: one message
class Message:
    id: str  # => the dedup key -- the same across redeliveries
    body: str  # => the payload


@dataclass  # => co-29: a consumer that remembers every id it has processed
class IdempotentConsumer:
    seen: set[str] = field(default_factory=set[str])  # => processed message ids
    applied: list[str] = field(default_factory=list[str])  # => bodies ACTUALLY applied (for inspection)

    def process(self, msg: Message) -> str:  # => returns "applied" or "duplicate (skipped)"
        if msg.id in self.seen:  # => co-29: this id was already processed -> discard the duplicate
            return "duplicate (skipped)"  # => no effect
        self.seen.add(msg.id)  # => record the id as processed
        self.applied.append(msg.body)  # => apply the side effect ONCE
        return "applied"  # => genuinely new -> applied


consumer = IdempotentConsumer()  # => co-29: remembers processed ids
msg = Message(id="msg-1", body="charge $10")  # => the original message

first = consumer.process(msg)  # => genuinely new -> applied
print(f"first delivery:  {first}, applied={consumer.applied}")  # => Output: applied, ['charge $10']

redelivery = consumer.process(msg)  # => co-29: SAME id redelivered -> discarded
print(f"redelivery:      {redelivery}, applied={consumer.applied}")  # => Output: skipped, still ['charge $10']

assert first == "applied" and redelivery == "duplicate (skipped)"  # => co-29: duplicate detected + skipped
assert consumer.applied == ["charge $10"]  # => the body was applied exactly ONCE despite two deliveries
```

**Run**: `python3 example.py`

**Output**:

```text
first delivery:  applied, applied=['charge $10']
redelivery:      duplicate (skipped), applied=['charge $10']
```

**Key takeaway**: Recording processed ids makes a duplicate delivery a no-op.

**Why it matters**: Dedup-by-id is the standard fix for at-least-once's duplicate deliveries.

---

### Example 60: Idempotent Consumer -- a Side Effect Happens Exactly Once

_ex-60 &middot; exercises co-29_

A side-effecting message (increment a balance) delivered MULTIPLE times: the idempotent consumer applies the EFFECT exactly once by deduping on the id.

**`learning/code/ex-60-idempotent-consumer-effect-once/example.py`**

```python
# pyright: strict
"""Example 60: Idempotent consumer -- a side effect happens exactly once. (co-29)

A side-effecting message (e.g. incrementing a balance) is delivered MULTIPLE
times. The idempotent consumer applies the EFFECT exactly once by deduping
on the message id, so the balance increments once despite N redeliveries.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-29: a credit message carrying an idempotent id + an amount
class Credit:
    id: str  # => the dedup key
    amount: int  # => how much to add to the balance


BALANCE = [0]  # => the side-effect target (a wallet balance)


@dataclass  # => co-29: a consumer that guards the side effect with an id set
class CreditConsumer:
    processed: set[str] = field(default_factory=set[str])  # => ids whose effect was already applied

    def apply(self, credit: Credit) -> bool:  # => returns True if the effect was applied, False if deduped
        if credit.id in self.processed:  # => co-29: duplicate -> skip the side effect
            return False  # => no balance change
        self.processed.add(credit.id)  # => record the id
        BALANCE[0] += credit.amount  # => apply the side effect ONCE
        return True  # => applied


consumer = CreditConsumer()  # => co-29: guards the balance mutation
credit = Credit(id="credit-1", amount=100)  # => the original message

# The broker delivers the SAME credit 4 times (at-least-once, retries).
results = [consumer.apply(credit) for _ in range(4)]  # => co-29: applied once, deduped 3 times
print(f"deliveries: {len(results)}, applied count: {sum(results)}")  # => Output: 4 deliveries, 1 applied
print(f"final balance: {BALANCE[0]}")  # => Output: 100 -- incremented ONCE despite 4 deliveries

assert results == [True, False, False, False]  # => co-29: effect applied exactly once
assert BALANCE[0] == 100  # => the side effect happened once, not four times
```

**Run**: `python3 example.py`

**Output**:

```text
deliveries: 4, applied count: 1
final balance: 100
```

**Key takeaway**: A side effect happens exactly once despite N redeliveries.

**Why it matters**: Effect-once is the real guarantee -- dedup is just the mechanism that delivers it.

---

### Example 61: Dead-Letter Queue -- a Poison Message Is Sidelined

_ex-61 &middot; exercises co-30_

A poison message fails every time. After it exceeds maxReceiveCount, the broker moves it to a dead-letter queue for later inspection instead of redelivering forever (AWS SQS DLQ).

**`learning/code/ex-61-dead-letter-queue/example.py`**

```python
# pyright: strict
"""Example 61: Dead-letter queue -- a poison message is sidelined. (co-30)

A poison message fails processing every time it is delivered. After it
exceeds `maxReceiveCount`, the broker moves it to a dead-letter queue (DLQ)
for later inspection, instead of redelivering it forever. Source: AWS SQS
dead-letter queues.
"""

from collections import deque  # => deque: FIFO queues for main + DLQ
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-30: one message
class Message:
    id: str  # => the message id
    poison: bool  # => True = always fails processing


@dataclass  # => co-30: a broker with a main queue, receive counters, and a DLQ
class Broker:
    main: deque[Message] = field(default_factory=deque[Message])  # => messages awaiting processing
    receive_counts: dict[str, int] = field(default_factory=dict[str, int])  # => deliveries per id
    dlq: list[str] = field(default_factory=list[str])  # => ids sidelined to the DLQ
    max_receive_count: int = 3  # => co-30: after this many failed receives, move to the DLQ
    processed: list[str] = field(default_factory=list[str])  # => ids successfully processed

    def deliver(self, msg: Message) -> None:  # => enqueue a message
        self.main.append(msg)  # => to the back of the main queue

    def process_one(self) -> str:  # => pull, attempt, and either ack / requeue / dead-letter
        if not self.main:  # => nothing to process
            return "idle"  # => no-op
        msg = self.main.popleft()  # => pull the front message
        self.receive_counts[msg.id] = self.receive_counts.get(msg.id, 0) + 1  # => count this receive
        if msg.poison and self.receive_counts[msg.id] >= self.max_receive_count:  # => co-30: exceeded the limit
            self.dlq.append(msg.id)  # => sideline to the DLQ
            return f"dead-lettered {msg.id}"  # => removed from circulation
        if msg.poison:  # => co-30: failed but under the limit -> redeliver
            self.main.append(msg)  # => re-queue for another attempt
            return f"failed {msg.id} (receive {self.receive_counts[msg.id]})"  # => will retry
        self.processed.append(msg.id)  # => good message -> acked
        return f"processed {msg.id}"  # => success


b = Broker()  # => co-30: maxReceiveCount=3
b.deliver(Message("good-1", poison=False))  # => a healthy message
b.deliver(Message("poison-9", poison=True))  # => a poison message

log = [b.process_one() for _ in range(6)]  # => drain the queue (good succeeds, poison retries then DLQs)
for line in log:  # => print each processing step
    print(line)  # => Output: processed good-1, then poison retries, then dead-lettered
print(f"DLQ: {b.dlq}, processed: {b.processed}")  # => Output: poison-9 sidelined, good-1 done

assert "poison-9" in b.dlq and "good-1" in b.processed  # => co-30: poison dead-lettered, good processed
assert b.receive_counts["poison-9"] == b.max_receive_count  # => co-30: dead-lettered exactly at the limit
```

**Run**: `python3 example.py`

**Output**:

```text
processed good-1
failed poison-9 (receive 1)
failed poison-9 (receive 2)
dead-lettered poison-9
idle
idle
DLQ: ['poison-9'], processed: ['good-1']
```

**Key takeaway**: A poison message is dead-lettered after maxReceiveCount instead of looping forever.

**Why it matters**: A DLQ stops one bad message from blocking the whole queue.

---

### Example 62: Backpressure -- a Bounded Queue Blocks the Producer

_ex-62 &middot; exercises co-31_

A bounded queue caps in-flight work so a fast producer cannot overwhelm a slow consumer. When the queue is FULL, the producer is REJECTED rather than piling up unbounded work.

**`learning/code/ex-62-backpressure-bounded-queue/example.py`**

```python
# pyright: strict
"""Example 62: Backpressure -- a bounded queue blocks the producer. (co-31)

A bounded queue caps in-flight work so a fast producer cannot overwhelm a
slow consumer. When the queue is FULL, the producer is REJECTED (or would
block) rather than piling up unbounded work. This is backpressure -- bounding
load at the source.
"""

from collections import deque  # => deque: a bounded FIFO queue
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-31: a bounded queue + a slow consumer
class BoundedQueue:
    capacity: int  # => the max items allowed in-flight
    queue: deque[int] = field(default_factory=deque[int])  # => the bounded buffer
    rejected: list[int] = field(default_factory=list[int])  # => items turned away when full
    processed: list[int] = field(default_factory=list[int])  # => items the consumer finished

    def try_produce(self, item: int) -> bool:  # => co-31: enqueue only if room remains
        if len(self.queue) >= self.capacity:  # => co-31: FULL -> reject (backpressure on the producer)
            self.rejected.append(item)  # => record the rejected item
            return False  # => producer must slow down / retry
        self.queue.append(item)  # => enqueued
        return True  # => accepted

    def consume_one(self) -> int | None:  # => the slow consumer finishes one item
        if not self.queue:  # => nothing in-flight
            return None  # => idle
        item = self.queue.popleft()  # => take the front item
        self.processed.append(item)  # => finished
        return item  # => the item consumed


q = BoundedQueue(capacity=2)  # => co-31: only 2 items may be in-flight at once

# A fast producer floods 4 items; only 2 fit, 2 are rejected (backpressure).
produced = [q.try_produce(i) for i in range(1, 5)]  # => items 1,2 accepted; 3,4 rejected
print(f"produced results: {produced}")  # => Output: [True, True, False, False]
print(f"rejected (backpressure): {q.rejected}")  # => Output: [3, 4]
print(f"in-flight: {list(q.queue)}")  # => Output: [1, 2]

# The consumer drains one item, freeing a slot -- the producer may now retry one.
q.consume_one()  # => item 1 finished -> a slot opens
retry = q.try_produce(3)  # => co-31: now there is room -> accepted
print(f"retry item 3 after a slot freed: {retry}, in-flight: {list(q.queue)}")  # => Output: True, [2, 3]

assert produced == [True, True, False, False]  # => co-31: the producer was rejected when full
assert retry is True  # => co-31: backpressure lifts once a slot frees
```

**Run**: `python3 example.py`

**Output**:

```text
produced results: [True, True, False, False]
rejected (backpressure): [3, 4]
in-flight: [1, 2]
retry item 3 after a slot freed: True, in-flight: [2, 3]
```

**Key takeaway**: When the bounded queue is full, the producer is rejected -- backpressure at the source.

**Why it matters**: Backpressure bounds load at the source instead of letting a queue grow unbounded.

---

### Example 63: The Dual-Write Problem -- a Crash Loses the Message

_ex-63 &middot; exercises co-12_

Writing to a DB AND a broker cannot be made atomic: if the process crashes between them, the DB write survives but the message is LOST.

**`learning/code/ex-63-dual-write-problem-demo/example.py`**

```python
# pyright: strict
"""Example 63: The dual-write problem -- a crash loses the message. (co-12)

Writing to a DB AND a broker in one step cannot be made atomic across BOTH:
if the process crashes between the DB commit and the broker publish, the DB
write survives but the message is LOST. This example demonstrates the loss.
Source: microservices.io -- the dual-write problem.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-12: a process with a DB and a broker, plus a crash switch
class Service:
    db: list[str] = field(default_factory=list[str])  # => the committed DB writes
    broker: list[str] = field(default_factory=list[str])  # => the published broker messages
    crash_before_publish: bool = False  # => co-12: simulate a crash between commit and publish

    def place_order(self, order: str) -> None:  # => the dual-write: commit to DB, then publish
        self.db.append(order)  # => WRITE 1: committed to the DB
        if self.crash_before_publish:  # => co-12: CRASH right here -- the process dies
            return  # => the DB write survived, but the publish never happened
        self.broker.append(order)  # => WRITE 2: published to the broker (skipped on crash)


happy = Service()  # => co-12: no crash
happy.place_order("order-A")  # => both writes succeed
print(f"happy path: db={happy.db}, broker={happy.broker}")  # => Output: both have order-A

crashed = Service(crash_before_publish=True)  # => co-12: crash between the two writes
crashed.place_order("order-B")  # => DB committed, then the process "died" before publishing
print(f"crash path: db={crashed.db}, broker={crashed.broker}")  # => Output: db has order-B, broker is EMPTY
print("dual-write result: order-B is committed but its event was LOST")  # => Output: the lost message

assert happy.db == ["order-A"] and happy.broker == ["order-A"]  # => happy path: both consistent
assert crashed.db == ["order-B"] and crashed.broker == []  # => co-12: the message was lost in the crash
```

**Run**: `python3 example.py`

**Output**:

```text
happy path: db=['order-A'], broker=['order-A']
crash path: db=['order-B'], broker=[]
dual-write result: order-B is committed but its event was LOST
```

**Key takeaway**: A crash between the DB commit and the broker publish loses the message.

**Why it matters**: The dual-write is the specific failure mode the transactional outbox (co-13) solves.

---

### Example 64: Transactional Outbox -- Sent Iff the Transaction Commits

_ex-64 &middot; exercises co-13_

The fix: write the outbound message into the DB AS PART OF THE SAME TRANSACTION, then a separate relay publishes it. Because the message and the business write commit together, it is 'sent if and only if the transaction commits' (microservices.io).

**`learning/code/ex-64-transactional-outbox/example.py`**

```python
# pyright: strict
"""Example 64: Transactional outbox -- sent iff the transaction commits. (co-13)

The fix for the dual-write problem (co-12): write the outbound message into
the DB AS PART OF THE SAME TRANSACTION, then a separate relay publishes it.
Because the message and the business write commit together, the message is
"sent if and only if the transaction commits." Source: microservices.io --
Transactional Outbox (Chris Richardson).
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-13: a service whose DB holds an outbox table in the same transaction
class Service:
    db: list[str] = field(default_factory=list[str])  # => committed business rows
    outbox: list[str] = field(default_factory=list[str])  # => co-13: messages staged INSIDE the same transaction
    committed: bool = False  # => whether the transaction reached commit

    def place_order(self, order: str, fail: bool = False) -> None:  # => one transaction writes business + outbox
        staged_db = order  # => the business write (staged, not yet committed)
        staged_outbox = f"event:{order}"  # => co-13: the message staged IN THE SAME transaction
        if fail:  # => a mid-transaction failure -> rollback BOTH
            self.committed = False  # => neither the business write nor the message survives
            return  # => rolled back
        self.db.append(staged_db)  # => commit the business write
        self.outbox.append(staged_outbox)  # => co-13: commit the message TOGETHER with it
        self.committed = True  # => both committed atomically


def relay_publish(service: Service) -> list[str]:  # => co-13: a SEPARATE relay publishes committed outbox rows
    if not service.committed:  # => the transaction rolled back -> nothing to publish
        return []  # => no message (sent iff committed)
    published = list(service.outbox)  # => publish every committed outbox row
    service.outbox.clear()  # => the relay marks them sent
    return published  # => the published messages


committed = Service()  # => co-13: a transaction that commits
committed.place_order("order-A")  # => business + outbox commit together
published = relay_publish(committed)  # => the relay publishes the committed message
print(f"commit path: db={committed.db}, published={published}")  # => Output: db has order-A, event published

rolled_back = Service()  # => co-13: a transaction that fails
rolled_back.place_order("order-B", fail=True)  # => rollback -- neither business write nor message survives
lost = relay_publish(rolled_back)  # => co-13: nothing to publish (the transaction rolled back)
print(f"rollback path: db={rolled_back.db}, published={lost}")  # => Output: db empty, nothing published

assert committed.db == ["order-A"] and published == ["event:order-A"]  # => commit -> message sent
assert rolled_back.db == [] and lost == []  # => co-13: rollback -> message NOT sent (atomic with the business write)
```

**Run**: `python3 example.py`

**Output**:

```text
commit path: db=['order-A'], published=['event:order-A']
rollback path: db=[], published=[]
```

**Key takeaway**: The message is staged in the same transaction as the business write -- sent iff committed.

**Why it matters**: The outbox makes 'update the DB and send a message' atomic without a distributed transaction.

---

### Example 65: Outbox Relay Is At-Least-Once; the Consumer Keeps Effects Once

_ex-65 &middot; exercises co-13, co-29_

The outbox relay publishes at-LEAST-once (it may publish twice if it crashes before marking sent). The downstream idempotent consumer keeps the effect exactly once, so a duplicate is harmless.

**`learning/code/ex-65-outbox-relay-idempotent/example.py`**

```python
# pyright: strict
"""Example 65: Outbox relay is at-least-once; the consumer keeps effects once. (co-13, co-29)

The transactional-outbox relay (co-13) publishes at-LEAST-once -- it may
publish the SAME message twice (e.g. it crashes after publishing but before
marking it sent). The downstream idempotent consumer (co-29) keeps the
effect exactly once, so a duplicate relay delivery is harmless.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-13: a relay that may redeliver, plus the outbox it drains
class Relay:
    outbox: list[str] = field(default_factory=list[str])  # => committed messages awaiting publish
    published: list[str] = field(default_factory=list[str])  # => every publish attempt (incl. duplicates)
    crash_before_marking_sent: bool = True  # => co-13: simulates a crash after publish, before marking sent

    def publish_all(self) -> list[str]:  # => co-13: at-least-once publish (may emit a message twice)
        emitted: list[str] = []  # => what was emitted this round
        for msg in list(self.outbox):  # => drain the outbox
            self.published.append(msg)  # => record the publish attempt
            emitted.append(msg)  # => emit it
        if self.crash_before_marking_sent:  # => co-13: crashed before clearing the outbox
            self.outbox = list(self.outbox)  # => outbox NOT cleared -> messages will be re-published
        else:  # => cleanly marked sent
            self.outbox.clear()  # => outbox cleared
        return emitted  # => this round's emissions


BALANCE = [0]  # => the side-effect target


@dataclass  # => co-29: an idempotent consumer guards the side effect
class WalletConsumer:
    seen: set[str] = field(default_factory=set[str])  # => processed message ids

    def apply(self, msg_id: str, amount: int) -> str:  # => returns "applied" or "duplicate"
        if msg_id in self.seen:  # => co-29: duplicate -> skip
            return "duplicate"  # => no effect
        self.seen.add(msg_id)  # => record the id
        BALANCE[0] += amount  # => apply ONCE
        return "applied"  # => applied


relay = Relay(outbox=["credit:100"])  # => co-13: one committed message in the outbox
consumer = WalletConsumer()  # => co-29: guards the balance

round1 = relay.publish_all()  # => co-13: publishes, then "crashes" before marking sent
for m in round1:  # => consumer handles round 1
    consumer.apply(m, 100)  # => applied once
print(f"round 1 published: {round1}, balance: {BALANCE[0]}")  # => Output: ['credit:100'], 100

relay.crash_before_marking_sent = False  # => co-13: next round marks sent cleanly
round2 = relay.publish_all()  # => co-13: the SAME message redelivered (at-least-once)
for m in round2:  # => consumer handles round 2
    result = consumer.apply(m, 100)  # => co-29: duplicate -> skipped
    print(f"  redelivered {m}: {result}")  # => Output: duplicate
print(f"round 2 published: {round2}, balance: {BALANCE[0]}")  # => Output: redelivered, balance still 100

assert relay.published.count("credit:100") == 2  # => co-13: the relay published twice (at-least-once)
assert BALANCE[0] == 100  # => co-29: the consumer applied the effect exactly ONCE
```

**Run**: `python3 example.py`

**Output**:

```text
round 1 published: ['credit:100'], balance: 100
  redelivered credit:100: duplicate
round 2 published: ['credit:100'], balance: 100
```

**Key takeaway**: A duplicate relay delivery is harmless because the idempotent consumer dedups it.

**Why it matters**: At-least-once relay + idempotent consumer is the standard reliable-messaging pair.

---

### Example 66: Webhook -- Send with an HMAC-SHA256 Signature

_ex-66 &middot; exercises co-32_

An outbound webhook is signed with HMAC-SHA256 over the payload (Stripe-style Stripe-Signature), so the receiver can prove the payload came from a party that knows the secret.

**`learning/code/ex-66-webhook-send-hmac/example.py`**

```python
# pyright: strict
"""Example 66: Webhook -- send with an HMAC-SHA256 signature. (co-32)

An outbound webhook is signed with HMAC-SHA256 over the payload using a
shared secret, so the receiver can prove the payload came from a party that
knows the secret (authentication layered on top of HTTPS transport security).
This example models Stripe's `Stripe-Signature` header shape.
"""

import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 computation
import json  # => stdlib: serialize the payload to bytes

SECRET = b"whsec-shared-secret"  # => the shared secret (in production, loaded from env)


def sign(timestamp: str, payload: bytes) -> str:  # => co-32: Stripe-style signature
    signed_payload = f"{timestamp}.".encode() + payload  # => t=<ts> + "." + payload
    digest = hmac.new(SECRET, signed_payload, hashlib.sha256).hexdigest()  # => HMAC-SHA256
    return f"t={timestamp},v1={digest}"  # => co-32: the Stripe-Signature header value


def send_webhook(event: dict[str, str]) -> tuple[bytes, str]:  # => returns (payload bytes, signature header)
    payload = json.dumps(event).encode()  # => the canonical payload bytes
    timestamp = "1700000000"  # => a fixed timestamp for this demo (Stripe includes a real ts for replay protection)
    signature = sign(timestamp, payload)  # => co-32: sign over timestamp.payload
    return payload, signature  # => the POST body + the Stripe-Signature header


payload, signature = send_webhook({"event": "order.shipped", "order_id": "42"})  # => send one webhook
print(f"payload: {payload.decode()}")  # => Output: the JSON body
print(f"Stripe-Signature: {signature[:48]}...")  # => Output: a prefix of the header (t=...,v1=...)

# Recompute independently to prove the signature matches the payload (a receiver would do this).
ts = signature.split(",")[0].split("=")[1]  # => extract the timestamp
expected = sign(ts, payload)  # => co-32: recompute over the SAME timestamp.payload
matches = hmac.compare_digest(expected, signature)  # => constant-time compare
print(f"signature matches payload: {matches}")  # => Output: True

assert matches is True  # => co-32: the signature verifies against the payload it covers
```

**Run**: `python3 example.py`

**Output**:

```text
payload: {"event": "order.shipped", "order_id": "42"}
Stripe-Signature: t=1700000000,v1=7c5ddc46bddf414b633863bc24c48abe...
signature matches payload: True
```

**Key takeaway**: The signature is HMAC-SHA256 over timestamp.payload -- authentication layered on top of HTTPS.

**Why it matters**: HTTPS protects the transport; an HMAC authenticates the sender -- two different guarantees.

---

### Example 67: Webhook -- Verify an Incoming Signature

_ex-67 &middot; exercises co-32_

The receiver recomputes the HMAC and compares it in CONSTANT TIME (hmac.compare_digest). A tampered body produces a different digest and is rejected (GitHub X-Hub-Signature-256).

**`learning/code/ex-67-webhook-verify-signature/example.py`**

```python
# pyright: strict
"""Example 67: Webhook -- verify an incoming signature. (co-32)

The receiver recomputes the HMAC over the received timestamp.payload and
compares it to the header's signature in CONSTANT TIME (hmac.compare_digest).
A tampered body produces a different digest -> rejected. Source: GitHub
X-Hub-Signature-256 validating deliveries (HMAC-SHA256, constant-time).
"""

import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 + constant-time compare

SECRET = b"whsec-shared-secret"  # => the shared secret the sender and receiver share
TOLERANCE_SECONDS = 300  # => reject signatures older than this (replay protection), via a fixed clock here


def sign(timestamp: str, payload: bytes) -> str:  # => the sender's signature function (reused)
    signed = f"{timestamp}.".encode() + payload  # => timestamp.payload
    return hmac.new(SECRET, signed, hashlib.sha256).hexdigest()  # => the v1 digest


def verify(timestamp: str, payload: bytes, v1: str) -> bool:  # => co-32: the receiver's verification
    expected = sign(timestamp, payload)  # => recompute over the received timestamp.payload
    return hmac.compare_digest(expected, v1)  # => co-32: CONSTANT-TIME compare (avoids timing oracles)


payload = b'{"event":"order.shipped"}'  # => a genuine payload
timestamp = "1700000000"  # => the sender's timestamp
good_signature = sign(timestamp, payload)  # => the legitimate signature

valid = verify(timestamp, payload, good_signature)  # => co-32: matches -> accepted
print(f"genuine payload verifies: {valid}")  # => Output: True

tampered = verify(timestamp, b'{"event":"order.CANCELLED"}', good_signature)  # => co-32: body changed -> digest differs
print(f"tampered body verifies:   {tampered}")  # => Output: False -- rejected

bogus_sig = verify(timestamp, payload, "0" * 64)  # => a forged signature -> rejected
print(f"forged signature verifies: {bogus_sig}")  # => Output: False

assert valid is True and tampered is False and bogus_sig is False  # => co-32: only the genuine body+signature passes
```

**Run**: `python3 example.py`

**Output**:

```text
genuine payload verifies: True
tampered body verifies:   False
forged signature verifies: False
```

**Key takeaway**: Verification recomputes the HMAC and compares in constant time -- a tampered body is rejected.

**Why it matters**: Constant-time comparison avoids a timing oracle that would leak the secret.

---

### Example 68: Webhook -- Retry a Failed Delivery with Backoff

_ex-68 &middot; exercises co-32, co-38_

A failed webhook delivery (non-2xx) is retried with exponential backoff so successive attempts SPACE OUT rather than hammering a struggling receiver.

**`learning/code/ex-68-webhook-retry/example.py`**

```python
# pyright: strict
"""Example 68: Webhook -- retry a failed delivery with backoff. (co-32, co-38)

A webhook delivery that fails (the receiver returns non-2xx) is retried with
exponential backoff so successive attempts SPACE OUT rather than hammering an
already-struggling receiver. This example prints the deterministic attempt
schedule (no real sleeping). co-38 names the backoff discipline.
"""

from dataclasses import dataclass  # => a small typed record for one attempt


def backoff_delay(attempt: int, base_seconds: int = 2, cap_seconds: int = 3600) -> int:
    # => co-38: exponential backoff, capped: base * 2^(attempt-1), capped at `cap`
    return min(cap_seconds, base_seconds * (2 ** (attempt - 1)))  # => 2, 4, 8, 16, ... capped


@dataclass  # => co-32/co-38: one delivery attempt and the delay before it
class Attempt:
    number: int  # => 1-based attempt number
    status: int  # => the receiver's HTTP status (non-2xx = retry)
    delay_after: int  # => co-38: seconds to wait before the NEXT attempt


def deliver_with_retries(receiver_statuses: list[int]) -> list[Attempt]:  # => simulate N attempts
    attempts: list[Attempt] = []  # => the recorded schedule
    for number, status in enumerate(receiver_statuses, start=1):  # => one status per attempt
        delay = backoff_delay(number) if not (200 <= status < 300) else 0  # => co-38: backoff only on failure
        attempts.append(Attempt(number=number, status=status, delay_after=delay))  # => record it
        if 200 <= status < 300:  # => success -> stop retrying
            break  # => delivered
    return attempts  # => the full schedule


# The receiver fails 3 times (500), then succeeds (200). Delays space out: 2, 4, 8, then 0.
attempts = deliver_with_retries([500, 500, 500, 200])  # => co-38: 4 attempts total
for a in attempts:  # => print the schedule
    print(f"attempt {a.number}: status={a.status}, wait before next={a.delay_after}s")  # => Output: spaced delays

delays = [a.delay_after for a in attempts]  # => co-38: the backoff schedule
print(f"backoff schedule (s): {delays}")  # => Output: [2, 4, 8, 0]

assert delays == [2, 4, 8, 0]  # => co-38: delays double across failed attempts; 0 once it succeeds
assert attempts[-1].status == 200  # => co-32: eventually delivered
```

**Run**: `python3 example.py`

**Output**:

```text
attempt 1: status=500, wait before next=2s
attempt 2: status=500, wait before next=4s
attempt 3: status=500, wait before next=8s
attempt 4: status=200, wait before next=0s
backoff schedule (s): [2, 4, 8, 0]
```

**Key takeaway**: Failed deliveries are retried with doubling delays -- they space out.

**Why it matters**: Backoff (co-38) applied to outbound webhooks prevents retry storms against the receiver.

---

### Example 69: WebSocket Echo -- a Bidirectional Round-Trip

_ex-69 &middot; exercises co-33_

WebSocket is a full-duplex, bidirectional protocol over ONE TCP connection (RFC 6455). This example simulates a single persistent connection where the client sends and the server echoes back over the SAME channel.

**`learning/code/ex-69-websocket-echo/example.py`**

```python
# pyright: strict
"""Example 69: WebSocket echo -- a bidirectional round-trip. (co-33)

WebSocket is a full-duplex, bidirectional protocol over ONE TCP connection
(RFC 6455, 2011). This example simulates a single persistent connection where
the client sends a frame and the server echoes it back over the SAME channel.
"""

from collections import deque  # => deque: the bidirectional channel's two directions
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-33: one message frame on the connection
class Frame:
    payload: str  # => the frame's content


@dataclass  # => co-33: a full-duplex connection with a client->server and server->client direction
class WebSocket:
    to_server: deque[Frame] = field(default_factory=deque[Frame])  # => client -> server frames
    to_client: deque[Frame] = field(default_factory=deque[Frame])  # => server -> client frames

    def client_send(self, frame: Frame) -> None:  # => client writes to the connection
        self.to_server.append(frame)  # => one direction

    def server_echo(self) -> None:  # => co-33: the server reads a frame and echoes it back over the SAME connection
        if self.to_server:  # => a frame is waiting
            frame = self.to_server.popleft()  # => read the client's frame
            self.to_client.append(Frame(payload=frame.payload))  # => co-33: echo back the OTHER direction

    def client_recv(self) -> Frame | None:  # => client reads the server's response
        if not self.to_client:  # => nothing echoed back yet
            return None  # => idle
        return self.to_client.popleft()  # => the echoed frame


ws = WebSocket()  # => co-33: ONE persistent, bidirectional connection
ws.client_send(Frame("ping"))  # => client -> server
ws.server_echo()  # => co-33: server echoes back over the same connection
echoed = ws.client_recv()  # => server -> client
assert echoed is not None  # => type-narrow
print(f"client sent:    'ping'")  # => Output: the sent frame
print(f"server echoed:  {echoed.payload!r}")  # => Output: the echoed frame (bidirectional round-trip)

assert echoed.payload == "ping"  # => co-33: a bidirectional round-trip over one connection
```

**Run**: `python3 example.py`

**Output**:

```text
client sent:    'ping'
server echoed:  'ping'
```

**Key takeaway**: WebSocket is full-duplex over one connection -- the client sends and receives on the same channel.

**Why it matters**: Full-duplex matters when the client also needs to push to the server (not just receive).

---

### Example 70: SSE -- a One-Way Server->Client Event Stream

_ex-70 &middot; exercises co-33_

Server-Sent Events is a one-way server->client push over plain HTTP: the server writes text/event-stream frames (id + data) and the client receives them in order (WHATWG HTML Living Standard).

**`learning/code/ex-70-sse-stream/example.py`**

```python
# pyright: strict
"""Example 70: SSE -- a one-way server->client event stream. (co-33)

Server-Sent Events (SSE) is a one-way server->client push over a plain HTTP
connection: the server writes `text/event-stream` frames (id + data) and the
client receives them in order. Part of the WHATWG HTML Living Standard.
"""

from collections import deque  # => deque: the one-way server->client channel
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-33: one SSE event (an id + a data line)
class Event:
    id: int  # => the event id (lets the client resume with Last-Event-ID)
    data: str  # => the event payload


@dataclass  # => co-33: a one-way SSE stream (server pushes, client only receives)
class SSEStream:
    buffer: deque[Event] = field(default_factory=deque[Event])  # => events the server has pushed

    def push(self, data: str) -> Event:  # => the server pushes an event (client cannot push back)
        event_id = (self.buffer[-1].id + 1) if self.buffer else 1  # => monotonic ids
        event = Event(id=event_id, data=data)  # => build the event
        self.buffer.append(event)  # => co-33: server -> client, one direction only
        return event  # => the pushed event

    def client_recv(self) -> Event | None:  # => the client reads the next event in order
        if not self.buffer:  # => nothing pushed yet
            return None  # => idle
        return self.buffer.popleft()  # => the next event, in order


stream = SSEStream()  # => co-33: a one-way text/event-stream
stream.push("tick")  # => server pushes event 1
stream.push("tock")  # => server pushes event 2
stream.push("boom")  # => server pushes event 3

received = [stream.client_recv() for _ in range(3)]  # => client drains them in order
for ev in received:  # => print each as it arrived
    assert ev is not None  # => type-narrow
    print(f"received event id={ev.id}: {ev.data!r}")  # => Output: tick, tock, boom in order

assert [ev.data for ev in received if ev is not None] == ["tick", "tock", "boom"]  # => co-33: one-way, in order
```

**Run**: `python3 example.py`

**Output**:

```text
received event id=1: 'tick'
received event id=2: 'tock'
received event id=3: 'boom'
```

**Key takeaway**: SSE is one-way server->client push -- simpler than WebSocket when the client only listens.

**Why it matters**: SSE's simplicity (plain HTTP, auto-reconnect) wins when the client never needs to push back.

---

### Example 71: Broker Backplane -- Fanout Across Two App Nodes

_ex-71 &middot; exercises co-34_

WebSocket/SSE connections are STICKY to one node. Broadcasting to clients on DIFFERENT nodes requires a shared pub/sub BACKPLANE: a node publishes once, the backplane fans it out to every node.

**`learning/code/ex-71-broker-backplane-fanout/example.py`**

```python
# pyright: strict
"""Example 71: Broker backplane -- fanout across two app nodes. (co-34)

WebSocket/SSE connections are STICKY to the one node that accepted them.
Broadcasting an event to clients connected to DIFFERENT nodes requires a
shared pub/sub BACKPLANE: a node publishes once, the backplane fans the
message out to every node, and each node delivers to its own sticky clients.
Source: Socket.IO Redis adapter (relies on Redis Pub/Sub).
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-34: one app node holding its own sticky client connections
class AppNode:
    name: str  # => the node's label
    clients: list[str] = field(default_factory=list[str])  # => sticky clients connected to THIS node
    delivered: list[str] = field(default_factory=list[str])  # => messages this node delivered locally

    def deliver(self, message: str) -> list[str]:  # => push a message to THIS node's own sticky clients
        recipients = list(self.clients)  # => the local clients
        self.delivered.append(message)  # => record local delivery
        return recipients  # => who got it on this node


@dataclass  # => co-34: the shared pub/sub backplane that fans messages across nodes
class Backplane:
    nodes: list[AppNode] = field(default_factory=list[AppNode])  # => every node subscribed to the backplane

    def register(self, node: AppNode) -> None:  # => a node joins the backplane
        self.nodes.append(node)  # => subscribed

    def broadcast(self, message: str) -> dict[str, list[str]]:  # => co-34: publish once -> fan out to every node
        reached: dict[str, list[str]] = {}  # => node -> its local recipients
        for node in self.nodes:  # => every node gets the message via the backplane
            reached[node.name] = node.deliver(message)  # => each node delivers to its OWN sticky clients
        return reached  # => who received the message, per node


backplane = Backplane()  # => co-34: the shared pub/sub backplane
node_a = AppNode("A", clients=["client-1", "client-2"])  # => node A holds 2 sticky clients
node_b = AppNode("B", clients=["client-3"])  # => node B holds 1 sticky client
backplane.register(node_a)  # => A joins the backplane
backplane.register(node_b)  # => B joins the backplane

reached = backplane.broadcast("hello")  # => co-34: one broadcast -> clients on BOTH nodes receive it
print(f"broadcast reached: {reached}")  # => Output: A->[client-1,client-2], B->[client-3]

all_clients = reached["A"] + reached["B"]  # => every client across both nodes
print(f"all clients that received 'hello': {all_clients}")  # => Output: all 3 clients

assert all_clients == ["client-1", "client-2", "client-3"]  # => co-34: the backplane fanned out to both nodes
```

**Run**: `python3 example.py`

**Output**:

```text
broadcast reached: {'A': ['client-1', 'client-2'], 'B': ['client-3']}
all clients that received 'hello': ['client-1', 'client-2', 'client-3']
```

**Key takeaway**: A shared pub/sub backplane fans one broadcast out to clients on every node.

**Why it matters**: Without a backplane, a broadcast only reaches clients on the originating node.

---

### Example 72: Circuit Breaker -- Trip Open, Fail Fast, Half-Open

_ex-72 &middot; exercises co-37_

A circuit breaker wraps a protected call. Once failures reach a threshold, the breaker TRIPS OPEN and subsequent calls FAIL FAST. After a cooldown, a HALF-OPEN probe allows one trial; success closes it (Nygard, Release It!).

**`learning/code/ex-72-circuit-breaker/example.py`**

```python
# pyright: strict
"""Example 72: Circuit breaker -- trip open, then fail fast, then half-open. (co-37)

A circuit breaker wraps a protected call. Once failures reach a threshold,
the breaker TRIPS OPEN and subsequent calls FAIL FAST (no real call is made)
instead of piling onto a failing dependency. After a cooldown, a HALF-OPEN
probe allows one trial; success closes the breaker. Popularized by Nygard's
Release It! (Fowler, CircuitBreaker).
"""

from dataclasses import dataclass  # => a small typed record for the breaker's state


class CallFailed(Exception):  # => stands in for a real dependency error
    pass


@dataclass  # => co-37: the breaker's mutable state
class CircuitBreaker:
    failure_threshold: int  # => consecutive failures that trip the breaker OPEN
    failures: int = 0  # => current consecutive failure count
    state: str = "closed"  # => "closed" | "open" | "half-open"

    def call(self, fn_succeeds: bool) -> str:  # => invoke the protected call (or fail fast)
        if self.state == "open":  # => co-37: OPEN -> fail fast, no real call
            return "fail-fast (open)"  # => the breaker short-circuits
        if self.state == "half-open":  # => co-37: HALF-OPEN -> exactly one probe
            if fn_succeeds:  # => the probe succeeded
                self.state = "closed"  # => close the breaker
                self.failures = 0  # => reset the failure count
                return "recovered (closed)"  # => healthy again
            self.state = "open"  # => the probe failed -> re-open
            return "fail-fast (re-opened)"  # => still broken
        # => state == "closed": make the real call
        if fn_succeeds:  # => success
            self.failures = 0  # => reset
            return "ok (closed)"  # => healthy
        self.failures += 1  # => count the failure
        if self.failures >= self.failure_threshold:  # => co-37: threshold reached -> TRIP OPEN
            self.state = "open"  # => trip
        return f"failed ({self.state})"  # => the call failed

    def cooldown(self) -> None:  # => move an OPEN breaker to HALF-OPEN for a probe
        if self.state == "open":  # => only after a cooldown
            self.state = "half-open"  # => allow one trial


breaker = CircuitBreaker(failure_threshold=3)  # => co-37: trip after 3 consecutive failures

# Three failures trip the breaker OPEN.
print(breaker.call(False))  # => failed (closed) -- failure 1
print(breaker.call(False))  # => failed (closed) -- failure 2
print(breaker.call(False))  # => co-37: failed (open) -- failure 3 trips it
print(breaker.call(True))  # => co-37: fail-fast (open) -- no real call made while open

breaker.cooldown()  # => move to half-open for one probe
print(breaker.call(True))  # => co-37: recovered (closed) -- the probe succeeded, breaker closed

assert breaker.state == "closed"  # => co-37: the breaker recovered via a half-open probe
```

**Run**: `python3 example.py`

**Output**:

```text
failed (closed)
failed (closed)
failed (open)
fail-fast (open)
recovered (closed)
```

**Key takeaway**: Open -> fail fast; half-open -> one probe; a successful probe closes the breaker.

**Why it matters**: A breaker stops cascading failure by failing fast while a dependency is down.

---

### Example 73: Retry with Exponential Backoff

_ex-73 &middot; exercises co-38_

Retrying with exponential backoff DOUBLES the wait between attempts (base \* 2^attempt). The delays space out -- but plain backoff clusters retries when many clients fail at once (the flaw Example 74 fixes).

**`learning/code/ex-73-retry-exponential-backoff/example.py`**

```python
# pyright: strict
"""Example 73: Retry with exponential backoff. (co-38)

Retrying a transient failure with exponential backoff DOUBLES the wait
between attempts (base * 2^attempt). The delays space out -- but plain
backoff CLUSTERS retries when many clients fail at once (the flaw Example 74
fixes with jitter). Delays are computed, not slept, so output is deterministic.
"""

from dataclasses import dataclass  # => a small typed record for the schedule


def backoff_delay(attempt: int, base_seconds: float = 1.0, cap_seconds: float = 32.0) -> float:
    # => co-38: exponential backoff: base * 2^(attempt-1), capped at `cap`
    return min(cap_seconds, base_seconds * (2 ** (attempt - 1)))  # => 1, 2, 4, 8, 16, 32, 32, ...


@dataclass  # => co-38: one attempt's wait before the next retry
class ScheduledWait:
    attempt: int  # => 1-based attempt number
    wait_before_next: float  # => seconds waited BEFORE the next attempt


def schedule(max_attempts: int) -> list[ScheduledWait]:  # => compute the full backoff schedule
    return [ScheduledWait(attempt=n, wait_before_next=backoff_delay(n)) for n in range(1, max_attempts + 1)]  # => co-38


plan = schedule(max_attempts=6)  # => co-38: a 6-attempt schedule
for step in plan:  # => print each step
    print(f"attempt {step.attempt}: wait before next = {step.wait_before_next}s")  # => Output: doubling waits

waits = [step.wait_before_next for step in plan]  # => co-38: the delay sequence
print(f"delays: {waits}")  # => Output: [1, 2, 4, 8, 16, 32]

assert waits == [1, 2, 4, 8, 16, 32]  # => co-38: each delay doubles, capped at 32
```

**Run**: `python3 example.py`

**Output**:

```text
attempt 1: wait before next = 1.0s
attempt 2: wait before next = 2.0s
attempt 3: wait before next = 4.0s
attempt 4: wait before next = 8.0s
attempt 5: wait before next = 16.0s
attempt 6: wait before next = 32.0s
delays: [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
```

**Key takeaway**: Exponential backoff doubles the wait each attempt -- but plain backoff clusters retries.

**Why it matters**: Plain backoff's clustering is the flaw full jitter (next) exists to fix.

---

### Example 74: Retry with Full Jitter

_ex-74 &middot; exercises co-38_

Full Jitter replaces the capped delay with a UNIFORM random value in [0, capped delay]: sleep = random(0, min(cap, base\*2^attempt)). Clients de-synchronize, avoiding synchronized retry storms (AWS, Marc Brooker 2015).

**`learning/code/ex-74-retry-full-jitter/example.py`**

```python
# pyright: strict
"""Example 74: Retry with FULL JITTER. (co-38)

Plain exponential backoff clusters retries: when many clients fail at once,
they all retry at base*2^n together, producing synchronized retry storms. FULL
JITTER replaces the capped delay with a UNIFORM random value in [0, capped
delay]: sleep = random(0, min(cap, base*2^attempt)). Clients de-synchronize.
Source: AWS "Exponential Backoff and Jitter" (Marc Brooker, 2015). A FIXED
SEED makes the output deterministic for this example.
"""

import random  # => stdlib: uniform random for full jitter
from dataclasses import dataclass  # => a small typed record for one client's schedule


def full_jitter_delay(attempt: int, base_seconds: float = 1.0, cap_seconds: float = 32.0, rng: random.Random | None = None) -> float:
    # => co-38: Full Jitter: sleep = random(0, min(cap, base*2^(attempt-1)))
    bound = min(cap_seconds, base_seconds * (2 ** (attempt - 1)))  # => the capped exponential ceiling
    engine = rng if rng is not None else random.Random(0)  # => a seeded RNG for deterministic output
    return engine.uniform(0, bound)  # => a uniform random value in [0, bound]


@dataclass  # => co-38: one client's full-jitter retry schedule
class ClientSchedule:
    client: str  # => the client label
    delays: list[float]  # => this client's de-synchronized delay sequence


def schedule_for(client: str, attempts: int, seed: int) -> ClientSchedule:  # => one client's seeded schedule
    rng = random.Random(seed)  # => co-38: a distinct seed per client -> distinct (de-synchronized) delays
    delays = [full_jitter_delay(n, rng=rng) for n in range(1, attempts + 1)]  # => jittered delays
    return ClientSchedule(client=client, delays=delays)  # => the schedule


# Two clients failing at the SAME time get DIFFERENT retry schedules -> no synchronized storm.
client_a = schedule_for("A", attempts=4, seed=1)  # => co-38: seed 1
client_b = schedule_for("B", attempts=4, seed=2)  # => co-38: seed 2
print(f"client A delays: {[round(d, 2) for d in client_a.delays]}")  # => Output: jittered, distinct
print(f"client B delays: {[round(d, 2) for d in client_b.delays]}")  # => Output: jittered, distinct

desynchronized = client_a.delays != client_b.delays  # => co-38: the two clients retry at different times
within_bounds = all(0 <= d <= min(32, 1 * 2 ** (n - 1)) for n, d in enumerate(client_a.delays, 1))  # => co-38: each in [0, bound]
print(f"clients de-synchronized: {desynchronized}")  # => Output: True
print(f"client A delays within [0, bound]: {within_bounds}")  # => Output: True

assert desynchronized  # => co-38: full jitter de-synchronizes clients
assert within_bounds  # => co-38: every delay is in [0, min(cap, base*2^(attempt-1))]
```

**Run**: `python3 example.py`

**Output**:

```text
client A delays: [0.13, 1.69, 3.06, 2.04]
client B delays: [0.96, 1.9, 0.23, 0.68]
clients de-synchronized: True
client A delays within [0, bound]: True
```

**Key takeaway**: Full jitter spreads retries uniformly in [0, capped] -- clients de-synchronize.

**Why it matters**: De-synchronization prevents a thundering herd of retries after a shared outage.

---

### Example 75: Timeout Guard -- Abort a Slow Call at a Deadline

_ex-75 &middot; exercises co-39_

A timeout caps how long a call may wait. If the operation does not finish by the deadline, it ABORTS with a timeout error rather than hanging and tying up a request thread.

**`learning/code/ex-75-timeout-guard/example.py`**

```python
# pyright: strict
"""Example 75: Timeout guard -- abort a slow call at a deadline. (co-39)

A timeout caps how long a call may wait. If the operation does not finish by
the deadline, it ABORTS with a timeout error rather than hanging indefinitely
and tying up a request thread. The "clock" is the operation's reported
duration, so the abort is deterministic.
"""

from dataclasses import dataclass  # => a small typed record for the result


class TimeoutError(Exception):  # => stands in for a deadline-exceeded error
    pass


@dataclass  # => co-39: the outcome -- either a value or a timeout
class Result:
    status: str  # => "ok" or "timeout"
    value: str = ""  # => the value on success (empty on timeout)


def call_with_timeout(op_duration: float, deadline: float) -> Result:  # => co-39: abort if op_duration exceeds deadline
    if op_duration > deadline:  # => co-39: the operation outlasted the deadline -> abort
        return Result(status="timeout")  # => aborted at the deadline (no full wait)
    return Result(status="ok", value=f"completed in {op_duration}")  # => finished within the deadline


fast = call_with_timeout(op_duration=0.2, deadline=1.0)  # => finishes well within the deadline
print(f"fast call (0.2s, deadline 1.0s): {fast.status}, {fast.value!r}")  # => Output: ok

slow = call_with_timeout(op_duration=5.0, deadline=1.0)  # => co-39: would take 5s -> aborted at the 1s deadline
print(f"slow call (5.0s, deadline 1.0s): {slow.status}")  # => Output: timeout -- aborted, did NOT wait 5s

assert fast.status == "ok" and slow.status == "timeout"  # => co-39: the deadline aborted the slow call
```

**Run**: `python3 example.py`

**Output**:

```text
fast call (0.2s, deadline 1.0s): ok, 'completed in 0.2'
slow call (5.0s, deadline 1.0s): timeout
```

**Key takeaway**: A call that outlasts its deadline is aborted -- it does not hang indefinitely.

**Why it matters**: Without timeouts, one slow dependency can tie up every request thread and sink the service.

---

### Example 76: Bulkhead -- Isolate Resource Pools

_ex-76 &middot; exercises co-39_

A bulkhead partitions resources into ISOLATED pools so a failure or saturation in one does not sink the others. When pool A is saturated, pool B still serves (Nygard, Release It!).

**`learning/code/ex-76-bulkhead-isolation/example.py`**

```python
# pyright: strict
"""Example 76: Bulkhead -- isolate resource pools. (co-39)

A bulkhead partitions resources into ISOLATED pools so a failure or saturation
in one does not sink the others. Here pool A and pool B are separate; when
pool A is fully saturated (all its permits held), pool B still serves its own
calls. The bulkhead pattern was introduced by Michael Nygard in Release It!.
"""

from dataclasses import dataclass  # => a small typed record for one isolated pool


@dataclass  # => co-39: one isolated resource pool with a fixed permit count
class Pool:
    name: str  # => the pool's label
    permits: int  # => max concurrent in-flight calls this pool allows
    in_use: int = 0  # => currently held permits
    rejected: int = 0  # => calls turned away because the pool was full

    def acquire(self) -> bool:  # => take a permit if one is available
        if self.in_use >= self.permits:  # => co-39: this pool is saturated
            self.rejected += 1  # => count the rejection
            return False  # => caller must wait/fail
        self.in_use += 1  # => hold a permit
        return True  # => acquired

    def release(self) -> None:  # => return a permit
        self.in_use = max(0, self.in_use - 1)  # => never negative


pool_a = Pool("A", permits=2)  # => co-39: pool A allows 2 concurrent calls
pool_b = Pool("B", permits=2)  # => co-39: pool B is SEPARATE -- A's saturation does not touch it

# Saturate pool A fully.
pool_a.acquire()  # => A in_use=1
pool_a.acquire()  # => A in_use=2 (now full)
a_rejected = pool_a.acquire()  # => co-39: pool A is saturated -> this call is rejected
print(f"pool A saturated, 3rd call acquired: {a_rejected}, rejected count: {pool_a.rejected}")  # => Output: False, 1

# Pool B is ISOLATED -- it still serves even though pool A is full.
b_served = pool_b.acquire()  # => co-39: pool B has its OWN permits -> unaffected by A
print(f"pool B serves while A is saturated: {b_served}")  # => Output: True

assert a_rejected is False and pool_a.rejected == 1  # => co-39: A's saturation rejected the overflow
assert b_served is True  # => co-39: the bulkhead kept B serving despite A being full
```

**Run**: `python3 example.py`

**Output**:

```text
pool A saturated, 3rd call acquired: False, rejected count: 1
pool B serves while A is saturated: True
```

**Key takeaway**: Isolated pools mean A's saturation does not starve B.

**Why it matters**: Without bulkheads, one slow downstream can consume all threads and take down unrelated features.

---

### Example 77: Connection Pool -- Reuse, Do Not Reopen

_ex-77 &middot; exercises co-40_

A connection pool keeps DB connections warm and HANDS THEM OUT on check-out, returning them on check-in so the next request REUSES an existing connection rather than paying the open cost.

**`learning/code/ex-77-connection-pool/example.py`**

```python
# pyright: strict
"""Example 77: Connection pool -- reuse, do not reopen. (co-40)

A connection pool keeps DB connections warm and HANDS THEM OUT on check-out,
returning them on check-in so the NEXT request REUSES an existing connection
rather than paying the cost of opening a new one. The open counter proves the
second request did not trigger a new open.
"""

from collections import deque  # => deque: the pool of idle, warm connections
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-40: one reusable DB connection (stands in for a real TCP/db connection)
class Connection:
    id: int  # => a label for which connection this is


@dataclass  # => co-40: a pool that opens connections lazily and reuses them
class ConnectionPool:
    max_size: int  # => the most connections the pool will ever hold
    idle: deque[Connection] = field(default_factory=deque[Connection])  # => warm, checked-in connections
    opens: int = 0  # => how many times a connection was actually OPENED (the cost we want to minimize)
    next_id = [1]  # => a mutable counter for new connection ids

    def checkout(self) -> Connection:  # => hand out a connection, opening one only if none is idle
        if self.idle:  # => a warm connection is available -> reuse it (no new open)
            return self.idle.popleft()  # => reused
        conn = Connection(id=self.next_id[0])  # => must open a new connection
        self.next_id[0] += 1  # => advance the id counter
        self.opens += 1  # => co-40: count the open (the cost a pool avoids on reuse)
        return conn  # => a freshly opened connection

    def checkin(self, conn: Connection) -> None:  # => return a connection to the pool for reuse
        self.idle.append(conn)  # => now warm and reusable


pool = ConnectionPool(max_size=5)  # => co-40: a small pool

# First request: no idle connection -> OPEN one (opens=1).
c1 = pool.checkout()  # => opens connection 1
print(f"first checkout: opens={pool.opens}, conn id={c1.id}")  # => Output: opens=1, id=1

pool.checkin(c1)  # => return it to the pool (now idle/warm)

# Second request: an idle connection exists -> REUSE it (opens stays 1, no new open).
c2 = pool.checkout()  # => co-40: reuses the warm connection -> no new open
print(f"second checkout: opens={pool.opens}, conn id={c2.id} (reused)")  # => Output: opens=1, id=1

assert pool.opens == 1  # => co-40: the second request REUSED a connection, not reopened
assert c2.id == c1.id  # => co-40: the same connection object was handed out again
```

**Run**: `python3 example.py`

**Output**:

```text
first checkout: opens=1, conn id=1
second checkout: opens=1, conn id=1 (reused)
```

**Key takeaway**: A pool reuses warm connections -- the second checkout triggers no new open.

**Why it matters**: Reusing connections avoids the handshake cost on every request.

---

### Example 78: Pact -- Consumer-Driven Contract Testing

_ex-78 &middot; exercises co-35_

In consumer-driven contract testing, the CONSUMER declares the request it sends and the response it expects; this generates a contract. The PROVIDER is verified against it (pact.io).

**`learning/code/ex-78-pact-contract/example.py`**

```python
# pyright: strict
"""Example 78: Pact -- consumer-driven contract testing. (co-35)

In consumer-driven contract testing, the CONSUMER writes a test describing
the request it sends and the response it expects; this test GENERATES a
contract. The PROVIDER is then verified against that contract. This example
models a consumer contract and verifies the provider honours it. Source:
pact.io -- "code-first consumer-driven contract testing."
"""

from dataclasses import dataclass  # => a small typed record for the contract


@dataclass  # => co-35: the consumer's declared expectation of one interaction
class Interaction:
    description: str  # => a human label for this interaction
    request: dict[str, object]  # => what the consumer sends (method + path)
    expected_response_status: int  # => the status the consumer depends on
    expected_body_fields: list[str]  # => the response fields the consumer reads


# The CONSUMER declares: "when I GET /users/1, I expect 200 with {id, name}."
CONSUMER_CONTRACT: list[Interaction] = [  # => co-35: the generated contract
    Interaction(
        description="get a user by id",
        request={"method": "GET", "path": "/users/1"},
        expected_response_status=200,
        expected_body_fields=["id", "name"],
    ),
]


def provider_handle(method: str, path: str) -> tuple[int, dict[str, object]]:  # => the PROVIDER's real handler
    if method == "GET" and path == "/users/1":  # => the route the consumer calls
        return 200, {"id": 1, "name": "ada", "email": "ada@example.com"}  # => the real response (carries an EXTRA field)
    return 404, {"error": "not found"}  # => unknown route


def verify_provider(contract: list[Interaction]) -> list[tuple[str, bool]]:  # => co-35: provider verification
    results: list[tuple[str, bool]] = []  # => per-interaction pass/fail
    for interaction in contract:  # => replay each consumer interaction against the provider
        method = str(interaction.request["method"])  # => the consumer's method
        path = str(interaction.request["path"])  # => the consumer's path
        status, body = provider_handle(method, path)  # => the provider's real response
        status_ok = status == interaction.expected_response_status  # => status matches the contract
        fields_ok = all(field in body for field in interaction.expected_body_fields)  # => required fields present
        results.append((interaction.description, status_ok and fields_ok))  # => pass/fail for this interaction
    return results  # => the verification report


report = verify_provider(CONSUMER_CONTRACT)  # => co-35: verify the provider against the consumer contract
for desc, passed in report:  # => print each interaction's result
    print(f"interaction '{desc}': {'PASS' if passed else 'FAIL'}")  # => Output: PASS

assert all(passed for _desc, passed in report)  # => co-35: the provider honours the consumer contract
```

**Run**: `python3 example.py`

**Output**:

```text
interaction 'get a user by id': PASS
```

**Key takeaway**: The consumer's expectations become a contract; provider verification checks the provider honours it.

**Why it matters**: A contract test catches provider drift that would break a consumer, without a full integration environment.

---

### Example 79: Testcontainers -- an Integration Test Against a Real Engine

_ex-79 &middot; exercises co-36_

Testcontainers spins up EPHEMERAL, lightweight container instances of real dependencies (DB, broker) for tests instead of mocks. This example simulates the lifecycle: a fresh isolated engine per test, a real query, then teardown.

**`learning/code/ex-79-testcontainers-integration/example.py`**

```python
# pyright: strict
"""Example 79: Testcontainers -- an integration test against a real engine. (co-36)

Testcontainers spins up EPHEMERAL, lightweight Docker container instances of
real dependencies (a DB, a broker) for automated tests, instead of mocks.
This example simulates the lifecycle: a fresh isolated engine instance per
test, a REAL query against it, then teardown. Source: testcontainers.com.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-36: an ephemeral containerized DB instance (stands in for a real Docker container)
class ContainerDB:
    container_id: int  # => a unique id for this ephemeral instance
    rows: dict[int, str] = field(default_factory=dict[int, str])  # => the engine's own isolated state
    running: bool = True  # => the container is up until torn down

    def query(self, key: int) -> str | None:  # => a REAL query against the (simulated) engine
        if not self.running:  # => the container was torn down
            raise RuntimeError("container stopped")  # => cannot query a stopped container
        return self.rows.get(key)  # => the engine's real answer

    def insert(self, key: int, value: str) -> None:  # => a REAL write against the engine
        if not self.running:  # => the container was torn down
            raise RuntimeError("container stopped")  # => cannot write to a stopped container
        self.rows[key] = value  # => the engine persists it

    def stop(self) -> None:  # => co-36: teardown -- the ephemeral instance is destroyed
        self.running = False  # => the container is gone (its state does not leak to the next test)


class TestcontainersFactory:  # => co-36: stands in for the testcontainers library
    def __init__(self) -> None:
        self.next_id = 1  # => unique container ids
        self.started: list[int] = []  # => ids of containers started this run

    def start_db(self) -> ContainerDB:  # => co-36: spin up a FRESH, isolated DB instance
        container = ContainerDB(container_id=self.next_id)  # => a brand-new ephemeral instance
        self.started.append(container.container_id)  # => record it
        self.next_id += 1  # => advance
        return container  # => hand the test an isolated engine


factory = TestcontainersFactory()  # => co-36: the library stand-in

# Test 1: a fresh container, real insert + real query, then teardown.
db1 = factory.start_db()  # => co-36: an isolated instance
db1.insert(1, "row-one")  # => a REAL write against the engine
read1 = db1.query(1)  # => a REAL query against the engine
db1.stop()  # => co-36: teardown -- this instance is gone
print(f"test 1 (container {db1.container_id}): wrote 'row-one', read back {read1!r}")  # => Output: real round-trip

# Test 2: a SECOND fresh container -- its state is isolated from test 1 (no leak).
db2 = factory.start_db()  # => co-36: a NEW isolated instance
leaked = db2.query(1)  # => test 1's row is NOT here -- each container starts empty
print(f"test 2 (container {db2.container_id}): test 1's row leaked? {leaked!r}")  # => Output: None (isolated)
db2.stop()  # => teardown

assert read1 == "row-one"  # => co-36: the suite ran a real query against a real engine
assert leaked is None  # => co-36: each container is ephemeral and isolated (no cross-test leak)
assert factory.started == [1, 2]  # => co-36: two distinct ephemeral containers were spun up
```

**Run**: `python3 example.py`

**Output**:

```text
test 1 (container 1): wrote 'row-one', read back 'row-one'
test 2 (container 2): test 1's row leaked? None
```

**Key takeaway**: Each test gets a fresh, isolated, REAL engine -- not a mock -- then tears it down.

**Why it matters**: A real engine catches behavior a mock would silently get wrong.

---

### Example 80: Scale-Ready Service -- the Assembled End-to-End Service

_ex-80 &middot; exercises co-06, co-17, co-21, co-29_

Assemble versioned + cursor-paginated REST, an idempotent write (Idempotency-Key), an RBAC role gate, a token-bucket rate limit returning 429+Retry-After, a cache-aside layer, and an idempotent queue consumer behind one integration check. This is the capstone-preview: every prior pattern combined.

**`learning/code/ex-80-scale-ready-service/example.py`**

```python
# pyright: strict
"""Example 80: Scale-ready service -- the assembled end-to-end service. (co-06, co-17, co-21, co-29)

Assemble versioned + cursor-paginated REST, an IDEMPOTENT write (Idempotency-
Key), an RBAC role gate, a token-bucket RATE LIMIT returning 429+Retry-After,
a CACHE-ASIDE layer, and an IDEMPOTENT QUEUE CONSUMER behind one integration
check. This is the capstone-preview assembly: every prior pattern combined in
one self-contained service that passes end to end.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => the assembled service's response shape
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object] = field(default_factory=dict[str, object])  # => resource or error payload
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => RateLimit/Retry-After headers


@dataclass  # => co-06/co-17/co-21/co-29: the assembled, scale-ready service
class ScaleReadyService:
    store: dict[int, dict[str, object]] = field(default_factory=lambda: {1: {"id": 1, "title": "seed"}})  # => the DB
    idempotency: dict[str, dict[str, object]] = field(default_factory=dict[str, dict[str, object]])  # => co-06: key -> body
    cache: dict[int, dict[str, object]] = field(default_factory=dict[int, dict[str, object]])  # => co-21: cache-aside
    roles: dict[str, str] = field(default_factory=lambda: {"tok-admin": "admin", "tok-user": "user"})  # => co-17: RBAC
    budget: list[int] = field(default_factory=lambda: [2])  # => co-19: token-bucket budget
    processed_msgs: set[str] = field(default_factory=set[str])  # => co-29: idempotent consumer dedup
    next_id: list[int] = field(default_factory=lambda: [2])  # => the next id a create mints

    def list_v1(self, after_cursor: int | None, limit: int) -> Response:  # => GET /v1/items (cursor pagination)
        ids = sorted(self.store.keys())  # => stable order
        threshold = 0 if after_cursor is None else after_cursor  # => resume point
        page_ids = [i for i in ids if i > threshold][:limit]  # => the page
        return Response(200, {"ids": page_ids, "next_cursor": page_ids[-1] if page_ids else None})  # => paginated

    def create_v1(self, token: str, idempotency_key: str, title: str) -> Response:  # => POST /v1/items
        if self.roles.get(token) != "admin":  # => co-17: RBAC -- only admin may create
            return Response(403, {"error": "forbidden"})  # => 403
        if self.budget[0] <= 0:  # => co-19: rate limit FIRST -> 429
            return Response(429, headers={"Retry-After": "60"}, body={"error": "too many requests"})  # => 429
        if idempotency_key in self.idempotency:  # => co-06: replay -> return original, no double-apply
            return Response(200, body=self.idempotency[idempotency_key])  # => 200, original body
        self.budget[0] -= 1  # => consume budget for a genuinely new write
        new_id = self.next_id[0]  # => mint an id
        item: dict[str, object] = {"id": new_id, "title": title}  # => the new resource
        self.store[new_id] = item  # => persist
        self.cache.pop(new_id, None)  # => co-21: invalidate on write
        self.idempotency[idempotency_key] = item  # => co-06: record for safe replay
        self.next_id[0] += 1  # => advance
        return Response(201, body=item)  # => 201 created

    def read_cached(self, item_id: int) -> Response:  # => GET /v1/items/{id} (cache-aside)
        if item_id in self.cache:  # => co-21: HIT
            return Response(200, body={"source": "cache", **self.cache[item_id]})  # => from cache
        value = self.store.get(item_id)  # => MISS -> DB
        if value is None:  # => not found
            return Response(404, {"error": "not found"})  # => 404
        self.cache[item_id] = value  # => co-21: populate
        return Response(200, body={"source": "db", **value})  # => from DB

    def consume_message(self, msg_id: str, body: str) -> str:  # => co-29: idempotent queue consumer
        if msg_id in self.processed_msgs:  # => duplicate -> skip
            return "skipped"  # => no effect
        self.processed_msgs.add(msg_id)  # => record
        _ = body  # => (the effect would happen here)
        return "applied"  # => applied once


svc = ScaleReadyService()  # => the assembled service
checks: list[bool] = []  # => integration check accumulators

# (1) RBAC: a non-admin is forbidden.
forbidden = svc.create_v1("tok-user", "k-1", "X")  # => co-17: 403
checks.append(forbidden.status == 403)  # => RBAC gate works
print(f"non-admin create: {forbidden.status}")  # => Output: 403

# (2) Idempotent create + replay does not double-apply; rate limit decrements.
first = svc.create_v1("tok-admin", "k-1", "First")  # => co-06: 201, budget 2->1
replay = svc.create_v1("tok-admin", "k-1", "First")  # => co-06: 200, original body, no new item
checks.append(first.status == 201 and replay.status == 200 and len(svc.store) == 2)  # => idempotency works
print(f"create {first.status}, replay {replay.status}, store size {len(svc.store)}")  # => Output: 201, 200, 2

# (3) Rate limit trips on the next genuinely-new write (budget now 0 after first).
second = svc.create_v1("tok-admin", "k-2", "Second")  # => budget 1->0, 201
third = svc.create_v1("tok-admin", "k-3", "Third")  # => co-19: budget 0 -> 429
checks.append(second.status == 201 and third.status == 429 and third.headers.get("Retry-After") == "60")  # => rate limit works
print(f"second {second.status}, third (over limit) {third.status} Retry-After={third.headers.get('Retry-After')}")  # => Output: 201, 429

# (4) Cache-aside: first read misses (db), second read hits (cache).
read1 = svc.read_cached(1)  # => co-21: MISS -> db
read2 = svc.read_cached(1)  # => co-21: HIT -> cache
checks.append(read1.body["source"] == "db" and read2.body["source"] == "cache")  # => cache works
print(f"read 1 source={read1.body['source']}, read 2 source={read2.body['source']}")  # => Output: db, cache

# (5) Idempotent consumer: a duplicate message is applied once.
a = svc.consume_message("m-1", "do work")  # => co-29: applied
b = svc.consume_message("m-1", "do work")  # => co-29: skipped
checks.append(a == "applied" and b == "skipped")  # => consumer idempotency works
print(f"consume m-1 first: {a}, redelivered: {b}")  # => Output: applied, skipped

all_pass = all(checks)  # => the integration check
print(f"END-TO-END: {'PASS' if all_pass else 'FAIL'}")  # => Output: PASS

assert all_pass  # => co-06/co-17/co-21/co-29: the assembled service passes end to end
```

**Run**: `python3 example.py`

**Output**:

```text
non-admin create: 403
create 201, replay 200, store size 2
second 201, third (over limit) 429 Retry-After=60
read 1 source=db, read 2 source=cache
consume m-1 first: applied, redelivered: skipped
END-TO-END: PASS
```

**Key takeaway**: One service combines idempotency, RBAC, rate limiting, caching, and an idempotent consumer -- and passes end to end.

**Why it matters**: This is the integration point where every prior concept must cooperate; it previews the capstone.

---

← Previous: [Intermediate Examples](./intermediate.md) · Next: [Capstone](./capstone/overview.md) →
