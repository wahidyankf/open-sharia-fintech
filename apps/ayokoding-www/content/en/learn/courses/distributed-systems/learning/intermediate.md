---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 20
---

## Replication, quorums, and detection

These simulations make replication behavior visible before introducing consensus. They do not model
durable storage or a real transport; each example identifies the property its model can support.

### Example 27: Replicate from a leader

**Context**: A leader accepts a write and sends the resulting log entry to followers.

```python
leader, followers = ["set:x=1"], [[], []]
# => The leader establishes one ordered source of writes in this simplified model.
for follower in followers:
    follower.extend(leader)  # => Followers apply the leader entry in leader order.
assert all(follower == leader for follower in followers)
```

**Key takeaway**: Leader-follower replication separates write authority from copied state.

**Why It Matters**: A follower can lag, so the system must state whether a read may observe stale
state or must consult a sufficiently current replica before answering.

### Example 28: Read from a lagging follower

**Context**: A follower can serve an earlier value before it applies the newest leader entry.

```python
leader, follower = "paid", "pending"
# => Replication has not yet delivered the leader's newest update.
assert follower != leader
# => A follower read is fast but stale until the lag closes.
```

**Key takeaway**: A follower read needs an explicit freshness contract.

**Why It Matters**: Hiding replica lag behind a normal read creates surprising user behavior. A
system may route the operation to the leader, wait for a read index, or document bounded staleness.

### Example 29: Write to reachable leaderless replicas

**Context**: A leaderless client contacts replicas directly rather than one write authority.

```python
replicas = [{}, {}, {}]
# => Each reachable replica independently receives the client request.
for replica in replicas:
    replica["x"] = 1  # => All currently reachable replicas store the same write.
assert all(replica["x"] == 1 for replica in replicas)
```

**Key takeaway**: Leaderless replication needs a read, write, and conflict policy.

**Why It Matters**: A direct write can continue when one replica is unavailable, but concurrent
writes and stale replicas must be reconciled by versioning, read repair, or a mergeable datatype.

### Example 30: Require a write quorum

**Context**: A client succeeds only after enough replicas acknowledge a write.

```python
acks, required = 1, 2
# => Only one of the configured replicas confirmed the write.
accepted = acks >= required
# => The write fails its quorum contract rather than reporting a durable success.
assert not accepted
```

**Key takeaway**: A write quorum makes the durability and availability trade-off explicit.

**Why It Matters**: The response must say whether the outcome is definitely not applied or merely
unknown after a timeout. That distinction determines whether a caller may retry safely.

### Example 31: Require a read quorum

**Context**: A read can demand responses from enough replicas before selecting a value.

```python
responses, required = ["new"], 2
# => One response cannot meet a two-replica read policy.
accepted = len(responses) >= required
# => The reader does not pretend it met a stronger freshness guarantee.
assert not accepted
```

**Key takeaway**: Read quorum size affects both latency and confidence in observed state.

**Why It Matters**: The design needs a selection rule after gathering responses: highest version,
merge function, or an error on conflict. The quorum count alone does not resolve divergent values.

### Example 32: Use quorum intersection

**Context**: With R + W > N, every successful read and write share at least one replica.

```python
n, read_quorum, write_quorum = 3, 2, 2
# => The combined quorum size is larger than the replica set.
assert read_quorum + write_quorum > n
# => At least one reader response can include a completed writer's state.
```

**Key takeaway**: Quorum intersection is a mathematical property, not a promise of zero failure modes.

**Why It Matters**: The guarantee also depends on versions and correct replica behavior. A reader
must recognize the latest response, and a partition can still make the requested quorum unavailable.

### Example 33: Demonstrate a sub-quorum stale read

**Context**: When R + W is not greater than N, a reader can select only replicas that missed a write.

```python
n, read_quorum, write_quorum = 3, 1, 1
# => The read and write may choose disjoint single replicas.
assert read_quorum + write_quorum <= n
# => A stale read is permitted by this deliberately weak quorum configuration.
```

**Key takeaway**: Smaller quorums buy availability and latency by allowing weaker observations.

