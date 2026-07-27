---
title: "Overview"
date: 2026-07-27T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the NoSQL Databases topic: recall first, then applied
judgment, then a hands-on kata, then a self-check checklist, then elaborative-interrogation prompts
that ask _why_, not just _what_. Every answer is hidden in a `<details>` block; try each item yourself
before opening it.

Every kata below is self-contained and deterministic -- hand-constructed fixtures only, no live
database connection, no Docker container, and no dependency on this topic's own worked-example or
capstone code.

## Recall Q&A

Thirty-six short-answer questions, one per concept (`co-01` through `co-36`). Answer from memory, then
check.

**Q1 (co-01 -- NoSQL family taxonomy).** What distinguishes the key-value, document, wide-column, and
time-series families from each other, and which family is deliberately excluded from this topic?

<details>
<summary>Answer</summary>

Each family optimizes a different access shape: key-value for single-key lookups, document for
nested, self-describing records read as a whole, wide-column for partition-scoped rows ordered by a
clustering key, and time-series for append-heavy, timestamp-keyed range scans. Graph databases are
deliberately excluded -- they are their own sibling topic (`graph-databases`), not a NoSQL family this
topic covers.

</details>

**Q2 (co-02 -- when NoSQL vs. relational).** What should actually drive a NoSQL-vs-relational choice,
rather than "NoSQL is newer" or "NoSQL scales better" as a blanket claim?

<details>
<summary>Answer</summary>

The access pattern, the horizontal-scale need, and the consistency the application can actually
tolerate. A relational store's joins-plus-ACID default is the right choice for many workloads; NoSQL
earns its place only when one of those three specifically does not fit -- not by default, and not
because a name sounds more modern.

</details>

**Q3 (co-03 -- CAP theorem).** What does the CAP theorem actually force a distributed system to trade,
and under what condition?

<details>
<summary>Answer</summary>

Under a network partition, a distributed system must trade consistency for availability -- it cannot
guarantee both. This is Gilbert & Lynch's 2002 formal proof of Brewer's original conjecture: a
partitioned node can either refuse to answer (favoring consistency) or answer with possibly-stale data
(favoring availability), but not both at once.

</details>

**Q4 (co-04 -- PACELC extension).** What does PACELC add that CAP alone does not cover?

<details>
<summary>Answer</summary>

CAP only describes the trade-off DURING a partition. PACELC (Abadi, 2010) adds the ELSE branch: even
with no partition at all, a distributed system still trades latency for consistency on every normal
operation -- a synchronous, consistency-favoring write is slower than an asynchronous,
latency-favoring one, partition or not.

</details>

**Q5 (co-05 -- BASE vs. ACID).** What does BASE stand for, and why do many NoSQL stores default to it
instead of ACID?

<details>
<summary>Answer</summary>

Basically Available, Soft state, Eventually consistent. Many NoSQL stores default to BASE because
guaranteeing full ACID (especially cross-node isolation and durability) at scale costs coordination
latency that conflicts with the availability and horizontal-scale goals those stores were built for --
BASE is a deliberately looser contract traded for those goals, not an oversight.

</details>

**Q6 (co-06 -- eventual consistency).** What does "eventual consistency" promise, and what does it
explicitly NOT promise?

<details>
<summary>Answer</summary>

It promises that replicas converge to the same value over time, given no new writes. It explicitly
does NOT promise synchronous coordination on every write, or that a read immediately after a write on
a different replica returns the latest value -- a reader can observe a stale value for some window
before convergence completes.

</details>

**Q7 (co-07 -- tunable consistency / quorum).** What do R, W, and N control, and how does a client use
them to choose a consistency level per operation?

<details>
<summary>Answer</summary>

N is the number of replicas a piece of data is stored on; R and W are how many replicas must
acknowledge a read or write, respectively, for that one operation to succeed. A client dials
consistency versus latency per call by choosing R and W -- read/write at ONE for low latency and
weaker consistency, or at QUORUM (or ALL) for stronger consistency at the cost of waiting on more
replicas.

</details>

**Q8 (co-08 -- access-pattern-first modeling).** What does "design the schema from the queries" mean
in practice, and what does it replace?

<details>
<summary>Answer</summary>

It means naming the application's actual dominant reads and writes FIRST, then shaping documents,
partition keys, and indexes specifically to serve those named patterns efficiently. It replaces
starting from a normalized entity-relationship diagram and hoping the queries fall out naturally --
that relational-first instinct produces a schema optimized for data integrity, not for the specific
reads a NoSQL store will actually serve.

</details>

**Q9 (co-09 -- denormalization and aggregates).** What does embedding related data into one aggregate
buy, and what does it cost?

<details>
<summary>Answer</summary>

It buys read speed: the common read becomes a single fetch of one document or row instead of a join
across multiple tables. It costs write-side duplication -- the same fact now lives in multiple places,
so a write that changes it must update every copy, and an inconsistency between copies becomes
possible if that update is incomplete.

