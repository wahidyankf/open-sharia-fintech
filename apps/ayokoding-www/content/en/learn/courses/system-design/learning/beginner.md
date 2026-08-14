---
title: "Estimation and foundations"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

## Make the problem measurable

These examples establish the artifacts that keep a design from becoming a list of fashionable
components. Every number must influence a decision; every promise must say what happens when the
network is imperfect.

### Worked Example 1: Separate requirements

**Context**: A URL shortener needs a feature list and measurable operating promises; mixing them
makes neither reviewable.

| Type           | Requirement         | Testable statement                              |
| -------------- | ------------------- | ----------------------------------------------- |
| Functional     | Create a short code | `POST /urls` returns a unique code              |
| Functional     | Resolve a code      | `GET /{code}` redirects to the stored URL       |
| Non-functional | Read latency        | p99 redirect latency is below 200 ms            |
| Non-functional | Availability        | Redirects remain available during one node loss |

**Key takeaway**: Features describe behaviour; non-functional requirements set the constraints
that choose an architecture.

**Why It Matters**: Caching may satisfy a latency target but cannot define the redirect feature.
Putting both in a contract exposes the tension: cache misses, invalid URLs, and node loss must all
have an observable response. (co-02)

### Worked Example 2: Read a latency ladder

**Context**: Orders of magnitude prevent a local operation from being confused with a network call.

| Operation             | Approximate latency | Relative lesson                       |
| --------------------- | ------------------: | ------------------------------------- |
| L1 cache              |              0.5 ns | Keep hot data close                   |
| Main memory           |              100 ns | Fast, but finite                      |
| SSD random read       |              150 µs | Thousands of times slower than memory |
| Datacenter round trip |              500 µs | A remote dependency consumes a budget |
| Disk seek             |               10 ms | Avoid on a hot request path           |

**Key takeaway**: A latency budget is spent in units with radically different costs.

**Why It Matters**: The exact values vary by hardware; the gap does not. The table makes a cache
or batch request a reasoned response to an order-of-magnitude cost, not a ritual. (co-05)

### Worked Example 3: Use powers of two as a data ruler

**Context**: Storage estimates need a shared unit conversion before they can reveal a bottleneck.

| Power | Approximation | Design use            |
| ----- | ------------- | --------------------- |
| 2¹⁰   | 1 KB          | metadata record       |
| 2²⁰   | 1 MB          | image or page payload |
| 2³⁰   | 1 GB          | node memory slice     |
| 2⁴⁰   | 1 TB          | storage planning unit |

**Key takeaway**: Approximate binary units are adequate for an early capacity decision.

**Why It Matters**: A design need not predict bytes perfectly. It must distinguish a table that
fits in memory from one that needs object storage or sharding. (co-04)

### Worked Example 4: Estimate peak QPS

**Context**: One million daily users taking ten actions each gives an average that hides peaks.

`1,000,000 × 10 ÷ 86,400 ≈ 116 QPS; 10× peak factor = 1,160 peak QPS.`

**Key takeaway**: Estimate average first, then explicitly state the peak multiplier.

**Why It Matters**: The peak number tells the team whether one process, a load balancer, or a queue
is the first constraint. The multiplier remains an assumption to validate with production traffic.
(co-03)

### Worked Example 5: Estimate five-year storage

**Context**: A shortener writes 10 million 500-byte rows per day with 20% annual growth.

`10,000,000 × 500 ≈ 5 GB/day; 5 GB × 365 × (1 + 1.2 + 1.2² + 1.2³ + 1.2⁴) ≈ 13.6 TB before replicas.`

**Key takeaway**: Multiply record size, arrival rate, retention, and growth before choosing storage.

**Why It Matters**: Thirteen-point-six terabytes changes backup, index, and replication planning. A result is
useful precisely because it is approximate and can be recomputed when a premise changes. (co-03)

### Worked Example 6: Estimate bandwidth

**Context**: A read response of 1 KB at 1,160 peak QPS costs about 1.16 MB/s before protocol overhead.

`1,160 requests/s × 1 KB/request ≈ 1.16 MB/s.`

**Key takeaway**: Units should cancel from requests and bytes into bytes per second.

**Why It Matters**: Bandwidth can be cheap while latency or origin work is expensive. This estimate
stops a team from treating them as the same bottleneck. (co-03)

### Worked Example 7: Size for a read-heavy ratio

**Context**: A redirect service with 100 reads per write benefits from an intentionally high cache-hit target.

`100 reads : 1 write; at 99% hit rate, only 1 of every 100 reads reaches the database.`

**Key takeaway**: A read/write ratio connects traffic to a cache objective.

**Why It Matters**: The remaining one percent still defines database capacity and cache-miss
latency. A cache is an optimization with a miss path, not a replacement for durable storage. (co-03)

### Worked Example 8: Follow the design method

**Context**: A repeatable sequence prevents diagramming before constraints are known.

1. State requirements and assumptions.
2. Estimate QPS, storage, bandwidth, and latency budget.
3. Specify API and data model.
4. Draw the high-level request and data flow.
5. Identify the first bottleneck and selected mitigation.
6. Describe failures, consistency, and degradation.
7. Record explicit trade-offs and validation signals.

**Key takeaway**: Each step produces an artifact a reviewer can challenge.

**Why It Matters**: Skipping directly to components hides assumptions. The order keeps the design
reversible: new evidence can change a number, then a choice, without rewriting a fictional story.
(co-01)

### Worked Example 9: Sketch a URL API

**Context**: API shape defines idempotency, failure responses, and ownership before implementation.