**Why It Matters**: This can be a sound choice for non-critical data, but the product must expose
that a just-completed write might not be visible from every read path immediately.

### Example 34: Repair during a read

**Context**: A reader that sees a fresher value can update a lagging replica.

```python
fresh, stale = {"v": 2}, {"v": 1}
# => The read discovers inconsistent replica versions.
stale.update(fresh)
# => Read repair makes the observed stale replica converge as a side effect.
assert stale["v"] == 2
```

**Key takeaway**: Read repair uses an observation to reduce future divergence.

**Why It Matters**: A repair must use a conflict-aware version rule; blindly copying the most recent
arrival can destroy a concurrent value that needs a merge or a user-visible resolution.

### Example 35: Resolve by last writer wins

**Context**: A last-writer-wins register selects the value carrying the greater comparison timestamp.

```python
left, right = (5, "left"), (7, "right")
# => The pair includes an ordering key and a payload.
winner = max(left, right)
# => The later comparison key wins even if the writes were concurrent in reality.
assert winner == right
```

**Key takeaway**: LWW is simple conflict resolution that can discard a concurrent update.

**Why It Matters**: Use it only where losing one simultaneous value is acceptable. A shared note,
inventory count, or money movement usually needs a mergeable operation or a human resolution path.

### Example 36: Flag a version-vector conflict

**Context**: Incomparable version vectors indicate concurrent writes rather than one update replacing another.

```python
left, right = {"a": 2, "b": 0}, {"a": 1, "b": 1}
# => Each write contains progress the other did not observe.
comparable = all(left[k] <= right[k] for k in left) or all(right[k] <= left[k] for k in left)
# => Neither dominates, so a conflict policy must run.
assert not comparable
```

**Key takeaway**: A version vector preserves a conflict instead of hiding it behind an arbitrary order.

**Why It Matters**: Conflict detection is not resolution. The domain still needs to merge values,
surface both choices, or reject an update whose invariants cannot be reconciled automatically.

### Example 37: Suspect after missed heartbeats

**Context**: A simple detector marks a peer suspect after a configured number of missing heartbeats.

```python
missed, threshold = 3, 3
# => The detector has evidence of silence but not proof of failure.
suspect = missed >= threshold
# => The result is a suspicion used for a policy, not a declaration of physical death.
assert suspect
```

**Key takeaway**: Failure detection converts silence into a time-bounded operational judgment.

**Why It Matters**: The threshold changes false-positive and slow-recovery behavior. A system must
make its response safe when a slow node later resumes and still believes it can act.

### Example 38: Tune a timeout too aggressively

**Context**: A live node can look failed when an occasional delay exceeds a short threshold.

```python
observed_delay_ms, timeout_ms = 120, 100
# => The response arrives, but after the detector's chosen limit.
suspect = observed_delay_ms > timeout_ms
# => This is a false suspicion, not evidence that the peer crashed.
assert suspect
```

**Key takeaway**: Timeout tuning trades rapid detection against false-positive risk.

**Why It Matters**: A false suspicion can trigger duplicate leaders, unnecessary failover, or data
movement. Measure realistic tail latency and design fencing before treating a timeout as authority.

### Example 39: Raise phi as silence grows

**Context**: A phi-accrual detector expresses suspicion continuously rather than with one binary state.

```python
elapsed, expected_interval = 30, 10
# => More missed expected intervals should produce more suspicion.
phi = elapsed / expected_interval
# => This simplified value rises smoothly; production detectors use a statistical distribution.
assert phi == 3
```

**Key takeaway**: A continuous suspicion score lets consumers choose thresholds for their own risk.

**Why It Matters**: The score is not a universal truth. A latency-sensitive cache and a consensus
member can choose different actions at different phi values based on their safety requirements.

### Example 40: Apply the same command log

**Context**: Replicas reach the same state when they apply the same deterministic commands in the same order.

```python
log, state_a, state_b = [1, 2, 3], 0, 0
# => The command log is the shared source of ordered state changes.
for command in log:
    state_a += command; state_b += command  # => Both state machines apply identical transitions.
assert state_a == state_b == 6
```

**Key takeaway**: Replicated state machines require the same ordered commands and deterministic application.