</details>

**Q10 (co-10 -- partition/sharding keys).** What makes a partition key choice good or bad, and what is
the failure mode of a bad one?

<details>
<summary>Answer</summary>

A good partition key distributes rows, documents, or items EVENLY across nodes, so no single node
carries disproportionate load. A bad choice -- one with low cardinality, or one that concentrates
writes on a single popular value (a celebrity user ID, a single "global" counter key) -- creates a hot
partition: one node absorbs far more traffic than its peers, becoming a bottleneck the rest of the
cluster cannot help with.

</details>

**Q11 (co-11 -- consistent hashing).** What problem does consistent hashing solve that plain modulo
hashing does not?

<details>
<summary>Answer</summary>

Plain modulo hashing (`hash(key) % node_count`) remaps NEARLY EVERY key when a node is added or
removed, because `node_count` itself changed. Consistent hashing places both nodes and keys on a hash
ring, so adding or removing one node only remaps the keys that fall in that node's own small arc of
the ring -- the Dynamo paper's own technique for minimizing data movement during cluster resize.

</details>

**Q12 (co-12 -- leader-follower replication).** How does leader-follower replication route writes and
reads, and what happens on leader failure?

<details>
<summary>Answer</summary>

One leader accepts and orders every write; followers replicate the leader's write stream and can
serve reads (at the cost of some replication lag). On leader failure, a follower is promoted to become
the new leader -- failover -- and the cluster resumes accepting writes through the newly promoted
leader.

</details>

**Q13 (co-13 -- leaderless replication).** How does leaderless replication differ from leader-follower,
and how does it reconcile conflicting results?

<details>
<summary>Answer</summary>

Any replica can accept a write directly -- there is no single leader coordinating write order. A
client's read or write then targets a QUORUM of replicas (per co-07's R/W/N), and the client or
coordinator reconciles whatever the queried replicas return, the Dynamo-style approach that trades a
single point of write coordination for the read/write quorum doing the reconciling instead.

</details>

**Q14 (co-14 -- LWW conflict resolution).** How does last-write-wins pick a winner among concurrent
writes, and what is its silent cost?

<details>
<summary>Answer</summary>

LWW compares the timestamp attached to each concurrent write and keeps the one with the latest
timestamp, discarding the rest. Its silent cost is exactly that discarding: the losing write's data is
gone with no merge, no conflict flag, and no chance for the application to reconcile the two updates --
whichever write happened to have the later clock value wins, even if that is purely an artifact of
clock skew.

</details>

**Q15 (co-15 -- vector clocks).** What do vector clocks detect that LWW cannot, and what do they
explicitly NOT do?

<details>
<summary>Answer</summary>

Vector clocks detect whether two writes are causally ordered (one happened strictly after the other,
so it should win outright) or CONCURRENT (neither happened-before the other, so which one is "correct"
is genuinely ambiguous). What vector clocks explicitly do NOT do is resolve the conflict themselves --
they surface it, leaving the application to decide how to merge two concurrent, causally-unordered
updates.

</details>

**Q16 (co-16 -- CRDTs).** What do CRDTs guarantee that makes them different from vector-clock-flagged
conflicts an application must resolve by hand?

<details>
<summary>Answer</summary>

Conflict-free replicated data types are designed so that concurrent updates merge DETERMINISTICALLY,
with no application-level conflict-resolution code required at all -- a G-counter's merge is always
"take the max per replica," a set union is always "union both sets." The structure of the data type
itself guarantees the merge is well-defined and produces the same result regardless of merge order.

</details>

**Q17 (co-17 -- secondary indexes in NoSQL).** Why does adding a secondary index in a distributed
NoSQL store cost more than adding one in a single-node relational database?

<details>
<summary>Answer</summary>

In a distributed, partitioned store, a secondary index (one not on the partition key) either has to
be maintained across every partition on every write, or a query using it has to fan out to every
partition at read time -- both add coordination cost a single-node relational index never has to pay,
because a single-node index update never needs cross-node coordination in the first place.

</details>

**Q18 (co-18 -- MongoDB document model / schema-on-read).** What does "schema-on-read" mean for a BSON
document, and what is the tradeoff?

<details>
<summary>Answer</summary>

No schema is enforced by the engine at write time by default -- two documents in the same collection
can have entirely different fields. "Schema-on-read" means the READER is responsible for interpreting
whatever shape it finds, which buys flexibility to evolve document shape without a migration, at the
cost of pushing shape-validation responsibility into application code (or an optional schema validator)
instead of the database engine.

</details>

**Q19 (co-19 -- MongoDB aggregation pipeline).** What does the aggregation pipeline let a query do that
a plain `find()` cannot?

<details>
<summary>Answer</summary>