| Endpoint      | Input                     | Success        | Failure                      |
| ------------- | ------------------------- | -------------- | ---------------------------- |
| `POST /urls`  | long URL, idempotency key | `201 {code}`   | `409` same key/different URL |
| `GET /{code}` | short code                | `302 Location` | `404` unknown code           |

**Key takeaway**: An endpoint contract names the client-visible result and error semantics.

**Why It Matters**: A generated code is not enough: retries must not create duplicate durable rows.
The contract supplies a concrete place to apply rate limiting and observability. (co-01)

### Worked Example 10: Sketch the lookup model

**Context**: Redirect reads need a key that directly serves the access pattern.

| Key               | Fields                        | Index and reason                        |
| ----------------- | ----------------------------- | --------------------------------------- |
| `short_code`      | long URL, created time, owner | primary/indexed; direct redirect lookup |
| `idempotency_key` | request hash, short code      | unique; safe create retry               |

**Key takeaway**: Model the dominant lookup before adding general-purpose fields.

**Why It Matters**: A missing index turns a simple redirect into a growing scan. The second key
shows that correctness constraints can be first-class data, not application folklore. (co-01)

### Worked Example 11: Allocate a latency budget

**Context**: A 200 ms p99 target has to survive each synchronous hop.

| Hop                       | Budget |
| ------------------------- | -----: |
| Load balancer and network |  25 ms |
| Application work          |  25 ms |
| Cache lookup              |  10 ms |
| Database miss path        | 100 ms |
| Headroom                  |  40 ms |

**Key takeaway**: The row total must fit the promised budget, including headroom.

**Why It Matters**: A downstream call with no budget silently consumes the whole SLO. A budget also
identifies which work must become asynchronous rather than blocking a request. (co-05)

### Worked Example 12: Translate availability nines

**Context**: Percentages become actionable when expressed as downtime.

| Availability | Approximate downtime/year |
| -----------: | ------------------------: |
|        99.9% |                8.76 hours |
|       99.99% |              52.6 minutes |
|      99.999% |              5.26 minutes |

**Key takeaway**: A service-level target is a budget for failure, not a decorative percentage.

**Why It Matters**: The table forces a conversation about maintenance, dependencies, and alerting.
It also prevents a casual “five nines” requirement from becoming an unpriced architectural demand.
(co-19)

### Worked Example 13: Compose availability

**Context**: Two 99.9% dependencies in series do not make a 99.9% user journey.

`0.999 × 0.999 = 0.998001`, or roughly 99.8% availability.

**Key takeaway**: Series dependencies multiply their availability.

**Why It Matters**: A critical path should have fewer dependencies, redundancy, or a graceful
fallback. This arithmetic is a reason to question synchronous fan-out before adding it. (co-19)

### Worked Example 14: Start with one tuned database

**Context**: A read-heavy product needs evidence before sharding.

| Observation         | First response           | Escalation trigger                           |
| ------------------- | ------------------------ | -------------------------------------------- |
| Slow repeated reads | index and cache          | miss path still exceeds SLO                  |
| Write saturation    | batch or optimize schema | measured write throughput exceeds one leader |
| Storage growth      | partition and archive    | maintenance window cannot meet recovery goal |

**Key takeaway**: A measured limit, not scale theatre, justifies the next distributed component.

**Why It Matters**: Sharding adds rebalancing and cross-shard query costs. A single Postgres instance
with a good schema is often the least risky design until its observed limits say otherwise. (co-26)

### Worked Example 15: Treat estimates as bets

**Context**: A capacity number should change a decision or be removed.

| Estimate              | Decision it informs          | Signal to revisit         |
| --------------------- | ---------------------------- | ------------------------- |
| 1,160 peak QPS        | cache capacity and LB target | peak exceeds 1,000 QPS    |
| 13.6 TB in five years | archive/object-store plan    | retained row size changes |
| 200 ms p99            | timeout budget               | p99 burn-rate alert       |

**Key takeaway**: An estimate is a falsifiable planning assumption.

**Why It Matters**: Precision theatre produces numbers without an owner. Tying each to a measured
signal makes the architecture adaptive rather than pretending its forecast is permanent. (co-03)

### Worked Example 16: Choose CAP behaviour

**Context**: During a partition, a ledger and a like counter have different acceptable failures.

| Workload     | Choice under partition | User-visible behaviour                         |
| ------------ | ---------------------- | ---------------------------------------------- |
| Bank ledger  | CP                     | reject or delay a conflicting write            |
| Like counter | AP                     | accept and reconcile a temporarily stale count |

**Key takeaway**: Partition tolerance is required in a distributed system; the choice is consistency
or availability while it occurs.

**Why It Matters**: CAP does not say a database is always CP or AP. A product operation selects a
failure response according to the harm caused by wrong versus unavailable information. (co-15)

### Worked Example 17: Add PACELC

**Context**: A key-value store may have no partition and still trade latency against coordination.

`Partition: choose Availability or Consistency. Else: choose lower Latency or stronger Consistency.`

**Key takeaway**: Normal operation has a cost too; replication coordination can add latency.

**Why It Matters**: PACELC stops “we handled CAP” from ending the design discussion. A team must
state whether ordinary reads wait for replicas and why that latency is acceptable. (co-16)

### Worked Example 18: Pick read-your-writes

**Context**: After a user edits a profile, the next read must not show their old display name.

`Write profile → route that session to leader or a caught-up replica → read profile.`

**Key takeaway**: Read-your-writes is a session guarantee, weaker and cheaper than global strong consistency.

**Why It Matters**: Eventual consistency can be correct for unrelated viewers yet confusing for the
writer. Naming the session rule lets a system apply extra coordination only where users expect it.
(co-17)