**Why It Matters**: A hidden clock, random choice, or external read inside a command handler breaks
the property. Keep such inputs in the replicated command or outside the deterministic state transition.

### Example 41: Check deterministic replay

**Context**: Replaying one log from the same initial state must produce the same result.

```python
log = ["+1", "+2"]
# => The log contains fully specified state transitions.
apply = lambda commands: sum(int(command) for command in [item.replace("+", "") for item in commands])
# => A deterministic function has no hidden time, random value, or external read.
assert apply(log) == apply(log)
```

**Key takeaway**: Determinism is a correctness requirement for replicated state machines.

**Why It Matters**: Replication cannot repair two nodes that make different choices for the same
command. Make nondeterministic inputs explicit in the command or resolve them before replication.

### Example 42: Keep a command log append-only

**Context**: Consensus logs preserve history by adding entries rather than overwriting positions.

```python
log = ["set:x=1"]
# => A committed command has a stable position in the history.
log.append("set:x=2")
# => Later state derives from a new entry, preserving the prior transition.
assert log == ["set:x=1", "set:x=2"]
```

**Key takeaway**: An ordered append-only log lets replicas reconstruct state consistently.

**Why It Matters**: Real consensus protocols must also handle uncommitted conflicting suffixes. The
append-only model describes committed history, not permission to ignore leader terms or quorum rules.

### Example 43: Replicate a leader log

**Context**: A follower should receive the leader's entries in order and track its matching prefix.

```python
leader_log, follower_log = ["a", "b"], ["a"]
# => The follower acknowledges only the prefix it has applied.
follower_log.append(leader_log[1])
# => Sending the next entry extends the matching prefix.
assert follower_log == leader_log
```

**Key takeaway**: Log replication is agreement about an ordered history, not just copying a final value.

**Why It Matters**: The protocol needs term and index checks so an old leader cannot overwrite a
newer history. Raft examples later make those checks part of the replication contract.

### Example 44: Reject a log-matching violation

**Context**: Two entries with the same index and term must have identical prior history.

```python
left, right = [(1, "a"), (2, "b")], [(1, "a"), (2, "c")]
# => The same logical position contains two different commands.
matching = left == right
# => The mismatch must be reconciled before replicas can claim one shared log.
assert not matching
```

**Key takeaway**: Log matching prevents replicas from silently treating incompatible histories as one.

**Why It Matters**: A leader-change protocol needs a safe rule for selecting and repairing the
authoritative suffix. Copying the most recent arrival has no consensus safety meaning.

### Example 45: Illustrate FLP non-termination

**Context**: In a fully asynchronous model, a process cannot know whether missing input means delay or failure.

```python
message_arrived = False
# => The model provides no time bound that turns silence into proof.
decision = "wait" if not message_arrived else "decide"
# => Waiting preserves safety but can continue forever.
assert decision == "wait"
```

**Key takeaway**: FLP limits guaranteed termination under full asynchrony and a failure.

**Why It Matters**: It does not say consensus is useless. Real systems add timing assumptions or
failure detectors and then state the liveness conditions under which they expect to make progress.

### Example 46: Add a failure-detector assumption

**Context**: A timeout provides an operational assumption that can let a protocol make a decision.

```python
missed, threshold = 4, 3
# => The detector acts after bounded silence according to an explicit policy.
replace_peer = missed >= threshold
# => The decision relies on an assumption that can be wrong, so fencing remains necessary.
assert replace_peer
```

**Key takeaway**: Failure detectors trade perfect knowledge for progress under stated assumptions.

**Why It Matters**: A protocol gains liveness only because it accepts possible false suspicion. The
surrounding system must prevent a delayed old member from retaining unsafe authority.

### Example 47: Coordinate a two-phase commit

**Context**: A coordinator asks every participant to prepare before issuing one commit decision.

```python
votes = ["yes", "yes"]
# => Each participant has durably promised it can commit.
decision = "commit" if all(vote == "yes" for vote in votes) else "abort"
# => The coordinator makes one all-or-nothing outcome while it remains available.
assert decision == "commit"
```

**Key takeaway**: Two-phase commit coordinates one distributed transaction decision.

