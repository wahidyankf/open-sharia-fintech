---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 10
---

## Partial failure and causal time

These examples deliberately model only one failure or ordering property at a time. Treat the output
as a reason to ask a design question, not a substitute for a network or database guarantee.

### Example 1: Make the fallacies concrete

**Context**: The common network fallacies are dangerous because each looks plausible on one laptop.

```python
fallacies = {"reliable": "a packet is lost", "zero latency": "a reply is late"}
# => Each comforting assumption maps to a failure a design must tolerate.
assert all(fallacies.values())
# => A checklist has value only when every item names an observable counterexample.
```

**Key takeaway**: Begin a distributed design by listing which local assumptions fail across a network.

**Why It Matters**: Reliable, immediate, ordered communication is not the default. A concrete failure
turns a slogan into a required timeout, retry, idempotency, or user-visible failure decision.

### Example 2: Drop a message

**Context**: A channel may accept a send locally while the receiver never observes it.

```python
sent, delivered = "reserve", []
# => The sender believes it issued a command, but delivery remains a separate fact.
drop = True
# => Injecting loss models the difference without claiming a particular network cause.
if not drop:
    delivered.append(sent)
assert delivered == []
# => No arrival proves that a send result alone cannot establish remote execution.
```

**Key takeaway**: Loss means a sender needs an explicit delivery or outcome strategy.

**Why It Matters**: Retrying can improve delivery but creates duplicate risk. The next delivery
examples show why a receiver must make its own effect safe to repeat.

### Example 3: Delay and reorder messages

**Context**: Arrival order need not match send order when messages take different paths or waits.

```python
sent = ["first", "second"]
# => Sender order is a local observation only.
arrived = ["second", "first"]
# => A delayed first message permits the later message to arrive first.
assert arrived != sent
# => Any ordering guarantee must state its scope, such as one partition key.
```

**Key takeaway**: Do not infer global order from send order.

**Why It Matters**: A consumer that applies non-commutative changes needs sequence, causality, or
partition-local order. Otherwise correct-looking code can reconstruct the wrong state.

### Example 4: Show two clocks disagree

**Context**: Wall-clock timestamps cannot establish causal order when nodes drift or observe at different times.

```python
node_a_time, node_b_time = 10, 9
# => Node B can record a later real event with an earlier local wall-clock value.
assert node_b_time < node_a_time
# => Comparing these values alone would falsely order the events.
```

**Key takeaway**: Physical time is useful metadata, not universal causal proof.

**Why It Matters**: Use a logical mechanism when an application needs to reason about happened-before.
Use clock synchronization bounds only where the system can actually provide and verify them.

### Example 5: Increment a Lamport clock

**Context**: A scalar logical clock increases for every local event.

```python
clock = 0
# => The node starts with no logical history.
clock += 1
# => A local event advances the clock monotonically.
assert clock == 1
# => The value orders causal events on this node.
```

**Key takeaway**: A Lamport clock records a minimal monotonic notion of local progress.

**Why It Matters**: The clock does not claim elapsed time. Its value becomes meaningful only with
the send and receive rules that preserve the happened-before relation across nodes.

### Example 6: Advance a Lamport clock on receive

**Context**: A receiver moves past both its own time and the message timestamp.

```python
receiver_clock, message_clock = 3, 7
# => The message carries the sender's logical observation.
receiver_clock = max(receiver_clock, message_clock) + 1
# => IR2 guarantees the receive event follows the send event logically.
assert receiver_clock == 8
# => The result is greater than both previous timestamps.
```

**Key takeaway**: Receivers advance past a received logical timestamp.

**Why It Matters**: This rule gives a useful causal implication: if event A happened before B,
then A's Lamport timestamp is smaller. The reverse implication remains unsafe.

### Example 7: Break a Lamport tie deterministically

**Context**: A timestamp plus process identifier can create a repeatable total order.

