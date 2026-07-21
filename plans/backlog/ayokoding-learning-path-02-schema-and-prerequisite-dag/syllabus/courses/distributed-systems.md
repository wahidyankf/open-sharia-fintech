# Distributed Systems (By Example, Python)

**Course ID**: `distributed-systems` · **Format**: By Example · **Language**: Python.

**Short summary**: Consensus, replication, partitions, CAP

**Scope note**: why distributed systems are hard — CAP/PACELC, consensus (Paxos/Raft intuition),
logical clocks, replication, quorums, and CRDTs — taught as the failure modes that appear the moment
one machine becomes many. The point is judgment about trade-offs, not a from-scratch consensus
engine; that build lives in [`92-build-your-own-raft`](./build-your-own-raft.md). `†`: Python,
fully type-annotated (DD-39) — every snippet carries type hints in the pyright-clean spirit.

## Why this exists · the big idea

- **The problem before the solution**: on one machine, a write either happens or it doesn't. Add a
  network and everything you assumed breaks — messages arrive late, out of order, twice, or never; a
  node that looks dead is just slow; and no one has a shared "now". Reasoning that was trivial in
  process becomes a minefield of partial failure.
- **Keep-this-if-you-forget-everything**: in a distributed system the network is unreliable and there
  is no global clock, so you cannot have perfect consistency, availability, and partition tolerance at
  once — you choose which guarantee to relax, on purpose, per operation.
- **Big ideas touched**: `consistency-latency-throughput` (CAP/PACELC is exactly this trilemma —
  under a partition choose consistency or availability, and even without one, consistency costs
  latency), `determinism-vs-emergence` (correct global behaviour — agreement, ordering, convergence —
  has to _emerge_ from unreliable local message-passing, since no node sees the whole truth).

## Prerequisites

- **Prior topics**: [topic 12 Networking Essentials](./networking-essentials.md) (packets, latency,
  timeouts, why the network lies) and [topic 44 System Design](./system-design.md) (replication,
  partitioning, and the scaling context these guarantees serve).
- **Tools & environment**: a macOS/Linux terminal; **Python** at a recent stable release with type
  hints and `pyright`; the ability to run several communicating processes locally (asyncio or multiple
  processes) with simulated message delay/loss/reordering; Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: timeouts, retries, and network latency (topic 12); replication and sharding
  at a design level (topic 44); running concurrent tasks in Python (topics 04/24).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the theory here is settled and correctly version-unpinned — the CAP theorem
  (Gilbert–Lynch proof), Lamport's logical/vector clocks, Paxos, and **Raft** as the most widely
  implemented production consensus algorithm are all stable, foundational results, not moving targets.
- 2026-07-12 — verified: **PACELC** (Abadi) is correctly presented as the refinement of CAP that also
  accounts for the latency-vs-consistency trade-off in the _absence_ of a partition; keep CAP and
  PACELC together rather than treating CAP alone as complete. CRDTs are stable as a convergence
  strategy for AP designs.

> DD-35 primary-source pass (2026-07-12). The foundational papers were fetched and read directly
> where open-access (Lamport 1978, FLP 1985, Paxos Made Simple 2001, Raft 2014, Gifford 1979,
> φ-accrual 2004, Demers 1987, Kleppmann 2016, STONITH, Dapper 2010). Paywalled classics
> (2PC/Gray, 3PC/Skeen, PBFT, Sagas, vector clocks, bully/ring) are bibliographically `[Verified]`
> but their exact prose is `[Needs Verification]`. Misattributions to avoid are flagged.

- **Eight fallacies** — (1) network reliable, (2) latency zero, (3) bandwidth infinite, (4) network
  secure, (5) topology stable, (6) one administrator, (7) transport cost zero, (8) network homogeneous.
  **Attribution**: L. Peter Deutsch authored the first **seven** (1994); **James Gosling** added the
  eighth (~1997) — do not credit all eight to Deutsch alone, and there is **no canonical published URL**
  (internal Sun documents). Corroborated via [Wikipedia](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing); `[Needs Verification]` for a primary artifact.
