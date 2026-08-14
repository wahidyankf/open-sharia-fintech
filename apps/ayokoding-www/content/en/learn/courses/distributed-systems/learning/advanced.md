---
title: "Advanced Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 30
---

## Consensus and convergence

Consensus algorithms are deliberately simplified here. Each example names a safety property or
liveness condition but omits production concerns such as persistent log storage, membership changes,
and transport authentication.

### Example 55: Start a Raft election

**Context**: A follower that receives no leader heartbeat begins a new election term.

```python
role, term = "follower", 4
# => The node has observed no valid leader activity within its election timeout.
role, term = "candidate", term + 1
# => It votes for itself and requests votes for a new logical term.
assert (role, term) == ("candidate", 5)
```

**Key takeaway**: Raft makes leader election an explicit term-scoped state transition.

**Why It Matters**: The timeout only starts an election; it does not prove other nodes failed. A
majority vote and term checks prevent one isolated candidate from becoming a valid leader.

### Example 56: Advance a Raft term

**Context**: Terms are logical clocks that distinguish newer election authority from older authority.

```python
old_term, new_term = 5, 6
# => A later election uses a strictly greater term value.
assert new_term > old_term
# => Nodes reject or step down for messages carrying a valid higher term.
```

**Key takeaway**: A term orders leadership epochs, not elapsed time.

**Why It Matters**: Term comparison stops stale leaders from continuing after a newer election. The
protocol must persist term changes before responding so a restart does not forget newer authority.

### Example 57: Require a majority vote

**Context**: A candidate needs more than half of the configured voters to lead.

```python
votes, members = 2, 3
# => Two affirmative votes form a majority in a three-member configuration.
won = votes > members // 2
# => A minority candidate cannot claim leader authority.
assert won
```

**Key takeaway**: Majorities intersect, preventing two different majorities in one membership view.

**Why It Matters**: The property relies on a coherent membership configuration. Joint consensus or
another safe transition is required when the voter set itself changes.

### Example 58: Keep followers quiet with heartbeats

**Context**: A valid leader heartbeat resets a follower's election timeout.

```python
role, received_heartbeat = "follower", True
# => The follower recognizes the current term's leader activity.
start_election = role == "follower" and not received_heartbeat
# => It stays a follower instead of creating unnecessary competing terms.
assert not start_election
```

**Key takeaway**: Heartbeats provide a liveness signal for a leader term.

**Why It Matters**: Heartbeats do not prove the leader can commit writes. A client-facing linearizable
read or write still needs the protocol's quorum and log-commit evidence.

### Example 59: Append through a leader

**Context**: A Raft leader appends a client command before replicating it to followers.

```python
leader_log, follower_log = ["set:x=1"], []
# => The leader assigns the command a position in its current-term log.
follower_log.extend(leader_log)
# => A follower stores the same ordered entry when its prefix check succeeds.
assert follower_log == leader_log
```

**Key takeaway**: Raft replication shares an ordered log, not arbitrary state snapshots.

**Why It Matters**: The real append request carries prior index and term so a follower can reject a
bad prefix. That rejection is how a leader discovers and repairs divergent suffixes safely.

### Example 60: Commit after majority storage

**Context**: A leader marks an entry committed only after a majority has stored it.

```python
replicated_on, members = 2, 3
# => The leader counts durable acknowledgements for one log index.
committed = replicated_on > members // 2
# => A majority makes the entry survive the loss of any minority.
assert committed
```

**Key takeaway**: A Raft commit index advances from quorum evidence, not a leader-local append.

**Why It Matters**: Applying an uncommitted command can expose behavior that a later leader removes.
The commit rule is the line between a proposed command and replicated state-machine history.

### Example 61: Reject a conflicting Raft append

**Context**: A follower rejects an append whose claimed prior entry does not match its local log.

```python
local_prior_term, request_prior_term = 3, 2
# => The leader request describes a history inconsistent with this follower.
accepted = local_prior_term == request_prior_term
# => Rejection directs the leader to search for the shared prefix.
assert not accepted
```

**Key takeaway**: Prefix checks protect Raft's log-matching property.

**Why It Matters**: An accepting follower would permit two histories at one index. The retry process
must back up safely until it finds a matching point, then overwrite only uncommitted conflict entries.

### Example 62: Step down for a higher term

**Context**: A leader that observes a valid higher term loses its older leadership authority.

```python
role, local_term, observed_term = "leader", 4, 5
# => Another node has evidence of a newer election epoch.
if observed_term > local_term:
    role, local_term = "follower", observed_term  # => The old leader stops accepting authority.
assert (role, local_term) == ("follower", 5)
```

