# System Design (Annotated-concept, Python)

**Course ID**: `system-design` · **Format**: Annotated-concept · **Language**: Python.

**Short summary**: Designing systems for scale, availability

**Scope note**: designing systems at scale — the building blocks (load balancing, caching, sharding,
replication, queues, CDNs), the estimation/trade-off method, and worked case studies (URL shortener,
rate limiter, news feed). `*`: Python where a component is demonstrated runnably (e.g. a rate limiter,
a consistent-hashing ring), else annotated architecture diagrams. Single-service scaling depth is
[`39-backend-at-scale`](./backend-at-scale.md).

## Why this exists · the big idea

- **The problem before the solution**: "build a system that handles millions of users" has no single right
  answer — every building block (cache, shard, queue, replica) relieves one bottleneck by creating another,
  and the skill is choosing under uncertainty.
- **Keep-this-if-you-forget-everything**: start from the numbers — estimate load, find the bottleneck, reach
  for the specific block that relieves it, and say out loud what each choice gives up. Design is trade-off,
  not a checklist of components.
- **Big ideas touched**: `consistency-latency-throughput` (the axes every decision moves along),
  `correctness-vs-pragmatism` (capacity estimation is deliberate approximation, not precision),
  `abstraction-and-its-cost` (every building block buys scale and charges operational complexity).

## Prerequisites

- **Prior topics**: [topic 39 Backend at Scale](./backend-at-scale.md) (services, queues, caching),
  [topic 29 Advanced Networking](./advanced-networking.md) (latency, DNS, load balancing), and
  [topic 26 Advanced SQL](./advanced-sql-and-query-performance.md) (indexes, replication, sharding).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** for the runnable component demos; a
  Markdown/Mermaid editor for the architecture diagrams + capacity estimates (Neovim per DD-17).
- **Assumed knowledge**: how a single service scales (topic 39); back-of-the-envelope arithmetic; reading a
  latency/throughput number.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: no version/license-sensitive claims here. Capacity-estimation numbers (latency
  ladder, QPS/storage rules of thumb), consistent hashing, token-bucket/sliding-window rate limiting, and
  the canonical case studies (URL shortener, news feed) are evergreen CS fundamentals unchanged in years —
  nothing time-sensitive to correct.

> DD-35 primary-source pass (2026-07-12). Numbers traced to their original sources and fetched/read.
> Where a figure is a mathematical identity (powers of two, nines arithmetic) it is independently
> checkable. Unverifiable specifics flagged `[Needs Verification]`.