**Why It Matters**: Prepared participants can be blocked if the coordinator fails before the
decision. Do not use the happy path to imply 2PC remains available during coordinator loss.

### Example 48: Show two-phase commit blocking

**Context**: Participants that voted yes cannot safely choose a result after a coordinator crash.

```python
prepared, coordinator_alive = True, False
# => The participant holds resources while awaiting the unique transaction decision.
state = "blocked" if prepared and not coordinator_alive else "finished"
# => Neither commit nor abort is safe without recovering the decision.
assert state == "blocked"
```

**Key takeaway**: Two-phase commit can preserve atomicity by sacrificing availability.

**Why It Matters**: Blocking is a design cost that can exhaust locks and capacity. Prefer local
transactions plus compensation when the workflow can tolerate eventual completion and explicit repair.

### Example 49: State three-phase commit's assumption

**Context**: A pre-commit stage can enable progress only when timing assumptions bound communication.

```python
synchronous_network, precommitted = True, True
# => The protocol's progress argument depends on the synchrony premise.
can_finish = synchronous_network and precommitted
# => A partition invalidates the premise; this is not a general partition-tolerant solution.
assert can_finish
```

**Key takeaway**: Three-phase commit avoids some blocking only under stronger timing assumptions.

**Why It Matters**: A design must not present 3PC as a free upgrade from 2PC. Its liveness claim
changes when real network delay becomes indistinguishable from a lost peer.

### Example 50: Elect by highest live identifier

**Context**: The bully algorithm selects the highest identifier among responding nodes.

```python
live = [1, 3, 2]
# => Every participant uses the same deterministic ordering rule.
leader = max(live)
# => The highest responding identifier wins this simplified election.
assert leader == 3
```

**Key takeaway**: Election algorithms need membership and failure assumptions as well as a winner rule.

**Why It Matters**: A node can be alive but unreachable from part of the network. A safe leader
protocol needs quorum or fencing; “highest id” alone does not prevent split brain.

### Example 51: Circulate a ring election token

**Context**: A ring can collect candidate identifiers and announce the maximum around the topology.

```python
ring, token = [2, 1, 3], []
# => Each participant contributes its identifier as the token circulates.
token.extend(ring)
# => A completed pass includes each reachable member once.
assert max(token) == 3
```

**Key takeaway**: Ring election trades direct fanout for an ordered membership traversal.

**Why It Matters**: The model assumes a connected ring and known membership. Production membership
changes and partitions require stronger coordination than a list traversal can express.

### Example 52: Reconcile with anti-entropy

**Context**: Two replicas exchange state and merge the missing information.

```python
left, right = {"a", "b"}, {"b", "c"}
# => Each replica has observations the other lacks.
merged = left | right
# => Set union is commutative and makes both replicas converge after exchange.
assert merged == {"a", "b", "c"}
```

**Key takeaway**: Anti-entropy repeatedly exchanges state until replicas converge.

**Why It Matters**: The merge function must be safe for reordering and repetition. Arbitrary
business updates may need versions, causal context, or a different coordination strategy.

### Example 53: Spread a rumor epidemically

**Context**: Gossip disseminates an update by repeatedly sharing it with peers.

```python
informed = {"a"}
# => One node starts with the update.
informed.update({"b", "c", "d"})
# => A completed simulation round reaches each peer in this small topology.
assert informed == {"a", "b", "c", "d"}
```

**Key takeaway**: Gossip favors scalable, eventually widespread dissemination over immediate certainty.

**Why It Matters**: Real gossip uses probabilistic rounds, duplicate suppression, and failure
handling. Readers should model convergence time and loss tolerance rather than assume instant broadcast.

### Example 54: Expire a lease

**Context**: A lease gives a lock holder authority only until a specified expiry.

```python
now, expires_at = 11, 10
# => The holder's authority ended before this attempted action.
valid = now < expires_at
# => A resource must reject a write from an expired holder.
assert not valid
```

**Key takeaway**: A lease is time-bounded authority, not proof that one client stopped acting.

**Why It Matters**: A paused client can resume after its lease ends. The resource needs a fencing
token to reject stale operations even when the client still believes it owns the lock.