```python
events = [(5, "node-b"), (5, "node-a")]
# => Two concurrent events can share a scalar timestamp.
assert sorted(events) == [(5, "node-a"), (5, "node-b")]
# => The identifier breaks a tie without claiming the events were causally ordered.
```

**Key takeaway**: A total order can be chosen without discovering real causality.

**Why It Matters**: Deterministic conflict handling is useful, but a product must not mistake the
tie-breaker for evidence that one user action truly preceded another.

### Example 8: Represent happened-before edges

**Context**: Local sequence and send-to-receive edges compose transitively.

```python
edges = {("send", "receive"), ("receive", "apply")}
# => A message edge connects histories that no wall clock can prove alone.
assert ("send", "receive") in edges and ("receive", "apply") in edges
# => Together they justify send happened-before apply by transitivity.
```

**Key takeaway**: Happened-before is a relation over events, not a timestamp comparison shortcut.

**Why It Matters**: Causal reasoning identifies which updates a reader must observe before another.
It leaves concurrent events intentionally unordered so a design can choose a merge policy.

### Example 9: Expose scalar-clock false ordering

**Context**: Concurrent events still receive scalar values that can be sorted.

```python
event_a, event_b = (4, "node-a"), (4, "node-b")
# => Neither event sent a message to the other, so they are concurrent.
assert sorted([event_a, event_b])[0] == event_a
# => The result is deterministic but not evidence that A happened before B.
```

**Key takeaway**: Lamport clocks preserve causality but cannot detect all concurrency.

**Why It Matters**: A system that needs to distinguish concurrent edits needs a richer mechanism,
such as version vectors or a domain-specific conflict rule, not merely a sortable timestamp.

### Example 10: Increment a vector clock locally

**Context**: A vector records one counter per participant.

```python
clock = {"a": 0, "b": 0}
# => Each coordinate represents one node's observed progress.
clock["a"] += 1
# => Node A advances only its own coordinate on a local event.
assert clock == {"a": 1, "b": 0}
```

**Key takeaway**: Vector coordinates preserve more causal information than one scalar.

**Why It Matters**: The extra information has cost: vector size grows with participants or requires
compression. Use it where identifying concurrency has a real conflict-resolution value.

### Example 11: Merge vector clocks on receive

**Context**: A receiver joins its knowledge with a message's knowledge, then advances locally.

```python
receiver, message = {"a": 1, "b": 2}, {"a": 3, "b": 1}
# => Each map describes causal knowledge at its event.
merged = {key: max(receiver[key], message[key]) for key in receiver}
# => Element-wise maximum dominates both observations before the next local increment.
assert merged == {"a": 3, "b": 2}
```

**Key takeaway**: Vector merge keeps the greatest known progress for every participant.

**Why It Matters**: The merge gives a later event enough information to determine whether it follows,
precedes, or is concurrent with another vector-bearing event.

### Example 12: Detect causal dominance

**Context**: One vector happened before another when every coordinate is no greater and at least one is smaller.

```python
before, after = {"a": 1, "b": 0}, {"a": 2, "b": 1}
# => `after` includes all knowledge from `before` plus later events.
dominates = all(before[k] <= after[k] for k in before) and before != after
# => Strict dominance represents a happened-before relationship.
assert dominates
```

**Key takeaway**: Vector dominance can identify causality rather than only preserve it.

**Why It Matters**: The result supports causally consistent reads and conflict detection. It still
depends on every writer carrying and merging vector metadata correctly.

### Example 13: Detect concurrent vectors

**Context**: Two vectors are concurrent when neither dominates the other.

```python
left, right = {"a": 2, "b": 0}, {"a": 1, "b": 1}
# => Each event contains progress the other did not observe.
left_before_right = all(left[k] <= right[k] for k in left)
# => The false result means left did not happen before right.
assert not left_before_right
```

**Key takeaway**: Concurrency is a real state that needs a merge or user-facing resolution choice.