The aggregation pipeline is a staged, server-side sequence of operators (`$match`, `$group`,
`$lookup`, and others) that transforms, groups, and even joins documents entirely on the server,
returning only the final, already-computed result. A plain `find()` returns raw documents the client
must then filter, group, or join itself -- the aggregation pipeline moves that work server-side instead
of pulling raw data across the network first.

</details>

**Q20 (co-20 -- Redis data structures).** What is the practical benefit of Redis exposing typed
structures (strings, lists, hashes, sets, sorted sets) as first-class operations, rather than storing
everything as an opaque blob?

<details>
<summary>Answer</summary>

Typed structures let the SERVER perform structure-aware operations atomically and efficiently --
appending to a list, incrementing a hash field, or reading a sorted set's top N members all happen
server-side in one round trip. Storing everything as an opaque blob would force the client to fetch
the whole blob, deserialize it, mutate it, and write the whole thing back, losing both atomicity and
efficiency.

</details>

**Q21 (co-21 -- Redis: cache vs. store).** What changes when the SAME Redis engine is configured as a
disposable cache versus a durable primary store?

<details>
<summary>Answer</summary>

As a cache: TTL-based eviction is the norm, and losing the data on a crash is acceptable because it
can be recomputed or re-fetched from the system of record. As a durable store: persistence (RDB
snapshots and/or AOF write-ahead logging) is tuned so data survives a restart or crash, because there
is no other system of record to fall back on -- the engine is identical, but the durability
configuration and the acceptable-loss assumption are opposite.

</details>

**Q22 (co-22 -- wide-column partition/clustering keys).** How do Cassandra and DynamoDB each structure
a row or item using two kinds of keys, and what does each key control?

<details>
<summary>Answer</summary>

A partition key determines WHICH node (or partition) a row or item lives on -- all rows sharing a
partition key land together. Within that one partition, a clustering key (Cassandra) or sort key
(DynamoDB) determines the ORDER rows are physically stored and read back in -- which is why a
partition-scoped, clustering-ordered read is cheap, while a query that does not name the partition key
is not.

</details>

**Q23 (co-23 -- DynamoDB single-table design).** What is single-table design, and what should drive the
decision to overload key prefixes for multiple entity types?

<details>
<summary>Answer</summary>

Single-table design stores multiple different entity types (e.g., users, orders, products) in ONE
physical DynamoDB table, distinguishing them via deliberately overloaded partition-key and sort-key
prefixes (e.g., `USER#123` vs. `ORDER#456`). The decision to do this should be driven entirely by the
application's own NAMED access patterns -- which entities need to be fetched together in one query --
not applied reflexively as a DynamoDB "best practice" independent of what the application actually
reads.

</details>

**Q24 (co-24 -- time to live).** What does a TTL attribute do, and which store used in this topic
relies on it as its ONLY built-in expiry mechanism?

<details>
<summary>Answer</summary>

A TTL attribute marks an item or key for automatic deletion once a stated expiry time passes, freeing
the application from writing an explicit cleanup job. Cassandra relies on per-row TTL as its own
CLOSEST built-in equivalent to retention -- unlike TimescaleDB's dedicated retention-policy mechanism
(co-30), Cassandra has no store-level retention concept beyond per-row TTL.

</details>

**Q25 (co-25 -- LSM-tree vs. B-tree and amplification).** What write path does an LSM-tree use, and
what does it trade for write throughput?

<details>
<summary>Answer</summary>

Writes land first in an in-memory memtable, which is periodically flushed to an immutable on-disk
SSTable; a background compaction process later merges SSTables to reclaim space and bound the number a
read must check. This append-only path buys high write throughput (writes never do an in-place disk
seek) at the cost of write amplification (compaction rewrites the same logical bytes multiple times)
and read amplification (a read may need to check several SSTables before finding the latest value) --
a B-tree's in-place updates avoid both amplifications but pay a random-seek cost per write instead.

</details>

**Q26 (co-26 -- polyglot persistence).** What does polyglot persistence mean, and why is it not the
same as "use whichever database is trendy for each service"?

<details>
<summary>Answer</summary>

Polyglot persistence means DELIBERATELY using different stores for different services or access
patterns within one system, because no single engine serves every access pattern well. It is not the
same as picking a trendy database per service arbitrarily -- the "deliberately" is load-bearing: each
store choice should trace back to that service's own access pattern and consistency needs (co-08,
co-02), not to novelty.

</details>

**Q27 (co-27 -- multi-item transactions).** What did adding multi-item transactions to NoSQL stores
change, and what does it still cost?

<details>
<summary>Answer</summary>

It let a NoSQL store guarantee ACID-style atomicity and isolation across MULTIPLE keys, documents, or
rows in one operation -- something the earliest NoSQL stores explicitly did not offer, single-item
writes only. It still costs latency: coordinating a multi-item transaction requires more cross-node
agreement than a single-item write, so it is reached for only when the access pattern genuinely
requires atomicity across more than one item, not by default.

