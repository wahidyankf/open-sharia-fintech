# Build Your Own Raft (By Example, Go)

**Course ID**: `build-your-own-raft` · **Format**: By Example · **Language**: Go.

**Short summary**: Raft consensus and a replicated key-value store

**Scope note**: demystify consensus by building it — a Raft implementation (leader election + log
replication) driving a small replicated key-value store, exercised under deliberate failure injection
(dropped messages, partitions, crashed nodes). This is the build-your-own tier of
[`46-distributed-systems`](./distributed-systems.md): that topic gave the CAP/consensus intuition; here
you make Raft real. `†`: Go, chosen for its goroutines/channels and `net/rpc` — the concurrency model maps
cleanly onto Raft's timers, RPCs, and per-peer state.

## Why this exists · the big idea

- **The problem before the solution**: keeping several machines agreeing on one ordered history — through
  crashes, delays, and network splits — is deceptively hard, and hand-rolled "just have a leader" schemes
  quietly lose or duplicate data; consensus algorithms exist because the obvious approaches are subtly wrong.
- **Keep-this-if-you-forget-everything**: Raft reduces consensus to an understandable core — elect exactly
  one leader per term, replicate an append-only log to a majority, and only apply an entry once it is safely
  on a quorum. A majority that agrees on a prefix of the log is the whole game.
- **Big ideas touched**: `consistency-latency-throughput` (a write must reach a quorum before it commits —
  that round-trip is the latency price of strong consistency), `determinism-vs-emergence` (correct global
  behaviour — a single consistent log — has to emerge from independent nodes exchanging messages with no
  shared clock).

## Prerequisites

- **Prior topics**: [topic 46 Distributed Systems](./distributed-systems.md) (CAP/PACELC, consensus
  intuition, logical clocks, quorums — the theory this topic implements) and
  [topic 64 Just Enough Go](./just-enough-go.md) (goroutines, channels, and RPC for the concurrency model).
- **Tools & environment**: a macOS/Linux terminal; **Go** on a recent stable toolchain; the standard library
  (`net/rpc` or gRPC, `testing`, `time`) plus a way to simulate an unreliable network (a message-dropping/
  delaying test harness); Neovim/VSCode with the Go LSP (`gopls`, DD-17).
- **Assumed knowledge**: the consensus problem and why quorums matter (topic 46); Go concurrency —
  goroutines, channels, `select`, timers (topic 64); writing tests that inject failure (topic 15).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: Raft's structure — terms, leader election with randomized election timeouts,
  `AppendEntries`/`RequestVote` RPCs, log matching, and the commit rule (replicate to a majority, then apply)
  — is stable and matches the Ongaro–Ousterhout paper; correctly left version-unpinned. The Go standard
  library surface (`net/rpc`, `testing`, `time`) used here is evergreen.
- 2026-07-12 — verified (SCOPE note for plan owner): implement the core (leader election + log replication +
  a replicated KV state machine on top) and treat log compaction/snapshotting and dynamic membership changes
  as clearly-labelled stretch goals — they are part of full Raft but not needed to demonstrate consensus. The
  MIT 6.5840 labs are a well-trodden reference for exactly this scoping. (raft.github.io; pdos.csail.mit.edu/6.824)

### DD-35 primary-source citations (fetched-and-read)

Every RPC, property, and scope claim below traces to a primary source fetched and read during grounding.
Unverifiable specifics are marked `[Needs Verification]` and never shipped as fact.

- **The Raft paper** — Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm (Extended
  Version)" (2014) — is the primary source. **Figure 2** specifies the state (`currentTerm`, `votedFor`,
  `log[]`, `commitIndex`, `lastApplied`, per-leader `nextIndex[]`/`matchIndex[]`) and the two RPCs
  (`RequestVote`, `AppendEntries`) with their exact rules. (raft.github.io/raft.pdf)
- **Figure 3 — the five safety properties**: Election Safety (≤1 leader per term), Leader Append-Only,
  Log Matching, Leader Completeness, State Machine Safety. These are the invariants the tests assert.
  (raft.github.io/raft.pdf §5.2–§5.4)