**Why It Matters**: Silently selecting one concurrent value may be acceptable for a preference but
dangerous for a financial record. The domain owns that trade-off, not the clock alone.

### Example 14: Compare scalar and vector evidence

**Context**: The same two events can be ordered by a scalar tie-breaker but remain concurrent by vector.

```python
scalar_order = sorted([(2, "a"), (2, "b")])
# => A scalar tie-breaker produces an arbitrary repeatable order.
vector_a, vector_b = {"a": 1, "b": 0}, {"a": 0, "b": 1}
# => Neither vector contains the other's local event.
assert scalar_order and vector_a != vector_b
```

**Key takeaway**: Choose clock metadata for the question the application must answer.

**Why It Matters**: Scalar clocks cost little and help establish a total processing order. Vector
clocks cost more but make concurrent changes visible instead of hiding them behind a tie-breaker.

### Example 15: Buffer for causal delivery

**Context**: A consumer delays a dependent message until the message it relies on is present.

```python
applied, buffer = ["create"], ["rename"]
# => `rename` is safe only after the object exists locally.
if "create" in applied:
    applied.extend(buffer)
# => The dependency gate releases the later causal message.
assert applied == ["create", "rename"]
```

**Key takeaway**: Causal delivery may trade immediate visibility for an order a reader can understand.

**Why It Matters**: A buffer needs a policy for missing dependencies and unbounded delay. Causal
consistency is not free; the product must decide when waiting is worth the coherent history.

### Example 16: Model a strongly consistent register

**Context**: A linearizable register makes each completed write appear before a later read.

```python
register = {"value": None}
# => One authoritative state represents the model's linearization point.
register["value"] = "paid"
# => The write completes before the following read begins.
assert register["value"] == "paid"
```

**Key takeaway**: Strong consistency is an observable promise about completed operations.

**Why It Matters**: The model intentionally hides replication cost. A real system must decide how
it obtains this promise during failures, and what happens when it cannot communicate with a quorum.

### Example 17: Model eventual convergence

**Context**: Replicas may differ temporarily but should agree after propagation stops changing state.

```python
replicas = [{"value": "old"}, {"value": "new"}]
# => A write has reached one replica but not the other.
replicas[0]["value"] = replicas[1]["value"]
# => Synchronization brings the lagging replica to the later known value.
assert {replica["value"] for replica in replicas} == {"new"}
```

**Key takeaway**: Eventual consistency promises convergence, not immediate agreement.

**Why It Matters**: Readers must know which operations tolerate stale observations. A design also
needs a conflict rule when replicas accept different writes before they exchange state.

### Example 18: Preserve a causal read

**Context**: A reader that observed a creation should not later observe a dependent update without it.

```python
history = ["create order", "mark order paid"]
# => The payment event causally depends on the prior creation event.
assert history.index("create order") < history.index("mark order paid")
# => A causally consistent view keeps this relationship visible.
```

**Key takeaway**: Causal consistency preserves effects after their causes for an observer.

**Why It Matters**: The guarantee can be cheaper than global linearizability while still preventing
confusing user journeys. It does not impose one order on unrelated concurrent actions.

### Example 19: Choose under a partition

**Context**: When replicas cannot communicate, an operation cannot promise both consistent agreement and availability.

```python
partitioned, choice = True, "consistency"
# => The operation names the guarantee it keeps while the network is split.
result = "reject" if partitioned and choice == "consistency" else "accept"
# => A CP choice gives a visible unavailable result instead of a potentially divergent write.
assert result == "reject"
```

**Key takeaway**: CAP is a per-operation failure behavior choice, not a product label.

**Why It Matters**: The alternative can be valid for a different operation. State the behavior in
the API and recovery design so callers do not discover it only during an incident.

### Example 20: Make CP unavailability explicit

**Context**: A CP register refuses a write when it cannot establish the required agreement.

```python
quorum_available = False
# => The partition prevents confirmation from enough replicas.
accepted = quorum_available
# => Refusal preserves the consistency claim instead of accepting a possibly conflicting write.
assert not accepted
```