**Key takeaway**: Higher-term evidence fences an older Raft leader.

**Why It Matters**: Stepping down is a safety action. Client retries must locate the new leader or
receive an honest unavailable result rather than having two nodes accept conflicting writes.

### Example 63: Re-elect on the majority side

**Context**: After a partition, only the side containing a majority can elect a valid new leader.

```python
partition_size, total_members = 2, 3
# => This side contains more than half of the configured voters.
can_elect = partition_size > total_members // 2
# => The minority side cannot form a competing legitimate majority.
assert can_elect
```

**Key takeaway**: Quorum membership chooses which partition can continue consensus.

**Why It Matters**: The minority's unavailable response is the availability cost that protects one
committed history. Fencing and term checks still matter when old nodes reconnect.

### Example 64: Converge logs after healing

**Context**: A valid leader brings a previously partitioned follower to the committed prefix.

```python
leader, follower = ["a", "b", "c"], ["a"]
# => The follower retained a valid prefix but missed later committed entries.
follower[:] = leader
# => Catch-up makes the follower state-machine history match the leader's committed log.
assert follower == leader
```

**Key takeaway**: Healing a partition requires explicit replication and catch-up work.

**Why It Matters**: “The network came back” does not itself merge state. The protocol must verify
terms and prefixes before applying entries or deleting a follower's uncommitted conflicting suffix.

### Example 65: Promise in Paxos phase one

**Context**: An acceptor promises not to accept proposals numbered below the highest prepare it has seen.

```python
promised, prepare = 7, 8
# => The proposer offers a unique, higher proposal number.
accepted = prepare > promised
# => The acceptor can advance its promise and reject lower future proposals.
assert accepted
```

**Key takeaway**: Paxos phase one prevents older proposers from reviving superseded proposals.

**Why It Matters**: Acceptors also report any accepted value so the proposer can preserve safety in
phase two. Proposal numbering and durable state are integral, not incidental implementation details.

### Example 66: Accept in Paxos phase two

**Context**: After a valid promise, an acceptor can accept a proposal/value pair at that number.

```python
promised, proposal, value = 8, 8, "x"
# => The proposal meets the acceptor's highest promise.
accepted = proposal >= promised
# => The acceptor records this candidate value for the proposal number.
assert accepted and value == "x"
```

**Key takeaway**: Paxos acceptance is guarded by the promise made in phase one.

**Why It Matters**: A proposer that learns prior accepted values cannot choose an arbitrary new value.
That carry-forward rule is what keeps quorum intersections from choosing two different outcomes.

### Example 67: Preserve one chosen Paxos value

**Context**: Two intersecting majorities cannot safely choose different values for the same slot.

```python
first_quorum, second_quorum = {"a", "b"}, {"b", "c"}
# => Acceptor b belongs to both majorities and carries prior acceptance information.
assert first_quorum & second_quorum == {"b"}
# => Intersection forces a later proposer to preserve a previously chosen value.
```

**Key takeaway**: Quorum intersection is the core safety reason only one value becomes chosen.

**Why It Matters**: This is a safety property, not a promise that a proposer will finish. Liveness
still needs proposer coordination, stable leadership, or retries under a practical timing assumption.

### Example 68: State consensus safety

**Context**: A consensus implementation must never report two different chosen values for one decision.

```python
chosen_values = {"approve"}
# => All successful decision paths have recorded the same result.
assert len(chosen_values) == 1
# => A second distinct value would violate the fundamental safety invariant.
```

**Key takeaway**: Consensus safety means agreement even when progress is delayed.

**Why It Matters**: A system may correctly prefer waiting to disagreeing. Product and operational
design must accept that safety can surface as timeout or unavailability rather than instant completion.

### Example 69: Merge a CRDT G-counter

**Context**: Each node owns one nondecreasing counter component; replicas merge by component maximum.

```python
left, right = {"a": 2, "b": 0}, {"a": 1, "b": 3}
# => Each replica has independently observed increments.
merged = {node: max(left[node], right[node]) for node in left}
# => Component-wise maximum is commutative and preserves both nodes' progress.
assert sum(merged.values()) == 5
```

**Key takeaway**: A G-counter converges without coordinating concurrent increments.

**Why It Matters**: The datatype only supports growth. Do not force a business rule needing decrements,
limits, or one-time reservation into a G-counter just because it merges conveniently.

### Example 70: Compose a PN-counter

**Context**: A PN-counter represents increments and decrements as two grow-only counters.

```python
increments, decrements = {"a": 5}, {"a": 2}
# => Each component grows even though the derived value can decrease.
value = sum(increments.values()) - sum(decrements.values())
# => The visible counter is the difference of two convergent G-counters.
assert value == 3
```