- **Randomized election timeouts** avoid repeated split votes; a candidate wins on a **majority** of votes.
  **Commit rule**: an entry commits once replicated to a majority, and a leader commits entries **from its
  own current term** directly (earlier-term entries commit indirectly). (raft.github.io/raft.pdf §5.2, §5.4.2)
- **Persistence** — `currentTerm`, `votedFor`, and `log[]` are persisted to stable storage **before**
  responding to RPCs, so a restarted node never double-votes or loses committed entries. (raft.github.io/raft.pdf Figure 2)
- **Scope (verified)** — core = election + replication + persistence + a replicated KV state machine;
  **snapshotting** (§7) and **membership change** (§6) are labelled stretch goals. **MIT 6.5840** (formerly
  6.824) labs scope Raft exactly this way. (pdos.csail.mit.edu/6.824)
- **Implementation** — Go on a recent stable toolchain, standard library only (`net/rpc`, `testing`, `time`),
  with a message-dropping/delaying/partitioning test harness; `†` chosen for goroutines/channels/timers.

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject). Each example below cites the co-NN it exercises. -->

- **co-01 · consensus-problem** — several nodes must agree on one ordered history despite crashes and delays.
- **co-02 · raft-roles** — every node is a follower, candidate, or leader at any time.
- **co-03 · terms** — terms are Raft's logical clock; a higher term always wins and forces a step-down.
- **co-04 · per-peer-state** — a leader tracks `nextIndex`/`matchIndex` for each follower.
- **co-05 · election-timeout** — a randomized timeout with no heartbeat triggers a new election.
- **co-06 · request-vote** — the `RequestVote` RPC solicits votes to become leader.
- **co-07 · vote-granting** — a node grants at most one vote per term, to a sufficiently up-to-date candidate.
- **co-08 · leader-election** — a candidate winning a majority of votes becomes leader for that term.
- **co-09 · split-vote** — randomized timeouts make repeated split votes unlikely.
- **co-10 · heartbeat** — the leader sends empty `AppendEntries` to suppress follower elections.
- **co-11 · append-entries** — the `AppendEntries` RPC replicates log entries to followers.
- **co-12 · log-entry** — each entry carries a term and a state-machine command.
- **co-13 · log-matching** — if two logs share an index+term, all preceding entries are identical.
- **co-14 · consistency-check** — `prevLogIndex`/`prevLogTerm` must match or the follower rejects.
- **co-15 · log-repair** — on rejection the leader backs up `nextIndex` and the follower truncates conflicts.
- **co-16 · commit-index** — an entry commits once a majority stores it; `commitIndex` advances.
- **co-17 · apply-to-state-machine** — committed entries are applied in log order.
- **co-18 · replicated-kv** — a key-value store is the state machine driven by the committed log.
- **co-19 · leader-completeness** — a committed entry is present in every future leader's log.
- **co-20 · election-restriction** — only a candidate with an up-to-date log can win, protecting commits.
- **co-21 · state-machine-safety** — no two nodes apply a different command at the same log index.
- **co-22 · persistence** — `currentTerm`/`votedFor`/`log` persist before an RPC reply.
- **co-23 · crash-restart** — a restarted node recovers persisted state and rejoins safely.
- **co-24 · partition-tolerance** — a minority partition cannot commit; the majority side makes progress.
- **co-25 · network-drop** — dropped or delayed messages are retried; correctness holds regardless.
- **co-26 · linearizability** — clients observe reads/writes as one consistent, ordered history.
- **co-27 · failure-injection** — a harness drops/delays/partitions messages to test safety under failure.
- **co-28 · liveness** — with a working majority, a leader is eventually elected and progress resumes.
- **co-29 · snapshot-stretch** — snapshotting + log compaction is a labelled stretch goal.
- **co-30 · membership-stretch** — dynamic cluster membership change is a labelled stretch goal.

## Worked examples