</details>

**Q28 (co-28 -- license awareness).** Why does checking a NoSQL product's license count as a real
engineering step, not paperwork?

<details>
<summary>Answer</summary>

Because the license determines what you are actually allowed to do with the software -- a
source-available, non-OSI-approved license like MongoDB's SSPLv1 carries real obligations (extending
copyleft to any "as a service" offering built around the software) that a permissive license like
Apache-2.0 or BSD-3-Clause does not. Adopting a store without checking this (DD-15) risks a legal and
architectural surprise discovered only after the store is already load-bearing in production.

</details>

**Q29 (co-29 -- time-series data model).** What makes a time-series store's data model different from a
general-purpose store's, and what read shape dominates?

<details>
<summary>Answer</summary>

Time is the PRIMARY axis the storage engine itself is organized around (chunk/partition boundaries
follow time, not an arbitrary key), because the workload is append-heavy and timestamp-keyed. The
dominant read is a range scan over a time window ("give me every point between these two timestamps"),
which is exactly the shape the engine's own time-partitioned chunking is built to serve efficiently.

</details>

**Q30 (co-30 -- retention and downsampling).** What two mechanisms bound a time-series store's storage
growth, and how do they differ?

<details>
<summary>Answer</summary>

A retention policy DROPS raw data entirely once it passes a stated age window. Downsampling instead
ROLLS high-resolution raw points into coarser, pre-aggregated buckets (e.g., per-minute readings into
hourly averages) -- retention discards data outright, while downsampling keeps a lossy, cheaper-to-scan
summary of it instead of the raw points.

</details>

**Q31 (co-31 -- continuous aggregates).** What problem do continuous aggregates solve that a plain
downsampling query does not?

<details>
<summary>Answer</summary>

A plain downsampling query (a `GROUP BY time_bucket(...)`) recomputes its rollup from raw points EVERY
time it runs. A continuous aggregate instead maintains that rollup INCREMENTALLY and PRE-COMPUTED, as
new raw data lands -- so a range query against it reads already-summarized buckets directly, never
re-scanning the underlying raw points at query time.

</details>

**Q32 (co-32 -- OLAP vs. OLTP).** What are the defining latency and access-shape differences between
OLTP and OLAP workloads?

<details>
<summary>Answer</summary>

OLTP is write-heavy, point-transaction-shaped, and expects millisecond latency per operation (a single
row read or write). OLAP is read-heavy, analytical-scan-shaped -- it touches many rows but typically
few columns per query -- and tolerates second-to-minute latency, because the workload is aggregation
over a large dataset, not a single-row transaction.

</details>

**Q33 (co-33 -- columnar storage and compression).** Why does a column-oriented on-disk layout help
both analytical query speed and compression ratio?

<details>
<summary>Answer</summary>

Storing each column's values contiguously on disk lets a query that references only a few columns
read ONLY those columns' own bytes, skipping every other column entirely -- a row-oriented layout
forces reading whole rows regardless of how few columns a query names. The same columnar layout also
compresses better, because values within one column tend to be far more similar to each other
(repeated categories, sorted timestamps) than values across a whole heterogeneous row.

</details>

**Q34 (co-34 -- vectorized execution).** What does "vectorized execution" mean, and what hardware
benefit does it unlock?

<details>
<summary>Answer</summary>

Instead of processing one row at a time through each operator, a vectorized engine processes a whole
BATCH (a "vector") of column values at once per operator call. This improves CPU cache locality (a
contiguous batch of same-typed values fits cache lines efficiently) and enables SIMD instructions
(single-instruction-multiple-data) to apply the same operation to many values in one CPU cycle, both
unavailable to a naive row-at-a-time execution loop.

</details>

**Q35 (co-35 -- Parquet and Arrow).** How do Parquet and Arrow differ, and how do they work together?

<details>
<summary>Answer</summary>

Parquet is an open, columnar, ON-DISK file format -- data at rest. Arrow is a columnar, IN-MEMORY
format -- data while being processed. They work together because Parquet's own on-disk column-chunk
layout maps directly onto Arrow's in-memory columnar layout, letting a reader load a Parquet file
straight into Arrow buffers with minimal transformation, and letting Arrow-aware engines (like DuckDB)
query an in-memory Arrow table with zero-copy interchange -- no serialize-then-copy round trip.

</details>

**Q36 (co-36 -- wide-column vs. columnar OLAP).** The word "column" appears in both "wide-column store"
and "columnar OLAP store" -- what layout does each one actually mean, and why does conflating them
cause real modeling mistakes?

<details>
<summary>Answer</summary>