- **Happens-before + logical clocks** — Lamport's `→` is "the smallest relation satisfying: (1) if a and b
  are in the same process and a comes before b then a→b; (2) if a is the sending of a message and b its
  receipt then a→b; (3) transitivity." Clock Condition: "if a→b then C(a) < C(b)"; **IR1** increments each
  process's clock; **IR2** advances the receiver past the message timestamp. Source: [Lamport, "Time, Clocks, and the Ordering of Events" (CACM 21(7), 1978)](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) (fetched, verbatim).
- **Vector clocks** — Fidge (ACSC'88) and Mattern (1988) developed them **independently**; "vector time
  cannot be attributed to a single person" (Schwarz & Mattern). Don't claim either as sole inventor.
  Bibliographic facts `[Verified]`; formal definitions `[Needs Verification]` (papers not fetchable).
- **CAP** — under a partition you cannot have both consistency and availability (Brewer's conjecture,
  proved by Gilbert & Lynch 2002, SIGACT News 33(2)). **PACELC** (Abadi 2012) extends it: Else (no
  partition) trade Latency vs Consistency.
- **Quorum intersection** — "every transaction collects a read quorum of r votes … and a write quorum of w
  votes … such that r+w is greater than the total number of votes … This ensures … a non-null intersection
  between every read quorum and every write quorum." Source: [Gifford, "Weighted Voting for Replicated Data" (SOSP 1979)](https://www.cs.cornell.edu/courses/cs5414/2017fa/papers/dynamo.pdf) (fetched abstract) — this is the origin of **R + W > N**.
- **Consensus / Paxos** — roles are "proposers, acceptors, and learners"; safety: "only a value that has
  been proposed may be chosen, only a single value is chosen, and a process never learns a value unless it
  actually has been [chosen]." Phase 1 `prepare`(n) → promise; Phase 2 `accept`(n, v) where v is the
  highest-numbered accepted value. Source: [Lamport, "Paxos Made Simple" (2001)](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf) (fetched, verbatim). The 1998 "Part-Time Parliament" is the harder original.
- **Raft** — **Election Safety**: "a candidate must receive votes from a majority … to become leader."
  **Leader Completeness**: "if a log entry is committed in a given term, then that entry will be present in
  the logs of the leader for all future terms." **Log Matching**: "if two logs contain an entry with the
  same index and term, then the logs are identical … up through the given index." A **term** is a logical
  clock. Source: [Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm" (USENIX ATC 2014)](https://raft.github.io/raft.pdf) (fetched, verbatim). Adopted by etcd, Consul, CockroachDB.
- **FLP impossibility** — "no completely asynchronous consensus protocol can tolerate even a single
  unannounced process death." **Scope**: crash (not Byzantine) failures, fully asynchronous, no synchronized
  clocks, reliable message delivery; it bounds **guaranteed termination**, not solvability. Source: [Fischer, Lynch, Paterson, "Impossibility of Distributed Consensus with One Faulty Process" (JACM 32(2), 1985)](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf) (fetched, verbatim). Failure detectors (Chandra–Toueg 1996) circumvent it.
- **φ-accrual failure detector** — outputs a **continuous suspicion level φ** rather than a binary
  trust/suspect decision; the app picks the threshold. Source: [Hayashibara et al., "The φ Accrual Failure Detector" (SRDS'04)](https://ieeexplore.ieee.org/document/1353004) (fetched, verbatim).
- **2PC / 3PC** — 2PC's **blocking problem**: if the coordinator crashes after participants vote yes
  (prepared) but before the decision, they block holding locks. 3PC (Skeen 1981) adds a `pre-commit` phase
  to be **nonblocking — but only under synchrony**, not under partitions. Gray 1978 first described 2PC.
  Bibliographic `[Verified]`; exact prose `[Needs Verification]` (paywalled).
- **Byzantine fault tolerance** — PBFT tolerates **f** faulty replicas out of **N = 3f + 1**; phases
  **pre-prepare / prepare / commit**. Safety holds under full asynchrony; liveness needs weak synchrony
  (avoid the oversimplified "PBFT works async"). Source: Castro & Liskov, "Practical Byzantine Fault
  Tolerance" (OSDI 1999); `[Needs Verification]` on exact prose (primary PDF unfetchable).
- **Gossip / epidemic** — "randomized algorithms for distributing updates … ensure that the effect of every
  update is eventually reflected in all replicas"; techniques are **anti-entropy** and **rumor-mongering**.
  Source: [Demers et al., "Epidemic Algorithms for Replicated Database Maintenance" (PODC 1987 / Xerox PARC CSL-89-1)](https://dl.acm.org/doi/10.1145/41840.41841) (fetched, verbatim abstract).
- **CRDTs** — two families: state-based **CvRDT** (convergent) and op-based **CmRDT** (commutative),
  equivalent in power; give **Strong Eventual Consistency (SEC)**. Source: Shapiro, Preguiça, Baquero,
  Zawirski, "Conflict-free Replicated Data Types" (INRIA RR-7687 / SSS 2011); exact SEC definition
  `[Needs Verification]` (scanned PDF).
- **Sagas** — a long-lived transaction as a sequence of local transactions each with a **compensating
  transaction** to undo it on failure. Origin: Garcia-Molina & Salem (SIGMOD 1987) — **single-database**
  LLTs, later re-adapted to microservices. `[Needs Verification]` on exact prose (paywalled).
- **Distributed locks / fencing** — a lease can expire while a paused (GC) client still believes it holds
  the lock; a **fencing token** is "a number that increases every time a client acquires the lock," and the
  resource server must reject any write carrying a lower token. Source: [Kleppmann, "How to do distributed locking" (2016)](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) (fetched, verbatim).
- **Split-brain / STONITH** — a "partitioned cluster" is when "two different systems each falsely believe
  the other to be dead"; STONITH ("Shoot The Other Node In The Head") fences by killing the other node so it
  cannot write. Source: [Robertson, Linux-HA STONITH doc](https://www.google.com/search?q=linux-ha+stonith) (fetched).
- **Delivery semantics** — at-most-once ("may be lost … not redelivered"), at-least-once ("never lost, but
  may be delivered more than once"), exactly-once ("once and only once"). End-to-end, "exactly-once" is
  really **at-least-once + idempotent processing = effectively-once**. Source: [Confluent — Message Delivery Guarantees](https://docs.confluent.io/kafka/design/delivery-semantics.html) (fetched); no single academic origin for the terminology.
- **Clock sync / TrueTime** — NTP's current spec is **RFC 5905 (NTPv4, 2010)**, not the historical RFC 958
  (1985). Spanner's **TrueTime** returns a bounded uncertainty interval `[earliest, latest]` (width ε) and
  uses **commit-wait** (wait out ε before acknowledging) for external consistency. Source: Corbett et al.,
  "Spanner" (OSDI 2012); TrueTime API/mechanism `[Verified]` via paraphrase, exact ε formula `[Needs Verification]`.
- **Coordination services (co-35–39, ex-81–85)** — added 2026-07-12. The theory (Chubby lineage; ZAB vs
  Raft; ephemeral/sequential znodes + watches; etcd Raft/MVCC/leases; Consul Serf/SWIM gossip; the
  ephemeral-sequential leader-election recipe that watches only the predecessor to avoid the herd effect)
  is well-established, but this rung was authored **without** a completed primary-source pass (the grounding
  agent died on network errors). `[Needs Verification]` at authoring time — confirm against primary docs
  before publishing: **ZooKeeper** ZAB + znode/watch semantics + Apache-2.0 (zookeeper.apache.org);
  **etcd** Raft + MVCC + leases + CNCF-graduated + Apache-2.0 (etcd.io); **Consul** Raft + Serf gossip +
  the **2023 license change to BUSL-1.1** (consul.io / hashicorp.com/license); **Chubby** (Burrows, OSDI 2006) as the coordination-service ancestor.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · fallacies-of-distributed-computing** — the eight false assumptions (Deutsch's seven + Gosling's eighth) that break naïve distributed designs.
- **co-02 · network-unreliable** — the first hard fact: messages can be lost, delayed, duplicated, or reordered.
- **co-03 · no-global-clock** — the second hard fact: no two nodes share a synchronized wall-clock.
- **co-04 · happens-before** — Lamport's causal `→` relation; two events with no `→` either way are concurrent.
- **co-05 · lamport-clock** — a scalar logical clock (IR1 increment, IR2 advance-on-receive) giving a consistent total order.
- **co-06 · vector-clock** — a per-process vector that captures causality and distinguishes concurrent from ordered events.
- **co-07 · concurrent-events** — events neither of which happens-before the other; a Lamport clock cannot detect them, a vector clock can.
- **co-08 · cap-theorem** — under a network partition you must choose consistency or availability (Gilbert & Lynch).
- **co-09 · pacelc** — even without a partition, choose latency vs consistency (Abadi).
- **co-10 · consistency-models** — strong/linearizable, causal, and eventual as distinct guarantees on the same data.
- **co-11 · leader-based-replication** — one leader accepts writes and propagates to read-only followers (with lag).
- **co-12 · leaderless-replication** — any replica accepts a write; conflicts resolved by version/timestamp (Dynamo-style).
- **co-13 · quorum-intersection** — R read + W write votes with R + W > N forces every read to overlap the latest write (Gifford).
- **co-14 · read-repair** — a read that spots a stale replica writes the fresh value back to it.
- **co-15 · replicated-state-machine** — applying the same ordered command log to each replica yields identical state (Schneider).
- **co-16 · log-abstraction** — an append-only ordered log is the shared source of truth for replication and consensus.
- **co-17 · consensus** — nodes agree on a single value despite failures, with safety (never two values) and liveness (eventually decide).
- **co-18 · paxos** — the classic consensus protocol: proposers/acceptors/learners, a two-phase prepare→accept (Lamport).
- **co-19 · raft** — an understandable consensus algorithm: leader election + log replication over numbered terms (Ongaro & Ousterhout).
- **co-20 · leader-election** — choosing a coordinator (bully by highest id, ring by circulating max, or Raft's majority vote).
- **co-21 · term-as-logical-clock** — Raft's monotonically increasing term detects and demotes stale leaders.
- **co-22 · log-matching** — if two logs share an entry's index and term, their prefixes up to it are identical (Raft).
- **co-23 · flp-impossibility** — no fully asynchronous consensus protocol can guarantee termination with even one crash (FLP).
- **co-24 · failure-detector** — heartbeats and φ-accrual suspicion levels detect crashes and let consensus proceed past FLP.
- **co-25 · two-phase-commit** — a coordinator's prepare→commit; its blocking problem when the coordinator crashes mid-decision (Gray).
- **co-26 · three-phase-commit** — 3PC adds a pre-commit phase to avoid blocking — but only under synchrony (Skeen).
- **co-27 · byzantine-fault-tolerance** — tolerating lying/arbitrary nodes: N = 3f + 1, PBFT's pre-prepare/prepare/commit (Castro & Liskov).
- **co-28 · gossip-epidemic** — anti-entropy and rumor-mongering spread updates so all replicas eventually converge (Demers).
- **co-29 · crdt** — conflict-free replicated data types merge deterministically to give strong eventual consistency (Shapiro).
- **co-30 · saga** — a distributed workflow as local transactions with compensating actions on failure (Garcia-Molina).
- **co-31 · distributed-lock-fencing** — a lease-based lock plus a monotonic fencing token the resource server enforces (Kleppmann).
- **co-32 · split-brain-stonith** — a partitioned cluster where both sides think they lead; fencing (STONITH) prevents dual writes.
- **co-33 · delivery-semantics** — at-most-once / at-least-once / exactly-once, and how idempotency makes at-least-once effectively-once.
- **co-34 · clock-sync-truetime** — NTP synchronizes clocks approximately; Spanner's TrueTime bounds uncertainty and commit-waits it out.
- **co-35 · coordination-service** — a small, strongly-consistent, highly-available store (ZooKeeper / etcd / Consul) that other distributed systems lean on for the hard coordination they don't want to reimplement — locks, leader election, membership, config — descending from Google's Chubby (Burrows, 2006).
- **co-36 · zookeeper-znodes-and-watches** — ZooKeeper's data model is a tree of _znodes_: _ephemeral_ nodes vanish when the creating session ends, _sequential_ nodes gain a monotonic suffix, and one-shot _watches_ notify a client of a change — the primitives its recipes build on (agreement via the ZAB atomic-broadcast protocol, not Raft).
- **co-37 · etcd-raft-kv** — etcd is a Raft-backed MVCC key-value store (Kubernetes' own backing store) offering leases, watches, and compare-and-swap transactions via `etcdctl` — the CNCF-default coordination store.
- **co-38 · coordination-recipes** — the classic recipes composed from those primitives: a distributed lock, leader election (create an ephemeral-sequential node and watch only your _predecessor_ to avoid the herd effect), a barrier, and a config store.
- **co-39 · service-discovery-and-membership** — instances register (typically via an ephemeral node / TTL lease) and clients discover the live set; Consul adds gossip-based (Serf / SWIM) membership + health checks alongside its Raft KV.

## Tensions & trade-offs — when NOT to reach for this

- **Distribution is a cost, not a feature**: consensus, quorums, and replication add latency, failure
  modes, and operational burden. A single well-backed-up node with a fast restore is simpler and often
  correct — reach for a distributed protocol only when the availability or scale requirement genuinely
  forces it.
- **Strong consistency isn't free and isn't always needed**: linearizable consensus costs a round trip
  and stalls under partition; many workloads are fine with causal or eventual consistency and a CRDT.
  Paying for strong consistency where the domain tolerates staleness is latency you burn for nothing.
- **Rolling your own consensus is a trap in production**: the algorithms are subtle and the failure
  cases are adversarial. Build one to _understand_ it (topic 92), but in production adopt a proven
  implementation (etcd/Consul/a database that embeds Raft) rather than hand-writing the protocol.

## Lineage — why it beat the alternative

- Distributed-systems theory grew from trying to make many unreliable machines behave like one
  reliable one. Lamport's 1978 logical clocks gave ordering without a shared clock; the CAP theorem
  (conjectured by Brewer, proved by Gilbert and Lynch) named the fundamental trade-off; Paxos proved
  consensus was possible but was famously hard to understand, so Raft (2014) re-expressed the same
  guarantees around an understandable leader-and-log model — which is why etcd, Consul, and
  CockroachDB adopted it. The winner wasn't a single protocol but the discipline of choosing your
  consistency model per operation. This feeds the hands-on build in
  [`92-build-your-own-raft`](./build-your-own-raft.md) and the scaling context in
  [topic 44 System Design](./system-design.md).

## Worked examples

Colocated under `distributed-systems/learning/code/` as typed, pyright-clean Python; each runnable as several
communicating local processes/tasks with injectable delay/loss (DD-20/DD-30/DD-34/DD-39). Contiguous
`ex-01..ex-85`. Every example cites the `co-NN` it exercises; concepts are taught before the examples.

### Beginner

- **ex-01 · fallacies-checklist** — annotate the eight fallacies, each with a failing scenario — verify each fallacy names a concrete failure. (co-01)
- **ex-02 · network-loss-inject** — a channel that drops messages at a rate — verify some sends never arrive. (co-02)
- **ex-03 · network-delay-inject** — a channel that delays messages — verify arrival order can differ from send order. (co-02)
- **ex-04 · no-global-clock-demo** — two nodes' wall-clocks disagree — verify a timestamp comparison misorders events. (co-03)
- **ex-05 · lamport-clock-basic** — increment a scalar clock on each local event — verify monotonic growth. (co-05)
- **ex-06 · lamport-clock-message** — carry the timestamp and advance on receive (IR2) — verify the receiver's clock jumps past the sender's. (co-05)
- **ex-07 · lamport-total-order** — break timestamp ties by process id — verify a deterministic total order. (co-05)
- **ex-08 · happens-before-relation** — build the `→` relation over a message history — verify transitive causal edges. (co-04)
- **ex-09 · lamport-cannot-detect-concurrency** — two concurrent events still get ordered timestamps — verify the false ordering. (co-05, co-07)
- **ex-10 · vector-clock-basic** — a per-process vector incremented locally — verify each index tracks its process. (co-06)
- **ex-11 · vector-clock-message** — merge element-wise max on receive — verify the merged vector dominates both. (co-06)
- **ex-12 · vector-clock-causal** — detect a happened-before b — verify one vector strictly dominates. (co-06, co-04)
- **ex-13 · vector-clock-concurrent** — detect concurrent events — verify neither vector dominates. (co-06, co-07)
- **ex-14 · vector-clock-vs-lamport** — the vector detects concurrency the scalar clock misses — verify on the same history. (co-05, co-06)
- **ex-15 · causal-delivery** — hold a message until its causal dependencies arrive — verify out-of-order messages are buffered. (co-04)
- **ex-16 · consistency-strong** — a linearizable single register — verify a read always returns the last write. (co-10)
- **ex-17 · consistency-eventual** — replicas converge once writes stop — verify divergence then convergence. (co-10)
- **ex-18 · consistency-causal** — causal order preserved, concurrent order may differ — verify causal reads are consistent. (co-10)
- **ex-19 · cap-partition-choose** — under a partition, pick C or A explicitly — verify the choice is enforced. (co-08)
- **ex-20 · cap-cp-behaviour** — a CP register refuses writes during a partition — verify unavailability. (co-08)
- **ex-21 · cap-ap-behaviour** — an AP register stays writable but may diverge — verify availability + divergence. (co-08)
- **ex-22 · pacelc-else-latency** — with no partition, trade latency vs consistency — verify a fast read can be stale. (co-09)
- **ex-23 · delivery-at-most-once** — fire-and-forget over a lossy channel — verify a lost message is not retried. (co-33)
- **ex-24 · delivery-at-least-once** — retransmit until acked — verify duplicates can occur. (co-33)
- **ex-25 · idempotent-receiver** — dedup by sequence number — verify a duplicate is ignored. (co-33)
- **ex-26 · effectively-once** — at-least-once plus idempotency — verify the net effect is once. (co-33)

### Intermediate

- **ex-27 · leader-follower-replicate** — writes to a leader propagate to followers — verify followers apply the write. (co-11)
- **ex-28 · follower-read-stale** — a follower serves a read before replication lands — verify the stale value. (co-11)
- **ex-29 · leaderless-write** — write to N replicas directly — verify all reachable replicas store it. (co-12)
- **ex-30 · quorum-write** — require W acks for a write — verify it fails below W. (co-13)
- **ex-31 · quorum-read** — require R responses for a read — verify it fails below R. (co-13)
- **ex-32 · quorum-intersection** — R + W > N guarantees overlap — verify a read sees the latest write. (co-13)
- **ex-33 · sub-quorum-stale** — R + W ≤ N can miss the latest write — verify a stale read appears. (co-13)
- **ex-34 · read-repair** — a read repairs a stale replica — verify the lagging replica is updated. (co-14)
- **ex-35 · last-writer-wins** — resolve concurrent writes by version/timestamp — verify the newest wins. (co-12)
- **ex-36 · version-vector-conflict** — detect a write conflict via vectors — verify concurrent writes are flagged. (co-06)
- **ex-37 · heartbeat-detector** — declare a node dead after missed heartbeats — verify detection after the threshold. (co-24)
- **ex-38 · timeout-tuning** — a too-aggressive timeout false-positives a live node — verify the false suspicion. (co-24)
- **ex-39 · phi-accrual** — output a continuous suspicion level φ — verify φ rises as heartbeats lapse. (co-24)
- **ex-40 · replicated-state-machine** — apply the same command log to two replicas — verify identical resulting state. (co-15)
- **ex-41 · rsm-determinism** — the same log always yields the same state — verify two applications match. (co-15)
- **ex-42 · command-log** — an append-only ordered command log — verify entries are never overwritten. (co-16)
- **ex-43 · log-replication** — a leader replicates its log to followers — verify follower logs match. (co-16, co-19)
- **ex-44 · log-matching** — same index + term implies identical prefix — verify a mismatch is detected. (co-22)
- **ex-45 · flp-impossibility-demo** — a run that never decides without a timeout — verify non-termination. (co-23)
- **ex-46 · failure-detector-circumvents-flp** — adding a timeout lets consensus proceed — verify a decision is reached. (co-23, co-24)
- **ex-47 · two-phase-commit** — coordinator prepare → commit across participants — verify all-or-nothing. (co-25)
- **ex-48 · 2pc-blocking** — a coordinator crash strands prepared participants — verify they block. (co-25)
- **ex-49 · three-phase-commit** — a pre-commit phase avoids blocking under synchrony — verify progress after coordinator loss. (co-26)
- **ex-50 · bully-election** — the highest-id live node becomes coordinator — verify the winner. (co-20)
- **ex-51 · ring-election** — the max id circulates the ring — verify all agree on it. (co-20)
- **ex-52 · gossip-anti-entropy** — pairwise state reconciliation — verify two nodes converge after exchange. (co-28)
- **ex-53 · gossip-rumor-spread** — an update spreads epidemically — verify all nodes receive it. (co-28)
- **ex-54 · distributed-lock-lease** — a lock with a TTL lease — verify it auto-expires. (co-31)

### Advanced

- **ex-55 · raft-election** — followers become candidate then leader on timeout — verify one leader emerges. (co-19, co-20)
- **ex-56 · raft-term-increment** — a new election increments the term — verify the term advances. (co-21)
- **ex-57 · raft-vote-majority** — a candidate needs a majority of votes — verify a minority cannot win. (co-19)
- **ex-58 · raft-heartbeat** — the leader sends periodic heartbeats — verify followers stay followers. (co-19)
- **ex-59 · raft-log-append** — the leader appends and replicates entries — verify followers store them. (co-19, co-16)
- **ex-60 · raft-commit-majority** — an entry commits once a majority stores it — verify the commit index advances. (co-19)
- **ex-61 · raft-log-matching** — enforce the log-matching property on append — verify a conflicting entry is rejected. (co-22)
- **ex-62 · raft-stale-leader-steps-down** — a leader seeing a higher term steps down — verify the demotion. (co-21)
- **ex-63 · raft-partition-reelection** — a partition triggers a re-election — verify a new leader on the majority side. (co-19)
- **ex-64 · raft-log-convergence** — followers converge after the partition heals — verify logs reconcile. (co-19)
- **ex-65 · paxos-prepare-promise** — phase 1 prepare/promise — verify an acceptor promises not to accept lower. (co-18)
- **ex-66 · paxos-accept** — phase 2 accept with the highest-numbered value — verify the chosen value. (co-18)
- **ex-67 · paxos-single-value-chosen** — only one value is ever chosen — verify no two proposers succeed with different values. (co-18, co-17)
- **ex-68 · consensus-safety** — never two different chosen values — verify the safety invariant under contention. (co-17)
- **ex-69 · crdt-g-counter** — a grow-only counter merges by per-node max — verify commutative merge. (co-29)
- **ex-70 · crdt-pn-counter** — increments and decrements via two G-counters — verify the net value converges. (co-29)
- **ex-71 · crdt-g-set** — a grow-only set merges by union — verify order-independent convergence. (co-29)
- **ex-72 · crdt-lww-register** — a last-writer-wins register merge — verify the latest timestamp wins. (co-29)
- **ex-73 · crdt-strong-eventual-consistency** — replicas converge regardless of merge order — verify all orders agree. (co-29)
- **ex-74 · byzantine-fault** — a lying node needs N = 3f + 1 to tolerate — verify agreement despite the liar. (co-27)
- **ex-75 · pbft-phases** — pre-prepare / prepare / commit rounds — verify a request commits after two rounds of votes. (co-27)
- **ex-76 · saga-compensation** — a distributed workflow undoes completed steps on failure — verify compensation runs. (co-30)
- **ex-77 · split-brain-demo** — two nodes both believe they lead — verify the conflicting-leader state. (co-32)
- **ex-78 · fencing-token** — reject a write carrying a stale fencing token — verify the resource server refuses it. (co-31, co-32)
- **ex-79 · truetime-commit-wait** — wait out clock uncertainty ε before committing — verify commit order respects real time. (co-34)
- **ex-80 · replicated-kv-capstone** — a KV store with an AP quorum mode + read-repair and a CP leader-elected mode, under injected partition — verify the CP mode blocks while the AP mode stays available and later converges. (co-06, co-13, co-14, co-19, co-32)

### Coordination services

- **ex-81 · zookeeper-ephemeral-lock** — a distributed lock on ZooKeeper (via `kazoo`) using an ephemeral-sequential znode plus watch-predecessor — verify only one holder at a time and that a crashed holder's ephemeral node auto-releases the lock. (co-36, co-38)
- **ex-82 · leader-election-ephemeral-sequential** — elect a leader as the smallest sequential znode, each candidate watching only its predecessor — verify exactly one leader and that watching the predecessor (not all nodes) avoids the herd effect. (co-38, co-36)
- **ex-83 · etcd-lease-service-registry** — register a service under an etcd key bound to a TTL lease and watch the prefix — verify a live instance appears, its key auto-expires when the lease lapses, and watchers observe the change. (co-37, co-39)
- **ex-84 · etcd-cas-config** — store config in etcd and update it with a compare-and-swap (revision-guarded) transaction — verify a stale-revision write is rejected by MVCC, preventing a lost update. (co-37)
- **ex-85 · coordination-service-vs-diy-consensus** — a decision artifact (DD-20) contrasting leaning on a coordination service (ZooKeeper/etcd/Consul) against hand-rolling consensus (ties to [`92-build-your-own-raft`](./build-your-own-raft.md)) for locks/leader-election — verify the trade-off (operational dependency vs build cost) and each product's license are recorded. (co-35, co-19)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small replicated key-value store over a simulated unreliable network that
  demonstrates the trade-off explicitly — a quorum-based (AP-leaning) mode with read-repair and a
  leader-elected (CP-leaning) mode — with injectable delay, loss, and partition, and a test that
  proves the consistency behaviour of each mode.
- **Concepts exercised**: [ ] logical/vector clocks (co-05, co-06) [ ] read/write quorums — R + W > N
  (co-13) [ ] read-repair (co-14) [ ] leader election (co-19, co-20) [ ] partition injection (co-08,
  co-32) [ ] a consistency-behaviour assertion per mode (co-10).
- **Ordered steps**:
  1. `.../learning/capstone/code/clocks.py` — vector clocks tagging every write. Verify concurrent vs
     causally-ordered writes are correctly classified; `pyright` clean.
  2. `.../learning/capstone/code/quorum.py` — a leaderless quorum store with read-repair. Verify that
     `W + R > N` yields the latest value and that a sub-quorum can observe a stale read.
  3. `.../learning/capstone/code/raft.py` — leader election + log replication. Verify a single leader
     is elected per term and followers converge on the leader's log.
  4. `.../learning/capstone/code/partition_test.py` — inject a partition against both modes. Verify the
     CP mode blocks/loses availability while the AP mode stays available but may diverge then converge.
- **Acceptance criteria**: clocks classify causality correctly; quorum reads/writes obey R + W > N;
  leader election is stable; the partition test demonstrates each mode's advertised consistency/
  availability behaviour; all Python is type-annotated and `pyright`-clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Designing Data-Intensive Applications** — Martin Kleppmann (2017). Arguably the single most cited
  modern reference for replication, consistency, and partitioning trade-offs.
- **Distributed Systems: Principles and Paradigms** — Andrew S. Tanenbaum, Maarten van Steen (2nd ed.,
  2007). Long-standing academic textbook covering the core theory of distributed systems.

**Papers & articles**

- **Time, Clocks, and the Ordering of Events in a Distributed System** — Leslie Lamport (1978). The
  foundational paper introducing logical clocks and the happened-before relation.
  <https://lamport.azurewebsites.net/pubs/time-clocks.pdf>
- **Paxos Made Simple** — Leslie Lamport (2001). The clearest author-written explanation of the Paxos
  consensus algorithm. <https://lamport.azurewebsites.net/pubs/paxos-simple.pdf>
- **In Search of an Understandable Consensus Algorithm (Extended Version)** — Diego Ongaro, John
  Ousterhout (2014), USENIX ATC. Introduced Raft, now the most widely implemented consensus algorithm
  in production systems (etcd, Consul, CockroachDB). <https://raft.github.io/raft.pdf>
- **CAP Twelve Years Later: How the "Rules" Have Changed** — Eric Brewer (2012), IEEE Computer.
  Brewer's own retrospective clarifying and correcting common misreadings of the CAP theorem.

## In which paths

- `interview-ready/software-engineer` — Go deeper · Architecture, distributed & internals builds — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Architecture, distributed & internals builds — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 7 · Networking, architecture & distributed systems.

> _Content originated in the now-closed FS-SE plan (topic 46); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