**Key takeaway**: Decrement support can preserve CRDT convergence by changing the representation.

**Why It Matters**: A PN-counter does not enforce a nonnegative business invariant during concurrent
updates. Use coordination if overselling or overdrawing is unacceptable at the operation boundary.

### Example 71: Merge a grow-only set

**Context**: A G-set adds elements and merges replicas by set union.

```python
left, right = {"a", "b"}, {"b", "c"}
# => Both replicas may add independently without a shared leader.
merged = left | right
# => Union is associative, commutative, and idempotent.
assert merged == {"a", "b", "c"}
```

**Key takeaway**: A G-set converges because additions never need to be undone.

**Why It Matters**: Removal changes the problem. Use an observed-remove set or coordination only
after defining what a concurrent add and remove should mean for the domain.

### Example 72: Merge an LWW register

**Context**: A last-writer-wins register chooses the payload with the larger supplied timestamp.

```python
left, right = (10, "blue"), (12, "teal")
# => The comparison key determines the winner, not arrival order.
assert max(left, right) == right
# => The later timestamp's payload becomes the merged visible value.
```

**Key takeaway**: LWW gives one convergent answer by discarding the other concurrent value.

**Why It Matters**: Clock skew and concurrent updates can make this choice surprising. It fits a
replaceable preference better than a value whose lost update has legal or financial consequences.

### Example 73: Check strong eventual convergence

**Context**: A CRDT merge should reach the same result regardless of replica exchange order.

```python
a, b, c = {"a"}, {"b"}, {"c"}
# => Each replica starts with one independent observation.
assert (a | b) | c == a | (b | c)
# => Associativity lets arbitrary anti-entropy schedules converge to the same set.
```

**Key takeaway**: Strong eventual consistency comes from a deterministic, convergent merge law.

**Why It Matters**: Convergence does not validate an application invariant. A datatype can merge
correctly while still allowing an unacceptable intermediate or final business state.

### Example 74: Size for Byzantine faults

**Context**: Byzantine agreement requires enough replicas to outvote up to f arbitrary faulty nodes.

```python
faults, members = 1, 4
# => The PBFT bound is N = 3f + 1 for f Byzantine faults.
assert members >= 3 * faults + 1
# => Three honest replicas can outnumber one liar under the protocol's assumptions.
```

**Key takeaway**: Byzantine tolerance assumes faults can lie, equivocate, or collude.

**Why It Matters**: Crash-fault consensus and Byzantine consensus have different cost and trust
models. Do not pay Byzantine complexity unless the threat model truly includes arbitrary replica behavior.

### Example 75: Walk PBFT vote phases

**Context**: PBFT uses pre-prepare, prepare, and commit messages to establish sufficient agreement.

```python
phases = ["pre-prepare", "prepare", "commit"]
# => Each phase gathers evidence for one ordered client request.
assert phases[-1] == "commit"
# => The simplified sequence names the protocol rounds without claiming a full implementation.
```

**Key takeaway**: Byzantine protocols use multiple authenticated voting phases to tolerate lies.

**Why It Matters**: Safety and liveness depend on quorum thresholds, authenticated messages, and
network assumptions. The list is a map for further study, not executable production consensus.

### Example 76: Compensate a saga step

**Context**: A distributed workflow reverses completed local work when a later local step fails.

```python
completed = ["reserve inventory"]
# => The first local transaction committed independently.
failed = True
# => A later payment step cannot complete the workflow.
if failed:
    completed.append("release inventory")  # => Compensation creates a new local action, not a rollback.
assert completed[-1] == "release inventory"
```

**Key takeaway**: A saga compensates with new business actions rather than one global transaction.

**Why It Matters**: Compensation can itself fail and may not perfectly erase real-world effects.
Design idempotent steps, durable progress records, and a repair path for outcomes that remain uncertain.

### Example 77: Expose split brain

**Context**: Two isolated nodes can both believe they lead if authority is not fenced by a quorum protocol.

```python
leaders = {"partition-a": "node-1", "partition-b": "node-2"}
# => Each side has a local story that names a different authority.
assert len(set(leaders.values())) == 2
# => This conflicting-leader condition threatens conflicting writes to one resource.
```

**Key takeaway**: Split brain is an authority failure, not merely a confusing monitoring state.

**Why It Matters**: A timeout-based failover needs quorum and fencing. Without a resource-side
rejection mechanism, an old but delayed leader can keep writing after a replacement becomes active.

### Example 78: Reject a stale fencing token

**Context**: A resource accepts writes only from a holder presenting a token greater than the last accepted token.