A wide-column store (Cassandra, DynamoDB) is row/PARTITION-oriented on disk -- an entire row lives
together, tuned for fast, partition-scoped operational reads and writes. A columnar OLAP store (DuckDB,
ClickHouse) is genuinely COLUMN-oriented on disk -- each column's values live together, tuned for
analytical scans over many rows and few columns. Conflating them leads to real mistakes: expecting a
wide-column store to efficiently answer a cross-partition analytical aggregate (it cannot, without an
explicit escape hatch like `ALLOW FILTERING`), or expecting a columnar OLAP store to efficiently answer
a single-partition point lookup the way a wide-column store's partition routing does.

</details>

## Applied problems

Eight scenarios spanning the whole topic. Each describes a realistic situation without naming the
specific concept -- decide what applies and why, then check your reasoning against the worked
solution. Every scenario below is invented for this drill and does not reuse any function, fixture, or
domain from the 91 worked examples or the capstone.

**AP1.** A team builds a global "total signups today" counter as a single key in their key-value
store, incremented by every signup request across the whole fleet. Under heavy signup traffic, that
one node becomes the throughput bottleneck for the entire cluster, even though every other node sits
mostly idle. What's the modeling mistake?

<details>
<summary>Worked solution</summary>

The counter key is a hot partition (co-10) -- every write in the whole system routes to the SAME
partition key, so no amount of horizontal scaling helps, because the bottleneck is one node's own
write capacity, not the cluster's aggregate capacity. The fix is to shard the counter itself (e.g., N
sub-counters incremented round-robin, summed on read) or use a CRDT counter (co-16) designed for
exactly this high-concurrency-increment shape.

</details>

**AP2.** A shopping cart is replicated leaderlessly across three nodes. Two devices belonging to the
same user add different items to the cart nearly simultaneously, on two different replicas. The store
resolves the conflict by keeping only the write with the later server timestamp, silently dropping the
other device's added item. The user is confused when an item they added disappears. What went wrong,
and what would have prevented it?

<details>
<summary>Worked solution</summary>

Last-write-wins (co-14) was the wrong conflict-resolution strategy for a cart, because the two writes
were CONCURRENT (co-15) -- neither happened causally after the other -- and both carried real,
non-conflicting information (two different items added) that LWW's "keep one, discard the other"
behavior cannot merge. A vector clock would have DETECTED the concurrency and let the application merge
both additions, or a CRDT (a set-union-based cart, co-16) would have merged them automatically with no
application-level conflict code at all.

</details>

**AP3.** A team adds a secondary index on a `status` column in their Cassandra cluster, expecting reads
filtered by `status` to become fast. Write latency across the whole table degrades noticeably after
the index is added, and the team is confused because `status` is rarely even queried. What's the
missing piece?

<details>
<summary>Worked solution</summary>

A secondary index in a distributed, partitioned store (co-17) is not "free" the way a single-node
relational index is -- maintaining it costs real, ongoing write-side coordination across partitions on
EVERY write to the indexed column, whether or not that index is ever actually queried. If `status` is
rarely queried, the index's ongoing write cost likely outweighs its rare read benefit -- the team
should reconsider whether denormalizing `status` into a purpose-built lookup table (co-08, co-09) for
the few reads that need it would cost less overall.

</details>

**AP4.** A team deploys MongoDB behind a managed "database-as-a-service" offering they plan to sell to
other companies, having assumed "open source" meant no licensing obligations. Six months in, legal
flags that their offering may trigger SSPLv1's own service-copyleft clause. What should have happened
before deployment?

<details>
<summary>Worked solution</summary>

The team should have checked and recorded MongoDB's ACTUAL license (co-28, DD-15) before building a
managed-service offering on top of it -- SSPLv1 is source-available but explicitly NOT OSI-approved,
and its terms extend copyleft-like obligations specifically to services offered "as a service" around
the software, a materially different commitment from Apache-2.0 or BSD-3-Clause. "Open source" is not
one uniform legal category; the exact license text is what actually governs what you may do.

</details>

**AP5.** A product analytics team runs their daily revenue-by-category report as a `GROUP BY` query
directly against their live, OLTP-serving Cassandra cluster. The report takes minutes to run and
degrades checkout latency for real customers while it executes. What's the architectural mismatch?

<details>
<summary>Worked solution</summary>

This is an OLAP workload (a read-heavy, many-row, analytical aggregate) running against a store tuned
for OLTP (co-32) -- Cassandra's wide-column, partition-oriented layout is not built for a
cross-partition analytical scan, which is exactly why such a query either requires `ALLOW FILTERING`
(a full-cluster scan) or performs poorly. The fix is to ETL the relevant data into a purpose-built
columnar OLAP store (DuckDB, ClickHouse; co-33, co-36) and run the analytical report there, leaving the
OLTP cluster free to serve checkout traffic.

</details>

**AP6.** A team ingests high-frequency sensor readings into a general-purpose document store instead of
a time-series-specific one, planning to "add cleanup later." Eighteen months later, the collection has
grown to billions of documents with no retention policy, no downsampling, and every range query scans
a steadily growing haystack of raw points. What two built-in mechanisms would a purpose-built
time-series store have given them for free?