**Key takeaway**: Consistency during a partition can require an unavailable operation.

**Why It Matters**: The client needs a clear retry or pending state. Hiding the refusal behind a
timeout makes it impossible to distinguish “not applied” from “outcome unknown.”

### Example 21: Make AP divergence explicit

**Context**: An AP register accepts writes on reachable replicas even though values can differ temporarily.

```python
replica_a, replica_b = "A", "B"
# => A partition permits both sides to accept a local write.
assert replica_a != replica_b
# => Availability is preserved while the system carries a conflict or stale state.
```

**Key takeaway**: Availability under a partition requires a later convergence rule.

**Why It Matters**: A user-visible conflict can be preferable to rejecting a non-critical change.
The application must say whether it uses last-writer-wins, a mergeable datatype, or human resolution.

### Example 22: State the PACELC normal-path trade-off

**Context**: Even when there is no partition, a reader may choose low latency or fresher agreement.

```python
near_replica_value, leader_value = "stale", "fresh"
# => A local replica answers quickly but has not received the leader's latest update.
fast_read = near_replica_value
# => The low-latency choice is intentionally allowed to return a stale value.
assert fast_read == "stale"
```

**Key takeaway**: The “else” in PACELC is a normal-path product trade-off.

**Why It Matters**: The choice belongs in operation semantics. A product catalog can tolerate
staleness differently from a balance confirmation even if both use the same replication topology.

### Example 23: Deliver at most once

**Context**: Fire-and-forget gives up retries when the message is lost.

```python
lossy_send_succeeds, received = False, []
# => The sender does not retry after the channel drops its only attempt.
if lossy_send_succeeds:
    received.append("charge")
assert received == []
# => The receiver observes zero deliveries, never a duplicate.
```

**Key takeaway**: At-most-once can lose work.

**Why It Matters**: This can be acceptable for a replaceable metric but not for a critical command.
The guarantee is defined by the effect a consumer observes, not a producer's optimistic log line.

### Example 24: Deliver at least once

**Context**: Retrying after an uncertain acknowledgement can produce duplicates.

```python
deliveries = ["reserve", "reserve"]
# => The producer retries because it cannot tell whether the first delivery was processed.
assert len(deliveries) == 2
# => The receiver must be prepared to see the same logical message more than once.
```

**Key takeaway**: At-least-once favors eventual delivery over single delivery.

**Why It Matters**: Retries are not a complete reliability strategy. A duplicate charge or decrement
is a correctness defect unless the consumer or downstream operation makes the effect idempotent.

### Example 25: Deduplicate at the receiver

**Context**: A receiver records message identity before applying its effect.

```python
seen, applied = set(), []
# => Stored identity is the receiver's memory of completed effects.
for message_id in ["m-1", "m-1"]:
    if message_id not in seen:
        seen.add(message_id); applied.append(message_id)  # => Only the first delivery changes state.
assert applied == ["m-1"]
```

**Key takeaway**: Idempotency makes repeated delivery safe for a defined effect.

**Why It Matters**: The deduplication record needs an appropriate lifetime and transactional boundary.
If it is written separately from the effect, a crash can still create an uncertain partial outcome.

### Example 26: Achieve an effectively-once effect

**Context**: At-least-once delivery plus an idempotent receiver can produce one net application effect.

```python
attempts, balance, processed = ["m-1", "m-1"], 0, set()
# => Transport repeats are expected rather than treated as an exceptional surprise.
for message_id in attempts:
    if message_id not in processed:
        processed.add(message_id); balance += 10  # => The business effect runs once for this identity.
assert balance == 10
```

**Key takeaway**: “Exactly once” is often an end-to-end effect built from retries and idempotency.

**Why It Matters**: State the boundary honestly. A deduplicated local effect does not prove that an
unrelated external provider also performed its work once unless its contract participates in the design.