- **Latency ladder** — the canonical figures (L1 0.5 ns, branch mispredict 5 ns, L2 7 ns, mutex 25 ns, main
  memory 100 ns, compress 1 KB with Snappy/**Zippy** ~3 µs, send 1 KB over 1 Gbps ~10 µs, SSD **4 KB** random
  read ~150 µs, read 1 MB sequentially from memory ~250 µs, same-datacenter round trip ~500 µs, disk seek
  ~10 ms, read 1 MB from disk ~20 ms, CA↔Netherlands round trip ~150 ms) trace to **Jeff Dean** (attributed,
  extending **Peter Norvig**'s original list). Source: [Latency Numbers Every Programmer Should Know (jboner gist)](https://gist.github.com/jboner/2841832) header "~2012", cross-checked against [norvig.com/21-days.html#answers](https://www.norvig.com/21-days.html#answers). Caveat: the live gist has been edited to add
  speculative "2026 LLM" rows — **cite a frozen mirror**, and the classic rows only. Snappy "was previously
  called 'Zippy'" per [Google Snappy README](https://github.com/google/snappy/blob/main/README.md).
- **Powers of two** — 2¹⁰≈1 KB, 2²⁰≈1 MB, 2³⁰≈1 GB, 2⁴⁰≈1 TB, 2⁵⁰≈1 PB. Mathematical identities;
  presentation follows [ByteByteGo — Back-of-the-Envelope Estimation](https://bytebytego.com/courses/system-design-interview/back-of-the-envelope-estimation) (Alex Xu).
- **Consistent hashing** — keys spread roughly uniformly; adding/removing a bucket remaps only a proportional
  fraction of keys. Source: Karger, Lehman, Leighton, Panigrahy, Levine, Lewin, "Consistent Hashing and Random
  Trees," **STOC '97**. Citation `[Verified]` (ACM DL / DBLP); verbatim abstract `[Needs Verification]`
  (PDF unparseable to fetch tool). [ACM DL](https://dl.acm.org/doi/10.1145/258533.258660).
- **Caching** — cache-aside = "populate the cache only when an object is actually requested"; LRU eviction;
  cache stampede / "dog piling" mitigated by pre-warming and TTL **jitter**. Source: [AWS — Caching Best Practices](https://aws.amazon.com/caching/best-practices/) (fetched).
- **Replication & sharding** — leader-based: "writes are only accepted on the leader (the followers are
  read-only)"; range vs hash partitioning; **federation** = functional/Y-axis split (AKF Scale Cube). Sources:
  Kleppmann, _DDIA_ (2017) chs. 5–6 (`[Needs Verification]` at fetch level — copyrighted, corroborated by
  convergent quoted summaries); [AKF Partners — Splitting Databases for Scale](https://akfpartners.com/growth-blog/splitting-databases-for-scale).
- **CAP** — "consistency, availability, and partition tolerance … It is impossible to achieve all three."
  Source: Gilbert & Lynch, "Brewer's Conjecture…," **ACM SIGACT News** 33(2), 2002 ([PDF](https://www.cs.princeton.edu/courses/archive/spr22/cos418/papers/cap.pdf)). Abstract `[Verified]` via convergent citation; direct PDF render `[Needs Verification]`.
- **PACELC** — under a **P**artition trade **A** vs **C**; **E**lse (no partition) trade **L**atency vs **C**.
  Source: Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design," **IEEE Computer** 45(2), 2012. Exact wording `[Needs Verification]` (paywalled); formulation corroborated by [Wikipedia PACELC](https://en.wikipedia.org/wiki/PACELC_design_principle) citing the original.
- **Consistency models** — causal: "causally-related operations … appear in the same order on all
  processes"; read-your-writes: "a subsequent read r … must observe w's effects" (single session). Source:
  [Jepsen — Consistency Models](https://jepsen.io/consistency) (fetched, verbatim). "Eventual consistency"
  exact definition `[Needs Verification]` (not directly fetched this pass; community sense = replicas
  converge absent new writes, per Vogels ACM Queue 2008).
- **Quorum (Dynamo N/W/R)** — R + W > N yields quorum-like consistency; Dynamo uses a "sloppy quorum" over
  the first N healthy nodes. Source: DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store,"
  **SOSP '07** ([PDF](https://www.cs.cornell.edu/courses/cs5414/2017fa/papers/dynamo.pdf)). Mechanism `[Verified]` via convergent course sources; verbatim quote `[Needs Verification]`.
- **Availability "nines"** — 99% = 3.65 days/yr, 99.9% = 8.76 h/yr, 99.99% = 52.6 min/yr, 99.999% =
  5.26 min/yr. Source: [Google SRE Book, Availability Table](https://sre.google/sre-book/availability-table/) (fetched, exact).
- **Kafka** — "Topics are partitioned … spread over a number of 'buckets' … on different Kafka brokers";
  offset is "a single integer"; ordering guaranteed **only within a partition**. Source: [Apache Kafka — Introduction](https://kafka.apache.org/intro) (fetched). Consumer-group semantics corroborated via [Confluent docs](https://docs.confluent.io/kafka/design/consumer-design.html) (kafka.apache.org's own page is JS-rendered, unfetchable).
- **Rate limiting** — Stripe uses a **token bucket** with per-user Redis buckets; tokens drip back over time,
  requests rejected when empty. Source: [Stripe — Scaling your API with rate limiters](https://stripe.com/blog/rate-limiters) (2017, fetched).
- **Circuit breaker** — "monitors for failures. Once the failures reach a certain threshold, the circuit
  breaker trips, and all further calls … return with an error." Source: [Fowler — CircuitBreaker](https://martinfowler.com/bliki/CircuitBreaker.html) (attributes popularization to Nygard, _Release It!_).
- **API gateway** — "a single entry point into the application, routing and composing requests to services …
  reduces the number of requests/roundtrips." Source: [microservices.io — API Gateway](https://microservices.io/patterns/apigateway.html) (Chris Richardson, fetched).
- **Interview framework** — 4 steps: (1) outline use cases/constraints/assumptions, (2) high-level design,
  (3) design core components, (4) scale the design. Source: [Donne Martin — system-design-primer](https://github.com/donnemartin/system-design-primer) (fetched).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept topic). Each example below cites the co-NN it exercises. -->

- **co-01 · design-method** — the repeatable order: requirements → capacity estimate → API → data model → high-level design → bottlenecks → trade-offs.
- **co-02 · functional-vs-nonfunctional** — separate what the system does (features) from how well (latency, availability, scale, durability).
- **co-03 · back-of-envelope-estimation** — estimate QPS, storage, and bandwidth to _find the bottleneck_, not to forecast the future.
- **co-04 · powers-of-two** — 2¹⁰/2²⁰/2³⁰/2⁴⁰ ≈ KB/MB/GB/TB; the ruler for data-volume math.
- **co-05 · latency-ladder** — the Dean/Norvig latency numbers (cache → memory → SSD → disk → cross-continent) that anchor a latency budget.
- **co-06 · load-balancing** — spread requests across servers (round-robin, weighted, least-connections).
- **co-07 · consistent-hashing** — a hash ring that remaps only a proportional fraction of keys when a node joins/leaves (Karger 1997).
- **co-08 · caching-strategies** — cache-aside (lazy population), LRU eviction, TTL expiry.
- **co-09 · cache-stampede** — a thundering herd of simultaneous misses; mitigated by pre-warming and TTL jitter.
- **co-10 · cdn** — geographically distributed edge caches serving static assets close to users.
- **co-11 · replication** — leader/follower: writes go to the leader, reads fan out to read-only followers (with replication lag).
- **co-12 · sharding-partitioning** — split data across nodes by range (scannable, hot-spot-prone) or hash (even, order-losing).
- **co-13 · hotspot-problem** — skewed load on a "celebrity" key; mitigated by salting/splitting the key.
- **co-14 · federation** — functional/Y-axis partitioning: split databases by service/feature (AKF Scale Cube).
- **co-15 · cap-theorem** — under a network partition you cannot have both consistency and availability (Gilbert & Lynch 2002).
- **co-16 · pacelc** — extends CAP: on Partition trade A vs C; Else trade Latency vs Consistency (Abadi 2012).
- **co-17 · consistency-models** — strong/linearizable, eventual, causal, and read-your-writes as distinct guarantees.
- **co-18 · quorum** — N replicas, W write / R read votes; R + W > N gives quorum-like consistency (Dynamo).
- **co-19 · availability-nines** — 99.9% = 8.76 h/yr, 99.99% = 52.6 min/yr, 99.999% = 5.26 min/yr; series availability multiplies.
- **co-20 · message-queue** — asynchronous decoupling of producers and consumers; competing consumers spread work.
- **co-21 · event-streaming** — a durable, replayable log (Kafka topic/partition/offset); ordering holds only within a partition.
- **co-22 · rate-limiting** — token-bucket / sliding-window shedding of excess requests (Stripe's Redis token bucket).
- **co-23 · idempotency** — at-least-once delivery plus an idempotent consumer (dedup by processed-id) approximates exactly-once.
- **co-24 · designing-for-failure** — redundancy, failover, graceful degradation, and circuit breakers keep a system up under partial failure.
- **co-25 · backpressure** — a bounded queue rejects or slows intake under overload instead of collapsing.
- **co-26 · sql-vs-nosql-at-scale** — relational for joins/transactions; document/wide-column for scale and denormalized access.
- **co-27 · microservices-vs-monolith** — service decomposition with an API gateway as the single entry point, traded against operational complexity.
- **co-28 · blob-object-storage** — object stores (+ presigned URLs) for large static assets, fronted by a CDN.
- **co-29 · case-study-method** — apply the whole method to canonical designs (URL shortener, news feed, rate limiter).
- **co-30 · communicating-a-design** — a design is diagrams + capacity numbers + explicit named trade-offs, not just a box drawing.

## Tensions & trade-offs — when NOT to reach for this

- **Estimation is a bet, not a prediction**: back-of-envelope numbers guide the design but are wrong by
  design. Treating them as precise (over-provisioning for imagined scale) wastes money and complexity;
  ignoring them entirely designs blind. Estimate to _find the bottleneck_, not to forecast the future.
- **Every block cuts both ways**: a cache adds staleness, a shard adds cross-shard queries and rebalancing,
  a queue adds eventual consistency and ordering headaches, a replica adds replication lag. No building
  block only helps.
- **When NOT to scale**: a single well-tuned Postgres serves further than most designs admit. Reach for
  sharding, a CDN, or multi-region when a _measured_ limit forces it, not because the diagram looks bigger.

## Lineage — why it beat the alternative

- The system-design canon crystallized when the big web companies published how they scaled — Dynamo (2007;
  eventual consistency + consistent hashing), MapReduce, and the CAP theorem (Brewer 2000) formalizing that
  you cannot have consistency, availability, and partition tolerance all at once. It became interview ritual
  because it compresses decades of scaling scars into a repeatable method: numbers → bottleneck → trade-off.
  The durable lesson isn't the specific blocks but the discipline of making the trade-off explicit — the same
  judgment [`39-backend-at-scale`](./backend-at-scale.md) applies to one service and
  [`42-software-architecture`](./software-architecture.md) applies to boundaries.

## Worked examples

Colocated under `system-design/learning/`; each example is either a runnable, type-annotated `pyright`-clean
Python component (DD-20/DD-30) **or** an annotated design artifact (Mermaid architecture, capacity table,
decision table) per the `*` Annotated-concept designation. Contiguous `ex-01..ex-53`. Every example cites
the `co-NN` it exercises; concepts are taught before the examples that use them.

### Beginner

- **ex-01 · requirements-split** — separate functional from non-functional requirements for a URL shortener — verify each requirement is labelled and testable. (co-02)
- **ex-02 · latency-ladder-table** — annotate the Dean/Norvig latency table with orders of magnitude — verify each row's relative multiplier. (co-05)
- **ex-03 · powers-of-two-table** — the 2¹⁰..2⁴⁰ → KB/MB/GB/TB conversion table — verify each identity arithmetically. (co-04)
- **ex-04 · qps-estimate** — estimate peak QPS from DAU × actions/day ÷ seconds, with a peak factor — verify the arithmetic. (co-03)
- **ex-05 · storage-estimate** — estimate 5-year storage for a shortener (rows × bytes × growth) — verify the total is arithmetic-checked. (co-03)
- **ex-06 · bandwidth-estimate** — estimate read/write bandwidth from QPS × payload — verify units cancel to MB/s. (co-03)
- **ex-07 · read-write-ratio** — compute a 100:1 read:write ratio and size the cache accordingly — verify the cache-hit target follows. (co-03)
- **ex-08 · design-method-checklist** — the seven-step method as an annotated checklist — verify each step names its output artifact. (co-01)
- **ex-09 · api-sketch** — sketch the REST API (`POST /urls`, `GET /{code}`) for a shortener — verify each endpoint's contract. (co-01)
- **ex-10 · data-model-sketch** — a `short_code → long_url` schema with an index — verify the lookup key is indexed. (co-01)
- **ex-11 · latency-budget** — allocate a 200 ms budget across LB → app → cache → DB hops — verify the sum fits the budget. (co-05)
- **ex-12 · availability-nines-table** — downtime-per-year for each nines level — verify each figure against the SRE table. (co-19)
- **ex-13 · availability-composition** — two 99.9% services in series → ~99.8% — verify the product. (co-19)
- **ex-14 · single-postgres-first** — argue one tuned Postgres serves before sharding — verify the measured-limit trigger is named. (co-26)
- **ex-15 · estimate-as-bet** — annotate why estimates find bottlenecks, not forecasts — verify each number is tied to a decision. (co-03)
- **ex-16 · cap-choose** — pick CP vs AP for a bank ledger vs a like-counter — verify each choice names its partition behaviour. (co-15)
- **ex-17 · pacelc-annotate** — annotate the no-partition latency/consistency trade-off for a KV store — verify the Else branch is stated. (co-16)
- **ex-18 · consistency-model-pick** — pick read-your-writes for a profile edit — verify why eventual would confuse the user. (co-17)

### Intermediate

- **ex-19 · round-robin-lb** — a round-robin load balancer in Python — verify requests cycle evenly across backends. (co-06)
- **ex-20 · weighted-lb** — weighted distribution favouring larger backends — verify the ratio matches weights. (co-06)
- **ex-21 · consistent-hashing-ring** — a hash ring; add/remove a node — verify only a bounded fraction of keys move. (co-07)
- **ex-22 · consistent-hashing-vnodes** — virtual nodes smooth the distribution — verify per-node load variance drops. (co-07)
- **ex-23 · cache-aside** — a cache-aside read path (miss → load → populate) — verify the second read hits the cache. (co-08)
- **ex-24 · lru-cache** — an LRU cache with capacity eviction — verify the least-recently-used entry is evicted. (co-08)
- **ex-25 · ttl-cache** — a TTL cache expiring stale entries — verify an expired key misses. (co-08)
- **ex-26 · cache-stampede-jitter** — add randomized jitter to TTLs — verify expiries spread instead of clustering. (co-09)
- **ex-27 · token-bucket-limiter** — a token-bucket limiter — verify it admits up to the limit and rejects beyond. (co-22)
- **ex-28 · sliding-window-limiter** — a sliding-window counter limiter — verify boundary requests are counted correctly. (co-22)
- **ex-29 · leader-follower-replication** — simulate leader→follower with lag — verify a follower read can be stale. (co-11)
- **ex-30 · read-replica-routing** — route reads to replicas, writes to the leader — verify writes never hit a replica. (co-11)
- **ex-31 · range-partition** — range sharding that produces a hotspot on sequential keys — verify the skew appears. (co-12, co-13)
- **ex-32 · hash-partition** — hash sharding spreads keys evenly — verify per-shard counts are near-equal. (co-12)
- **ex-33 · hotspot-salting** — salt a celebrity key across sub-partitions — verify load spreads. (co-13)
- **ex-34 · quorum-rw** — an N/W/R quorum with R + W > N — verify a read always sees the latest committed write. (co-18)
- **ex-35 · message-queue-decouple** — a producer/consumer queue — verify the producer does not block on the consumer. (co-20)
- **ex-36 · queue-competing-consumers** — work spread round-robin across consumers — verify each processes a fair share. (co-20)
- **ex-37 · idempotent-consumer** — dedup by a processed-message-id set — verify a redelivered message is a no-op. (co-23)
- **ex-38 · cdn-cache-annotate** — annotate an origin + edge-cache CDN diagram — verify the cache-hit path skips the origin. (co-10)

### Advanced

- **ex-39 · url-shortener-design** — a full annotated design (requirements + estimate + API + model + Mermaid) — verify the diagram matches the API and the numbers are checked. (co-01, co-29)
- **ex-40 · url-shortener-id-generation** — base62 encoding + collision handling for short codes — verify generated codes are unique and short. (co-01)
- **ex-41 · news-feed-design** — fan-out-on-write vs fan-out-on-read, annotated with the trade-off — verify each approach names its cost. (co-29)
- **ex-42 · feed-celebrity-problem** — a hybrid fan-out for high-follower accounts — verify the celebrity path avoids write amplification. (co-13)
- **ex-43 · rate-limiter-design** — a distributed rate limiter design (Redis-backed token bucket) — verify it enforces a shared limit across nodes. (co-22)
- **ex-44 · circuit-breaker** — a circuit breaker (closed → open → half-open) in Python — verify it trips after the failure threshold. (co-24)
- **ex-45 · graceful-degradation** — shed non-essential features under load — verify the core path still responds. (co-24)
- **ex-46 · backpressure** — a bounded queue that rejects when full — verify producers get a fast rejection, not OOM. (co-25)
- **ex-47 · failover-annotate** — annotate leader failover and the split-brain risk — verify the fencing mechanism is named. (co-24)
- **ex-48 · sql-vs-nosql-decision** — a decision table for a workload (joins vs scale) — verify each row justifies its pick. (co-26)
- **ex-49 · microservices-gateway** — an API gateway routing/composing to services — verify one client call fans out to several services. (co-27)
- **ex-50 · event-streaming-partition** — an annotated Kafka topic/partition/offset diagram — verify ordering is claimed only within a partition. (co-21)
- **ex-51 · blob-storage-design** — object storage + a presigned-URL upload path — verify the large asset never transits the app server. (co-28)
- **ex-52 · system-design-capstone** — assemble requirements → estimate → API → model → Mermaid → trade-offs plus a runnable rate limiter and consistent-hashing ring — verify checked numbers, a coherent diagram, passing components, and explicit trade-offs. (co-01, co-03, co-07, co-22, co-24, co-30)
- **ex-53 · federation-split** — split one database into per-service databases (AKF Y-axis) — verify each service owns its own store and cross-service joins become API calls. (co-14)

## Capstone spec — intra-topic (subject → design artifact + runnable components)

- **Goal**: produce a complete system design for one non-trivial system (e.g. a news feed or URL
  shortener) — requirements, capacity estimation, API, data model, a high-level architecture diagram, and
  a trade-off/bottleneck analysis — and back it with two runnable Python components (a rate limiter and a
  consistent-hashing ring) that prove the load-shedding and partitioning mechanics.
- **Concepts exercised**: [ ] capacity estimation (co-03, co-04, co-05) [ ] API + data model design
  (co-01) [ ] a high-level architecture diagram (co-30) [ ] a runnable rate limiter (co-22) [ ] a runnable
  consistent-hashing ring (co-07) [ ] an explicit trade-off/bottleneck analysis (co-24, co-30).
- **Ordered steps**:
  1. `.../learning/capstone/design.md` — requirements + capacity estimate + API + data model + a Mermaid
     architecture. Verify the capacity numbers are arithmetic-checked and the diagram matches the API.
  2. `.../learning/capstone/code/rate_limiter.py` — a token-bucket limiter with tests. Verify it admits up
     to the limit and rejects beyond it.
  3. `.../learning/capstone/code/hashing.py` — a consistent-hashing ring with tests. Verify adding/removing
     a node moves only a bounded fraction of keys.
  4. `design.md` trade-off section — bottlenecks + failure modes + graceful degradation. Verify each
     trade-off names what is gained and what is given up.
- **Acceptance criteria**: the design has checked capacity numbers, a coherent API + data model + diagram,
  two runnable components with passing tests, and an explicit trade-off analysis.
- **Done bar**: design artifact complete + components runnable + web-verified.

## Read more

**Books**

- **Designing Data-Intensive Applications** — Martin Kleppmann (2017). The definitive modern text connecting distributed systems theory to practical large-scale system design.
- **System Design Interview: An Insider's Guide** — Alex Xu (2020). The most widely used practical primer for the system-design-interview canon.
- **Web Scalability for Startup Engineers** — Artur Ejsmont (2015). Practical treatment of scaling patterns (load balancing, caching, sharding) for growing systems.

**Papers & articles**

- **MapReduce: Simplified Data Processing on Large Clusters** — Jeffrey Dean, Sanjay Ghemawat (2004), OSDI. The paper that popularized the batch-processing model underlying much of large-scale system design. <https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/>
- **The Google File System** — Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung (2003), SOSP. Canonical paper describing the distributed storage design that inspired HDFS and much of big-data infrastructure. <https://research.google/pubs/the-google-file-system/>
- **Dynamo: Amazon's Highly Available Key-value Store** — Giuseppe DeCandia et al. (2007), SOSP. Foundational paper behind eventually-consistent, partitioned key-value stores (Cassandra, Riak, DynamoDB). <https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Architecture, distributed & internals builds — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Architecture, distributed & internals builds — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 7 · Networking, architecture & distributed systems.

> _Content originated in the now-closed FS-SE plan (topic 44); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