<details>
<summary>Worked solution</summary>

Retention (dropping raw data past a stated age window) and downsampling (rolling high-resolution
points into coarser, pre-aggregated buckets), both first-class, built-in features of a purpose-built
time-series store like TimescaleDB (co-30) -- rather than something the application must hand-roll
after the fact. A continuous aggregate (co-31) would additionally have kept range queries fast by
reading pre-computed rollups instead of re-scanning an ever-growing set of raw points.

</details>

**AP7.** A team designs a DynamoDB single-table schema by directly mirroring their existing relational
schema's tables as separate DynamoDB tables with generic partition keys like `id`, then bolts on three
Global Secondary Indexes over the following months as new query needs surface, each one adding cost
and write-side complexity. What step did they skip?

<details>
<summary>Worked solution</summary>

They skipped access-pattern-first modeling (co-08) -- single-table design (co-23) is meant to be
DERIVED from the application's own named, dominant access patterns up front (overloading partition-key
and sort-key prefixes specifically to serve those patterns in one query), not retrofitted onto a
relational-shaped schema after the fact. Naming the actual queries first, then designing keys and
indexes to serve them, avoids the escalating GSI-bolt-on pattern this team fell into.

</details>

**AP8.** A team benchmarks the "same" analytical aggregate query on both their Cassandra cluster and a
DuckDB instance loaded with the identical data, and is surprised that Cassandra requires an explicit
`ALLOW FILTERING` flag (with a performance warning) while DuckDB runs the query with no special
handling at all, even though both stores physically hold the same rows. Why does this difference exist,
and is it a bug in Cassandra?

<details>
<summary>Worked solution</summary>

It is not a bug -- it is co-36's own distinction made concrete. Cassandra's wide-column layout and
query planner are BUILT for partition-scoped operational reads; a cross-partition aggregate is
structurally outside that design, so the planner requires an explicit `ALLOW FILTERING` opt-in as an
honest admission that the query will scan every partition. DuckDB's columnar layout is BUILT for
exactly this shape (a `GROUP BY` over a subset of columns across many rows), so it needs no such
guardrail -- the "requires a flag" versus "just works" difference IS the architectural difference
between the two layouts, not an inconsistency between them.

</details>

## Code katas

Five self-contained exercises. Every kata runs on hand-constructed, in-memory data using only the
Python 3.13 standard library -- no live database connection, no Docker container, and no dependency on
this topic's own worked-example or capstone files, so every kata is runnable anywhere Python 3.13 with
`pytest` is installed.

### Kata 1 -- A consistent-hashing ring, from scratch

Write `class HashRing` with `add_node(node: str) -> None`, `remove_node(node: str) -> None`, and
`get_node(key: str) -> str`, placing nodes and keys on a ring via `hashlib.md5` (or any deterministic
hash) reduced modulo a large ring size, and routing each key to the next node clockwise. Construct a
ring of 4 nodes and 1,000 hand-generated keys (`f"key-{i}"` for `i in range(1000)`), record which node
each key maps to, then add a 5th node and re-map every key. Confirm that FEWER than 40% of the 1,000
keys changed their assigned node -- demonstrating co-11's own minimal-movement property (plain modulo
hashing would remap close to 100%).

### Kata 2 -- Quorum math, from R/W/N

Write `has_strong_consistency(r: int, w: int, n: int) -> bool` returning `r + w > n`. Construct at
least 5 `(r, w, n)` combinations of your own, covering: a quorum read/write at `N=3` (e.g., `r=2, w=2,
n=3`), a read-at-ONE configuration (`r=1, w=3, n=3`), a write-at-ONE configuration (`r=3, w=1, n=3`),
and a genuinely under-quorate configuration (`r=1, w=1, n=3`). Confirm your function correctly
classifies each one, and write one sentence explaining WHY `r + w > n` guarantees at least one replica
overlaps between any read set and any write set (co-07).

### Kata 3 -- LWW vs. vector-clock conflict detection

Write two functions: `lww_merge(a: tuple[str, int], b: tuple[str, int]) -> str` (each tuple is
`(value, timestamp)`, returns the value with the later timestamp) and `vector_clocks_concurrent(a:
dict[str, int], b: dict[str, int]) -> bool` (returns `True` if neither clock dominates the other in
every position -- i.e., genuinely concurrent). Construct one fixture where `lww_merge` silently drops a
write that `vector_clocks_concurrent` correctly flags as concurrent (both writes carry real, distinct
information), and one fixture where one vector clock genuinely dominates the other (a real
happens-before relationship) and `vector_clocks_concurrent` correctly returns `False`. Confirm both
results match your hand-reasoning (co-14, co-15).

### Kata 4 -- A G-counter CRDT, merged deterministically