```python
last_accepted, incoming = 9, 8
# => The old holder resumed after its authority was replaced.
accepted = incoming > last_accepted
# => The resource, not the client, rejects stale authority.
assert not accepted
```

**Key takeaway**: Fencing tokens protect a resource from clients with expired or superseded leases.

**Why It Matters**: A lock service alone cannot stop a paused client from acting later. Every
protected write path must compare the token atomically with the resource's recorded highest token.

### Example 79: Wait out clock uncertainty

**Context**: A bounded-time system can wait until its uncertainty interval cannot overlap an earlier commit.

```python
now, uncertainty, prior_commit = 100, 5, 103
# => The clock reports an interval rather than pretending an instant is exact.
safe_to_ack = now + uncertainty > prior_commit
# => Waiting until the upper bound passes preserves the intended external order in this model.
assert safe_to_ack
```

**Key takeaway**: Commit-wait depends on a verified bound on clock uncertainty.

**Why It Matters**: Ordinary wall clocks do not provide this guarantee. Use such a mechanism only
where the platform exposes and monitors the required bound, not as a generic timestamp trick.

### Example 80: Compare AP and CP modes

**Context**: The capstone's two modes make the partition trade-off visible on the same key-value operation.

```python
partitioned = True
# => The simulated network prevents a required replica exchange.
cp_result = "blocked" if partitioned else "committed"
# => CP refuses the write while AP could accept locally and reconcile later.
assert cp_result == "blocked"
```

**Key takeaway**: A replicated store must document the behavior its mode chooses during a partition.

**Why It Matters**: The capstone tests the stated behavior rather than declaring one mode superior.
Readers should select the mode per operation based on whether divergence or unavailability is safer.

### Example 81: Describe an ephemeral lock

**Context**: A coordination service can bind lock ownership to a live session through an ephemeral sequential node.

```text
Create: /locks/order-0000000042 bound to the holder session.
Rule: the smallest sequence owns the lock; every waiter watches only its predecessor.
Failure: session loss removes the ephemeral node and releases the claim.
```

**Key takeaway**: Ephemeral sequential nodes make ownership and cleanup service-managed.

**Why It Matters**: The client must still handle session ambiguity and fencing at the protected
resource. A lock release observed by the service does not make a paused old client harmless.

### Example 82: Elect from sequential nodes

**Context**: The smallest live ephemeral-sequential node can lead while other candidates watch their predecessor.

```text
Candidates: member-0001, member-0002, member-0003.
Leader: member-0001; member-0002 watches member-0001, member-0003 watches member-0002.
Benefit: one predecessor watch avoids notifying every candidate on one departure.
```

**Key takeaway**: Predecessor watches reduce the herd effect in coordination-service election.

**Why It Matters**: Membership and session semantics come from the selected service. Keep the
application's leader duties small and fence its external side effects when leadership changes.

### Example 83: Register under a lease

**Context**: A service registry entry can expire automatically when its etcd lease is no longer renewed.

```text
Put: /services/orders/node-a with a TTL-backed lease.
Watch: consumers observe the prefix for additions and removals.
Expiry: a missed renewal removes the key without an explicit unregister call.
```

**Key takeaway**: A lease-backed registry turns liveness into a service-observed contract.

**Why It Matters**: A consumer must still treat discovery as eventually changing information. It needs
retry, connection failure handling, and an appropriate response when every discovered instance fails.

### Example 84: Guard configuration with compare-and-swap

**Context**: A revision guard prevents a writer from silently overwriting configuration changed by another writer.

```python
current_revision, writer_revision = 12, 11
# => The writer read an older version before a concurrent update completed.
accepted = writer_revision == current_revision
# => The stale conditional write is rejected instead of losing the newer configuration.
assert not accepted
```

**Key takeaway**: Compare-and-swap exposes conflicting configuration updates for retry or review.

**Why It Matters**: A rejected write is safer than an invisible lost update. The caller needs a
merge policy and authorization boundary; CAS itself does not determine which configuration is correct.

### Example 85: Choose a coordination-service boundary

**Context**: Record whether a mature coordination service or a bespoke consensus implementation fits the need.

| Choice                | Benefit                                      | Cost and verification                                                                        |
| --------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Coordination service  | Mature lease, watch, and consensus semantics | Operate and secure a dependency; verify its license and failure behavior                     |
| Hand-rolled consensus | Full learning and design control             | High implementation and correctness cost; reserve for the dedicated Raft construction course |

**Key takeaway**: Use a coordination service when its established contract fits the problem better than custom consensus.

**Why It Matters**: The decision must include the operational and licensing facts of the actual
product selected. This course teaches the trade-off; it does not declare ZooKeeper, etcd, or Consul mandatory.