Colocated under `build-your-own-raft/learning/code/`; Go (`go test`) with a message-dropping/partitioning
test harness (DD-20/DD-30). Correctness is proven under injected failure, not just the happy path. Contiguous
`ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · node-roles-enum** — a role type (`Follower`/`Candidate`/`Leader`) — verify transitions compile. (co-02)
- **ex-02 · term-counter** — a `currentTerm` field — verify it increments on a new election. (co-03)
- **ex-03 · election-timer** — a randomized election timer — verify timeouts fall in `[T, 2T]`. (co-05)
- **ex-04 · timer-reset-on-heartbeat** — reset the timer on `AppendEntries` — verify no election while heartbeats arrive. (co-05, co-10)
- **ex-05 · become-candidate** — timeout promotes a follower to candidate — verify the transition. (co-02, co-05)
- **ex-06 · request-vote-rpc** — a `RequestVote` RPC struct + handler — verify a vote reply. (co-06)
- **ex-07 · vote-once-per-term** — grant only one vote per term — verify a second request is denied. (co-07)
- **ex-08 · vote-deny-lower-term** — deny a candidate with a stale term — verify the denial. (co-07, co-03)
- **ex-09 · count-votes-majority** — tally votes for a majority — verify the threshold. (co-08)
- **ex-10 · become-leader** — a majority promotes a candidate to leader — verify the transition. (co-08, co-02)
- **ex-11 · three-node-election** — 3 nodes elect one leader — verify exactly one leader. (co-08)
- **ex-12 · five-node-election** — 5 nodes elect one leader — verify exactly one leader. (co-08)
- **ex-13 · one-leader-per-term** — assert at most one leader per term — verify Election Safety. (co-08, co-03)
- **ex-14 · term-increment-on-election** — each election bumps the term — verify monotonic terms. (co-03)
- **ex-15 · higher-term-steps-down** — seeing a higher term reverts to follower — verify the step-down. (co-02, co-03)
- **ex-16 · split-vote-retry** — a split vote triggers a new randomized timeout — verify a later term elects. (co-09)
- **ex-17 · randomized-timeout-range** — measure timeout spread — verify they are randomized, not fixed. (co-05, co-09)
- **ex-18 · heartbeat-suppresses-election** — a steady leader heartbeat — verify no follower times out. (co-10)
- **ex-19 · leader-crash-reelection** — kill the leader — verify a new leader is elected. (co-08)
- **ex-20 · candidate-loses-to-higher-term** — a candidate sees a higher term — verify it steps down. (co-02)
- **ex-21 · go-test-election** — a `go test` asserting one leader per term — verify it passes. (co-27)
- **ex-22 · rpc-over-net** — wire `RequestVote` over `net/rpc` — verify a round-trip. (co-06)
- **ex-23 · concurrent-timers** — one goroutine per node's timer — verify independent timing. (co-05)
- **ex-24 · vote-request-parallel** — send vote requests concurrently — verify all peers are asked. (co-06)
- **ex-25 · election-under-drop** — elect with some vote messages dropped — verify a leader still emerges. (co-25, co-08)
- **ex-26 · go-test-reelection** — a `go test` for re-election after a crash — verify it passes. (co-27, co-28)

### Intermediate

- **ex-27 · log-entry-struct** — a `{Term, Command}` entry — verify the encoding. (co-12)
- **ex-28 · append-entries-rpc** — an `AppendEntries` RPC struct + handler — verify a reply. (co-11)
- **ex-29 · leader-appends-local** — the leader appends a client command to its own log — verify the entry. (co-11, co-12)
- **ex-30 · replicate-to-followers** — the leader sends entries to followers — verify they receive them. (co-11)
- **ex-31 · prev-log-check** — `prevLogIndex`/`prevLogTerm` matching — verify a matched append succeeds. (co-14)
- **ex-32 · consistency-check-reject** — a mismatch is rejected — verify the follower says false. (co-14)
- **ex-33 · next-index-decrement** — on rejection the leader backs up `nextIndex` — verify the retry. (co-15, co-04)
- **ex-34 · log-backfill** — a follower missing entries catches up — verify its log fills in. (co-15)
- **ex-35 · log-matching-property** — assert shared index+term → identical prefix — verify Log Matching. (co-13)
- **ex-36 · conflict-truncate** — a conflicting suffix is deleted before append — verify truncation. (co-15)
- **ex-37 · match-index-track** — the leader tracks `matchIndex` per peer — verify it advances. (co-04)
- **ex-38 · commit-on-majority** — `commitIndex` advances on majority replication — verify the commit. (co-16)
- **ex-39 · commit-current-term-only** — a leader commits only its own-term entries directly — verify the rule. (co-16, co-19)
- **ex-40 · apply-committed** — committed entries apply to the state machine — verify application. (co-17)
- **ex-41 · apply-order** — entries apply in log order — verify no reordering. (co-17)
- **ex-42 · lagging-follower-catchup** — a slow follower converges — verify its log matches the leader. (co-15)
- **ex-43 · leader-append-only** — the leader never overwrites/deletes its own entries — verify Leader Append-Only. (co-13)
- **ex-44 · election-restriction-uptodate** — only an up-to-date candidate wins — verify the restriction. (co-20)
- **ex-45 · deny-vote-stale-log** — deny a vote to a less-up-to-date log — verify the denial. (co-20)
- **ex-46 · logs-converge** — after replication all logs match — verify convergence. (co-13)
- **ex-47 · heartbeat-carries-commit** — `leaderCommit` propagates on heartbeats — verify followers advance. (co-16, co-10)
- **ex-48 · client-write-commits** — a client write reaches a quorum and commits — verify the ack. (co-16)
- **ex-49 · go-test-replication** — a `go test` for log convergence — verify it passes. (co-27)
- **ex-50 · go-test-catchup** — a `go test` for follower catch-up — verify it passes. (co-27, co-15)
- **ex-51 · concurrent-appends** — replicate to peers concurrently — verify all converge. (co-11)
- **ex-52 · no-op-on-election** — a new leader commits prior entries via a current-term entry — verify indirect commit. (co-16, co-19)

### Advanced

- **ex-53 · kv-state-machine** — apply the log to a KV map — verify `put` mutates the store. (co-18, co-17)
- **ex-54 · kv-put-get** — `put`/`get` through Raft — verify a value written is read back. (co-18)
- **ex-55 · kv-linearizable-read** — a linearizable read path — verify reads reflect committed writes. (co-26)
- **ex-56 · persist-term-vote** — persist `currentTerm`/`votedFor` — verify they survive a restart. (co-22)
- **ex-57 · persist-log** — persist the log — verify entries survive a restart. (co-22)
- **ex-58 · restart-recover-state** — reload persisted state on boot — verify the node resumes correctly. (co-23, co-22)
- **ex-59 · restart-no-double-vote** — a restarted node honours its prior vote — verify no double vote in a term. (co-23, co-07)
- **ex-60 · partition-minority-blocks** — a minority partition cannot commit — verify no commit there. (co-24)
- **ex-61 · partition-majority-progresses** — the majority side keeps committing — verify progress. (co-24, co-16)
- **ex-62 · partition-heal-converge** — after healing, logs converge — verify one consistent log. (co-24, co-13)
- **ex-63 · stale-leader-steps-down** — a partitioned old leader rejoins — verify it steps down to follower. (co-03, co-02)
- **ex-64 · no-committed-loss** — a committed write survives a partition — verify it is never lost. (co-19, co-24)
- **ex-65 · drop-messages-retry** — dropped RPCs are retried — verify eventual delivery. (co-25)
- **ex-66 · delayed-messages** — delayed/reordered messages — verify correctness holds. (co-25)
- **ex-67 · crash-restart-cycle** — kill and restart nodes repeatedly — verify the cluster recovers. (co-23)
- **ex-68 · failure-harness** — a drop/delay/partition injector — verify it can sever links. (co-27)
- **ex-69 · safety-under-failure** — assert no two leaders in one term under failure — verify Election Safety. (co-21, co-27)
- **ex-70 · state-machine-safety-test** — assert same index → same command across nodes — verify State Machine Safety. (co-21)
- **ex-71 · leader-completeness-test** — a committed entry appears in every later leader — verify Leader Completeness. (co-19)
- **ex-72 · liveness-under-heal** — after a partition heals a leader is elected — verify liveness resumes. (co-28)
- **ex-73 · snapshot-stretch** — snapshot the state and truncate the log (stretch) — verify a snapshot restores state. (co-29)
- **ex-74 · install-snapshot-stretch** — an `InstallSnapshot` RPC (stretch) — verify a lagging follower is snapshotted. (co-29)
- **ex-75 · membership-change-stretch** — add/remove a node (stretch) — verify the cluster reconfigures safely. (co-30)
- **ex-76 · full-cluster-kv-cycle** — write → partition → restart → read — verify a consistent value. (co-18, co-24, co-26)
- **ex-77 · go-test-safety-liveness** — a `go test` asserting safety + liveness under failure — verify it passes. (co-27, co-28)
- **ex-78 · capstone-raft-kv** — the capstone: Raft (election + replication + persistence) driving a replicated KV — verify end-to-end + correct under failure injection + green tests. (co-08, co-16, co-18, co-22, co-27)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a working Raft — leader election, log replication, and persistence — that drives a
  replicated key-value store across a cluster of nodes, and prove it keeps a single consistent, durable log
  under dropped messages, partitions, and node restarts, all exercised by `go test` with a failure-injecting
  harness.
- **Concepts exercised**: [ ] terms + roles + per-peer state (co-02, co-03, co-04) [ ] leader election with
  randomized timeouts (co-05, co-08, co-09) [ ] `AppendEntries` log replication + commit rule (co-11, co-13,
  co-16) [ ] a replicated KV state machine (co-17, co-18) [ ] persistence across restarts (co-22, co-23)
  [ ] failure injection (drops/partitions/crashes) (co-24, co-25, co-27) [ ] `go test` coverage of safety +
  liveness (co-21, co-28).
- **Ordered steps**:
  1. `.../learning/capstone/code/raft/` — the Raft node with terms, roles, and `RequestVote`/`AppendEntries`
     RPCs; a test harness that can drop/delay/partition messages. Verify exactly one leader is elected per
     term and a re-election follows a leader crash (`go test`).
  2. Implement log replication + the commit index and persist term/vote/log. Verify a committed entry reaches
     a quorum, a lagging follower catches up, and state survives a restart (`go test`).
  3. `.../kv/` — a replicated key-value store applying the committed log. Verify client reads/writes are
     linearizable under partitions and restarts, and all live nodes converge to one log (`go test`).
- **Acceptance criteria**: one leader per term; committed entries never lost or reordered; followers converge;
  the KV store stays consistent under injected failures; persisted state survives restart; `go test` covers
  safety and liveness.
- **Done bar**: runnable end-to-end + correct under failure injection + tests green + web-verified.

## Read more

**Books**

- **Designing Data-Intensive Applications** — Martin Kleppmann (2017). Provides the replication and consensus
  context that underpins Raft-based systems.

**Papers & articles**

- **In Search of an Understandable Consensus Algorithm (Extended Version)** — Diego Ongaro, John Ousterhout
  (2014). THE Raft paper; the primary source for the algorithm. <https://raft.github.io/raft.pdf>
- **Consensus: Bridging Theory and Practice** — Diego Ongaro (PhD dissertation, 2014). The full formal
  treatment and proofs behind Raft, by its co-creator, including snapshotting and membership change.
  <https://web.stanford.edu/~ouster/cgi-bin/papers/OngaroPhD.pdf>
- **Paxos Made Simple** — Leslie Lamport (2001). The canonical predecessor consensus paper that motivates why
  Raft was designed for understandability. <https://www.microsoft.com/en-us/research/publication/paxos-made-simple/>
- **The Raft Consensus Algorithm** — Diego Ongaro et al. Official companion site with an interactive
  visualization widely used to build intuition before implementing Raft. <https://raft.github.io/>
- **MIT 6.5840 (6.824) Distributed Systems** — MIT PDOS. Free graduate course whose labs have students
  implement Raft and a replicated KV store from scratch. <https://pdos.csail.mit.edu/6.824/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Architecture, distributed & internals builds — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Architecture, distributed & internals builds — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 8 · Internals builds (apply the fundamentals).

> _Content originated in the now-closed FS-SE plan (topic 92); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