Write `class GCounter` with `increment(replica_id: str, amount: int = 1) -> None`, `value() -> int`
(sum of all replicas' own counts), and `merge(other: "GCounter") -> "GCounter"` (returns a new
`GCounter` whose per-replica count is the MAX of the two inputs' counts for that replica, never the
sum). Construct three independent `GCounter` instances, increment each a different number of times on
a different replica ID, merge all three pairwise in every possible ORDER (e.g., `(a merge b) merge c`
vs. `a merge (b merge c)`), and confirm every merge order produces the IDENTICAL final `value()` --
demonstrating co-16's own deterministic-merge guarantee.

### Kata 5 -- LSM-tree write amplification, simulated

Write `class SimpleLSM` with `put(key: str, value: str) -> None` (appends to an in-memory memtable
list) and `flush() -> None` (moves the current memtable's entries into a new immutable "SSTable" list,
tracking total bytes written to any SSTable across every flush) and `compact() -> None` (merges all
current SSTables into one, keeping only the LATEST value per key, and adds the merged SSTable's own
size to total bytes written again). Insert 500 keys with 10 overwrites each (5,000 total `put` calls,
50 flushes of 100 entries each), run 2 rounds of compaction, and compute `total_bytes_written /
logical_bytes_of_final_data` as the write amplification factor. Confirm this ratio is greater than 1.0
-- demonstrating co-25's own claim that an LSM-tree's append-only write path rewrites the same logical
bytes more than once.

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can name the four NoSQL families this topic covers and explain why graph is excluded. (co-01)
- [ ] I can state what should drive a NoSQL-vs-relational choice, beyond "NoSQL is newer." (co-02)
- [ ] I can state what CAP forces a distributed system to trade, and under what condition. (co-03)
- [ ] I can explain what PACELC adds that CAP alone does not cover. (co-04)
- [ ] I can spell out BASE and explain why many NoSQL stores default to it. (co-05)
- [ ] I can state what eventual consistency promises and what it does not. (co-06)
- [ ] I can explain what R, W, and N control and how a client tunes consistency per call. (co-07)
- [ ] I can explain what "design the schema from the queries" means and what it replaces. (co-08)
- [ ] I can explain what embedding related data buys and what it costs. (co-09)
- [ ] I can explain what makes a partition key good or bad, and name the failure mode. (co-10)
- [ ] I can explain what problem consistent hashing solves versus plain modulo hashing. (co-11)
- [ ] I can describe how leader-follower replication routes writes/reads and handles failover.
      (co-12)
- [ ] I can describe how leaderless replication differs and how it reconciles results. (co-13)
- [ ] I can explain how LWW picks a winner and name its silent cost. (co-14)
- [ ] I can explain what vector clocks detect and what they explicitly do not do. (co-15)
- [ ] I can explain what CRDTs guarantee that a hand-resolved conflict does not. (co-16)
- [ ] I can explain why a distributed secondary index costs more than a single-node one. (co-17)
- [ ] I can explain schema-on-read and its tradeoff for a BSON document. (co-18)
- [ ] I can explain what the aggregation pipeline does that a plain `find()` cannot. (co-19)
- [ ] I can explain the practical benefit of Redis's typed data structures. (co-20)
- [ ] I can explain what changes between Redis as a cache versus as a durable store. (co-21)
- [ ] I can explain what a partition key and a clustering/sort key each control. (co-22)
- [ ] I can explain single-table design and what should drive overloading key prefixes. (co-23)
- [ ] I can explain what a TTL attribute does and name Cassandra's own reliance on it. (co-24)
- [ ] I can describe an LSM-tree's write path and what it trades for write throughput. (co-25)
- [ ] I can explain polyglot persistence and why it is not "pick a trendy DB per service." (co-26)
- [ ] I can explain what multi-item transactions added to NoSQL stores and what they still cost.
      (co-27)
- [ ] I can explain why checking a product's license is a real engineering step. (co-28)
- [ ] I can explain what makes a time-series data model different and its dominant read shape.
      (co-29)
- [ ] I can explain the difference between retention and downsampling. (co-30)
- [ ] I can explain what problem a continuous aggregate solves versus a plain downsampling query.
      (co-31)
- [ ] I can state the defining latency and access-shape differences between OLTP and OLAP. (co-32)
- [ ] I can explain why columnar storage helps both query speed and compression. (co-33)
- [ ] I can explain what vectorized execution means and what hardware benefit it unlocks. (co-34)
- [ ] I can explain how Parquet and Arrow differ and how they work together. (co-35)
- [ ] I can explain the difference between a wide-column store and a columnar OLAP store, and name
      a real modeling mistake conflating them causes. (co-36)

## Elaborative interrogation & self-explanation

Six prompts that ask you to explain WHY, connecting two or more concepts, rather than recall a single
fact. Write your own answer before checking the discussion.

**E1.** CAP (co-03) and PACELC (co-04) both describe consistency-availability/latency trade-offs, but
PACELC applies even with NO partition at all. Why does this topic teach both, rather than just PACELC
as the strictly more complete model?

<details>
<summary>Discussion</summary>

CAP and PACELC answer different questions that both matter in practice: CAP names the trade-off a
system is FORCED into during a genuine partition (an emergency condition), while PACELC names the
trade-off a system CHOOSES on every single normal operation, partition or not. A team needs CAP's
vocabulary to reason about failure-mode behavior and PACELC's vocabulary to reason about everyday
latency/consistency tuning (co-07's R/W/N) -- collapsing them into "just PACELC" would lose the useful
distinction between an emergency trade-off and a routine one.

</details>

**E2.** LWW (co-14) and vector clocks (co-15) both handle concurrent writes, yet this topic frames LWW
as often the WRONG choice rather than simply "a faster alternative" to vector clocks. Why is "faster"
not the right lens for comparing them?

<details>
<summary>Discussion</summary>

LWW and vector clocks solve genuinely different problems: LWW picks a winner and silently discards
information, while vector clocks detect a conflict and preserve BOTH pieces of information for the
application to merge. "Faster" implies they are interchangeable answers to the same question with
different costs -- they are not. The right lens is whether losing the discarded write's data is
actually acceptable for that specific field (a last-write-should-win status flag) or not (two
independently-added shopping cart items, AP2) -- that decision, not raw speed, should drive the choice.

</details>

**E3.** Access-pattern-first modeling (co-08) and denormalization (co-09) are taught together, yet a
team could denormalize data WITHOUT having done access-pattern-first modeling first. Why does this
topic insist the two happen in that specific order?

<details>
<summary>Discussion</summary>

Denormalizing without first naming the dominant access pattern risks optimizing the wrong read --
duplicating data into an aggregate shape that serves a query the application does not actually run
often, while leaving the ACTUAL dominant query still requiring a join or a second fetch. Naming the
access pattern first turns denormalization from a guess into a targeted decision: embed or duplicate
specifically what the NAMED dominant read needs, not whatever seems convenient to combine.

</details>

**E4.** Both a secondary index in Cassandra (co-17) and `ALLOW FILTERING` (referenced across co-13,
co-22, and co-36) let a query filter on a non-partition-key column, yet this topic treats them as
different tools for different situations. What's the actual difference in what each one costs?

<details>
<summary>Discussion</summary>

A secondary index pays its cost UP FRONT, continuously, on every write to the indexed column,
regardless of how often the index is later queried. `ALLOW FILTERING` pays its cost AT QUERY TIME
instead -- each individual query that uses it triggers a full-cluster scan, with no ongoing write-side
overhead between queries. The right choice depends on frequency: a column filtered often justifies an
index's continuous write cost; a column filtered rarely is often cheaper served by an occasional
`ALLOW FILTERING` scan than by paying an index's cost on every write whether queried or not.

</details>

**E5.** Retention (co-30) and TTL (co-24) both auto-delete old data, yet this topic treats TimescaleDB's
retention policy and Cassandra's per-row TTL as meaningfully different mechanisms rather than the same
idea with different names. Why?

<details>
<summary>Discussion</summary>

TTL is set PER ROW, at write time, and each row expires independently on its own schedule -- it is a
fine-grained, per-item mechanism with no awareness of the table's overall shape. A retention policy
operates at the CHUNK or PARTITION level, dropping an entire time-partitioned chunk once its whole
window ages out, in one operation -- a coarser-grained, engine-native mechanism purpose-built for a
time-series store's own chunk structure. The practical difference shows up at scale: dropping one
chunk is far cheaper than expiring millions of individually-TTL'd rows one at a time.

</details>

**E6.** This topic's own scope boundary excludes `graph-databases` entirely but only PARTIALLY excludes
`database-internals-and-storage-engines` -- LSM-tree-vs-B-tree (co-25) is taught here at a conceptual
level even though the full internals-implementation treatment belongs to that other topic. Why is a
partial, conceptual-only inclusion the right boundary here, rather than excluding LSM-trees entirely
the same way graph databases are excluded?

<details>
<summary>Discussion</summary>

Graph databases are excluded entirely because nothing else in this topic depends on graph-traversal
concepts to be taught honestly. LSM-trees are different: understanding WHY Cassandra and other
wide-column stores accept higher write and read amplification in exchange for write throughput (co-25)
is necessary to explain their real access-pattern tradeoffs (co-08, co-22) -- you cannot honestly teach
"why does Cassandra reject a query that skips the partition key" without first establishing what
compaction and amplification are. The boundary is drawn at "how would I IMPLEMENT an SSTable's
compaction strategy" (that belongs entirely to `database-internals-and-storage-engines`), not at
"why does this trade-off exist" (that belongs here, because it is load-bearing for everything else
this topic teaches about wide-column stores).

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
