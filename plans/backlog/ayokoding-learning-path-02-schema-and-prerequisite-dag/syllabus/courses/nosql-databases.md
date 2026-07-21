# NoSQL Databases (By Example, Python)

**Course ID**: `nosql-databases` · **Format**: By Example · **Language**: Python.

**Short summary**: Document, key-value, column stores

**Scope note**: the non-relational families — key-value, document, wide-column, and time-series — when to
pick each, how to model access-pattern-first, and the CAP/PACELC trade-offs, accessed from Python. Graph databases are their
own topic ([`35-graph-databases`](./graph-databases.md)). License-awareness (DD-15) is treated as a
real engineering step. Relational depth is [`26-advanced-sql-and-query-performance`](./advanced-sql-and-query-performance.md).

## Why this exists · the big idea

- **The problem before the solution**: forcing every workload through one normalized relational store with
  strong consistency costs latency and blocks horizontal scale for access patterns that never needed either.
- **Keep-this-if-you-forget-everything**: choose the store by the access pattern and the consistency you can
  actually tolerate — CAP/PACELC says a distributed system trades consistency for availability and latency,
  so pick the trade deliberately instead of inheriting it.
- **Big ideas touched**: `consistency-latency-throughput` (CAP/PACELC is the whole decision),
  `abstraction-and-its-cost` (denormalization buys read speed and charges duplication + write complexity).

`†`: Python is the primary language here; the dagger flags the fully-typed-Python treatment (DD-39) —
every driver-facing example is type-annotated and `pyright`-clean, not a non-Python subject exception.

## Prerequisites

- **Prior topics**: [topic 10 SQL Essentials](./sql-essentials.md) (the relational model these contrast
  against) and [topic 4 Just Enough Python](./just-enough-python.md);
  [topic 26 Advanced SQL](./advanced-sql-and-query-performance.md) sharpens the modeling contrast.
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with pinned CVE-clean drivers; local
  instances (Docker fine) of **Valkey** (BSD) or Redis, a document store (MongoDB — note SSPL), and a
  wide-column store (Cassandra — Apache-2.0); each product's **license** checked before use.
- **Assumed knowledge**: relational schema + CRUD (topic 10); running a local service; basic Python
  driver use.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (all five license claims confirmed against primary sources): **Redis** — tri-license
  RSALv2/SSPLv1/**AGPLv3** since Redis 8 (2025-05-01, re-adding an OSI-approved option); **Valkey** —
  **BSD-3-Clause** (Linux Foundation fork, March 2024); **MongoDB** — **SSPLv1** (unchanged since Oct 2018,
  not OSI-approved); **Cassandra** — **Apache-2.0** (unchanged); **ScyllaDB** — **source-available**
  (Enterprise 2025.1+; Open Source 6.2.x is the final AGPL release). CAP (Brewer 2000) + PACELC (Abadi 2010)
  framing stable. (redis.io/blog/agplv3 / valkey.io / mongodb.com / cassandra.apache.org / scylladb.com)
- 2026-07-12 — DD-35 primary-source pass (API/behaviour claims traced to the vendor's own docs, actually
  fetched):
  - **MongoDB** (docs.mongodb.com Manual, `[Verified]`) — `$match`/`$group`/`$lookup` are current
    aggregation stages (co-19); `$lookup`'s concise correlated-subquery syntax is **5.0+** (ex-32 must not
    assume it pre-5.0). `createIndex()`/`explain()` + `IXSCAN`/`COLLSCAN`/`totalDocsExamined` terminology is
    current (ex-13/36/37). Multi-document ACID transactions: 4.0 (2018); sharded/distributed: 4.2 (2019);
    docs note real cost, embedding stays the default (co-27/ex-34/35/72). `w:"majority"`/`readConcern`
    semantics current (ex-65/66). Current GA line 8.0.x–8.2.x — re-pin exact patch at authoring time.
  - **Redis / Valkey** (redis.io docs, `[Verified]`) — data types current (co-20); `EXPIRE`/`TTL` in
    seconds, `TTL` returns `-1` for no-expiry, `PERSIST` removes expiry (ex-07/08). **`MULTI`/`EXEC` is NOT
    ACID-isolated**: a runtime error inside the block does not roll back remaining queued commands — ex-28/
    ex-30/ex-72 must not overclaim rollback; `WATCH` gives optimistic CAS aborting `EXEC` with `nil`
    (ex-29). RDB vs AOF both current, hybrid is the recommended default (ex-09/64). `redis-py` (PyPI
    `redis`) is the official client. Current point release ~8.8.0 (via endoflife.date, Tier-4) — treat patch
    as approximate.
  - **Cassandra** (cassandra.apache.org + DataStax, `[Verified]` mechanism) — partition/clustering keys
    (co-22/ex-45/46/47), LSM storage engine (co-25/ex-55/56/57), consistency levels `ONE`/`QUORUM`/`ALL`
    (co-07/ex-38/39/75) all current. LWT `INSERT ... IF NOT EXISTS` is Paxos compare-and-set with an
    `[applied]` boolean (ex-58) — **the commonly quoted "four round trips" figure was NOT confirmed against
    apache.org primary docs; dropped from ex-58, keep only the qualitative "LWTs are expensive" framing.**
    Python driver `cassandra-driver` is now Apache-maintained (3.30+). Current release ~5.0.8 (endoflife,
    Tier-4) — re-pin at authoring time.
  - **DynamoDB** (docs.aws.amazon.com, `[Verified]`) — partition+sort key model (co-22/23), GSI vs LSI
    quotas (ex-52/76), TTL is a Number epoch attr deleted **best-effort (typically within ~2 days), expired
    items still read until purged** (ex-53/77 must state this, not claim instant delete),
    `ConsistentRead` semantics with GSI/Streams always eventually-consistent (ex-54), `ConditionExpression`
    → `ConditionalCheckFailedException` and NOT supported by `BatchWriteItem` (ex-69). DynamoDB Local is an
    official AWS Docker image. **License caveat: DynamoDB is a proprietary AWS managed service, not an OSS
    product — it has no OSI license to record, so its examples (co-22/23/27) carry no co-28 citation;
    state this distinction explicitly rather than forcing it into the OSS license-naming pattern.**
  - **TimescaleDB / time-series (co-29/30/31, ex-81–85)** — added 2026-07-12 and DD-35-verified against
    tigerdata.com the same day. **TimescaleDB 2.28.2 (2026-06-30)**, shipped as a PostgreSQL extension
    (`CREATE EXTENSION timescaledb`). Note the vendor rebrand **Timescale → Tiger Data** (June 2025): docs
    now live at tigerdata.com/docs and the source-available license is the **Tiger Data License (TSL)** (same
    TSL abbreviation). **License split (drives co-28):** `create_hypertable`, `time_bucket`, and basic
    hyperfunctions are **Apache-2.0**; **continuous aggregates** (ex-84), **`add_retention_policy`** (ex-83),
    and columnar compression ("Hypercore") are **TSL / Community** — source-available, **not** OSI-approved —
    so ex-83/ex-84 record the TSL tier under co-28, not Apache-2. (Data-tiering to object storage is a Tiger
    **Cloud** managed-service feature, not part of the self-hosted extension — excluded, not a TSL extension
    feature.) **API note:** the current generalized hypertable API (v2.13+) is
    `create_hypertable('metrics', by_range('ts'))`; the positional `create_hypertable('metrics', 'ts')` still
    works as the backward-compatible old interface. Continuous aggregates use `CREATE MATERIALIZED VIEW ...
WITH (timescaledb.continuous)`; retention uses `add_retention_policy(rel, drop_after => INTERVAL '30 days')`.
  - **OLAP / columnar (co-32–36, ex-86–91)** — added 2026-07-12, DD-35-verified the same day.
    **OLAP-vs-OLTP** workload split verified against aws.amazon.com/compare. **Columnar win** (read only
    projected columns, dictionary/run-length/delta + ZSTD compression, vectorized/SIMD execution) verified
    against clickhouse.com/docs "Why is ClickHouse so fast?". **ClickHouse** = column-oriented OLAP DBMS,
    `MergeTree` engine, **Apache-2.0** (license confirmed via the GitHub repo, not the docs intro page).
    **DuckDB** = in-process columnar-vectorized OLAP DB, **MIT** (duckdb.org/why_duckdb). **Parquet**
    (columnar on-disk, Apache-2.0, parquet.apache.org) + **Arrow** (columnar in-memory, zero-copy;
    Apache-2.0 per the ASF project — `[Needs Verification]`: `arrow.apache.org/overview` did not print the
    literal license string, confirm against `github.com/apache/arrow/LICENSE.txt` at authoring time).
    **co-36 distinction** (wide-column Cassandra = row/partition-oriented SSTables vs columnar OLAP =
    column-on-disk) verified against cassandra.apache.org storage-engine docs — keep the two as separate
    concepts, do not conflate.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · nosql-family-taxonomy** — key-value, document, wide-column, and time-series stores optimize
  different access shapes and trade-offs; graph is covered separately in [topic 35](./graph-databases.md).
- **co-02 · when-nosql-vs-relational** — pick a NoSQL store when the access pattern, horizontal-scale need,
  or tolerable consistency doesn't fit the relational model's joins-plus-ACID default.
- **co-03 · cap-theorem** — a partitioned distributed system must trade consistency for availability
  (Gilbert & Lynch's 2002 formal proof of Brewer's conjecture).
- **co-04 · pacelc-extension** — even absent a partition, a distributed system trades latency for
  consistency (Abadi, 2010).
- **co-05 · base-vs-acid** — Basically Available / Soft state / Eventually consistent as the looser
  alternative many NoSQL stores default to instead of ACID.
- **co-06 · eventual-consistency** — replicas converge to the same value over time without synchronous
  coordination on every write.
- **co-07 · tunable-consistency-quorum** — per-operation R/W/N (or write-concern/read-concern) settings let a
  client dial consistency versus latency for that one call.
- **co-08 · access-pattern-first-modeling** — design the schema from the queries the application will
  actually run, not from a normalized entity diagram.
- **co-09 · denormalization-and-aggregates** — embedding or duplicating related data into one aggregate so
  the common read is a single fetch, at the cost of write-side duplication.
- **co-10 · partition-sharding-keys** — the key chosen to distribute rows/documents/items evenly across
  nodes; a poorly chosen one creates a hot partition.
- **co-11 · consistent-hashing** — a hash ring that minimizes data movement when nodes are added or removed
  (the Dynamo-paper technique).
- **co-12 · replication-leader-follower** — one leader orders writes; followers replicate and can serve
  reads; failover promotes a follower.
- **co-13 · replication-leaderless** — any replica accepts a write; a read/write quorum reconciles the
  result (Dynamo-style).
- **co-14 · conflict-resolution-lww** — last-write-wins picks a winner among concurrent writes by timestamp,
  silently dropping the loser.
- **co-15 · conflict-resolution-vector-clocks** — vector clocks detect (not resolve) concurrent, causally
  unordered updates so the application can merge them.
- **co-16 · crdts** — conflict-free replicated data types merge concurrent updates deterministically without
  app-level conflict code.
- **co-17 · secondary-indexes-in-nosql** — indexing beyond the primary/partition key, and the extra write
  and cross-node coordination cost it adds in a distributed store.
- **co-18 · mongodb-document-model-and-schema-on-read** — BSON documents/collections carry no schema
  enforced at write time by default; the reader interprets the shape it finds.
- **co-19 · mongodb-aggregation-pipeline** — a staged server-side pipeline (`$match`/`$group`/`$lookup`)
  transforms and joins documents without pulling raw data to the client.
- **co-20 · redis-data-structures** — Redis exposes typed structures (strings, lists, hashes, sets, sorted
  sets) as first-class server-side operations, not opaque blobs.
- **co-21 · redis-cache-vs-store** — the same engine used as a disposable cache (TTL eviction, no durability)
  or as a durable primary store (RDB/AOF persistence tuned).
- **co-22 · wide-column-partition-clustering-keys** — Cassandra/DynamoDB rows/items are grouped by a
  partition key and ordered within it by a clustering key (Cassandra) or sort key (DynamoDB).
- **co-23 · dynamodb-single-table-design** — one physical table holding multiple entity types, distinguished
  by overloaded key prefixes, driven by named access patterns.
- **co-24 · time-to-live** — a per-item/per-key expiry attribute the store uses to auto-purge stale data.
- **co-25 · lsm-tree-vs-btree-and-amplification** — an append-only write path (memtable → SSTable →
  compaction) buys write throughput at the cost of write and read amplification, versus a B-tree's in-place
  updates.
- **co-26 · polyglot-persistence** — deliberately using different stores for different services or access
  patterns within one system instead of forcing everything into one engine.
- **co-27 · multi-item-transactions** — NoSQL stores adding ACID-style transactions across multiple
  keys/documents/rows (Redis `MULTI`/`EXEC`, MongoDB multi-document transactions, Cassandra lightweight
  transactions), and the latency cost versus a single-item write.
- **co-28 · license-awareness-nosql** — checking and recording a NoSQL product's actual license (SSPL,
  AGPLv3, BSD-3-Clause, Apache-2.0, source-available, or proprietary-managed-service) before adopting it, as
  a real engineering step (DD-15).
- **co-29 · time-series-data-model** — a store optimized for append-heavy, timestamp-keyed measurements
  (metrics, events, IoT/telemetry): time is the primary axis, writes arrive roughly in time order, and reads
  are almost always range-scans over a window. The family includes TimescaleDB (a PostgreSQL extension that
  auto-partitions a table into time-chunked "hypertables"), InfluxDB, and the Prometheus TSDB. Contrast with
  a general wide-column store (co-22): a TSDB bakes the time axis, retention, and rollups into the engine
  rather than leaving them to the schema.
- **co-30 · retention-and-downsampling** — bounding storage growth on an ever-growing time series by (a) a
  **retention policy** that automatically drops raw data older than a window, and (b) **downsampling** that
  rolls high-resolution points up into coarser buckets (e.g. per-second → per-hour averages) so long-range
  history stays queryable cheaply after the raw points are gone.
- **co-31 · continuous-aggregates** — incrementally maintained, pre-computed time-bucketed rollups
  (a materialized view auto-refreshed as new data lands) so a range query reads summarized buckets instead of
  re-scanning raw points every time. In TimescaleDB these are continuous aggregates built over `time_bucket()`;
  the same idea appears as InfluxDB tasks / downsampling jobs.
- **co-32 · olap-vs-oltp** — OLTP is write-heavy point transactions on individual records at millisecond latency; OLAP runs read-heavy analytical scans and aggregations over many rows × a few columns at second-to-minute latency, so the two workloads want opposite storage layouts.
- **co-33 · columnar-storage-and-compression** — a column-oriented on-disk layout lets an analytical query read only the columns it touches and compresses far better (dictionary / run-length / delta codecs, then ZSTD) because same-type, same-distribution values sit together.
- **co-34 · vectorized-execution** — analytical engines process data in column _batches_ (vectors) rather than a row at a time, improving CPU-cache locality and enabling SIMD, which is why columnar OLAP engines outrun row-at-a-time execution on wide scans.
- **co-35 · columnar-formats-parquet-arrow** — Apache Parquet is an open columnar _on-disk_ file format for efficient projected reads; Apache Arrow is a language-agnostic columnar _in-memory_ format enabling zero-copy interchange between engines (both Apache-2.0).
- **co-36 · wide-column-vs-columnar-olap** — the word "column" names two different layouts: a **wide-column store** (Cassandra, co-22) is row/partition-oriented on disk and tuned for operational writes + partition reads, whereas a **columnar OLAP store** (ClickHouse, DuckDB) is column-oriented on disk and tuned for analytical scans — do not conflate them.

## Worked examples

Colocated under `nosql-databases/learning/code/`; each runnable from typed Python (`redis-py`, `pymongo`,
`cassandra-driver`, `boto3`, `psycopg` for the TimescaleDB time-series examples, and `duckdb` + `pyarrow` for
the OLAP-columnar examples) or the store's own shell (`redis-cli`/`mongosh`/`cqlsh`/`psql`/`clickhouse-client`)
against a local instance — Valkey/Redis and MongoDB and Cassandra and TimescaleDB and ClickHouse via Docker
(DuckDB runs in-process), DynamoDB via the official `amazon/dynamodb-local` Docker image (DD-20/DD-30/DD-39).
Contiguous `ex-01..ex-91`. Every example cites the `co-NN` it exercises; every concept above is exercised by
≥1 example.

### Beginner

- **ex-01 · key-value-set-get** — `SET`/`GET` a string key via `redis-cli` against Valkey/Redis — verify the value round-trips. (co-20)
- **ex-02 · key-value-crud-python** — a typed `redis-py` wrapper for set/get/delete — verify a full CRUD round trip from Python. (co-20)
- **ex-03 · redis-hash-basics** — `HSET`/`HGETALL` modeling a user record — verify all fields are returned. (co-20)
- **ex-04 · redis-list-basics** — `LPUSH`/`RPUSH`/`LRANGE` as a work queue — verify FIFO order. (co-20)
- **ex-05 · redis-set-basics** — `SADD`/`SMEMBERS` for a tag set — verify uniqueness (duplicate `SADD` is a no-op). (co-20)
- **ex-06 · redis-sorted-set-leaderboard** — `ZADD`/`ZRANGE` building a score leaderboard — verify score-order retrieval. (co-20)
- **ex-07 · redis-expire-ttl** — `EXPIRE` + `TTL` on a session key — verify the countdown and the eventual miss after expiry. (co-24)
- **ex-08 · redis-persist-cancel-ttl** — `PERSIST` removes a key's expiry — verify `TTL` returns `-1` afterward. (co-24)
- **ex-09 · redis-as-cache-vs-store** — the same keys with persistence disabled vs enabled, then a simulated restart — verify the cache-only case loses data and the persisted case does not. (co-21)
- **ex-10 · mongo-insert-one** — `insertOne`/`insert_one` via `pymongo` — verify the document is stored with a generated `_id`. (co-18)
- **ex-11 · mongo-find-query** — `find()` with a filter — verify only matching documents return. (co-18)
- **ex-12 · mongo-embedded-vs-referenced** — the same one-to-many relation modeled embedded vs referenced — verify both are queryable, then contrast document size and read-query count. (co-09, co-18)
- **ex-13 · mongo-create-index** — `createIndex()` on a query field — verify `explain()` shows an index scan (`IXSCAN`), not a collection scan (`COLLSCAN`). (co-17, co-18)
- **ex-14 · mongo-schema-on-read** — insert two documents into one collection with different field shapes — verify both are accepted and the reader must check field presence, not enforce a schema. (co-18)
- **ex-15 · nosql-family-classify** — classify five real products (Redis, MongoDB, Cassandra, DynamoDB, Neo4j) by family — verify against a reference answer key. (co-01)
- **ex-16 · when-to-pick-nosql-checklist** — score two sample workloads against a NoSQL-fit checklist (access pattern, scale, join needs) — verify the checklist recommends relational or NoSQL correctly for each. (co-02)
- **ex-17 · cap-theorem-classify** — classify three configured stores (MongoDB default, Cassandra at `QUORUM`, DynamoDB) as CP- or AP-leaning — verify against the documented guarantee for each configuration. (co-03)
- **ex-18 · pacelc-classify** — extend the CAP classification with the else-latency-vs-consistency axis for the same three stores — verify the PA/EL vs PC/EC labeling. (co-04)
- **ex-19 · base-vs-acid-table** — write a comparison table contrasting BASE and ACID guarantees property-by-property — verify each property is correctly attributed to its model. (co-05)
- **ex-20 · eventual-consistency-simulate** — a toy two-replica simulation where a read right after a write can return stale data — verify the stale read, then convergence after a delay. (co-06)
- **ex-21 · partition-key-hash-distribute** — hash five keys across four buckets with a simple mod-hash — verify roughly even distribution. (co-10)
- **ex-22 · consistent-hashing-ring** — add a node to a hash ring and count keys remapped — verify only about `1/N` keys move, not all of them. (co-11)
- **ex-23 · replication-leader-follower-sim** — a toy leader that orders writes while two followers replicate — verify followers converge to the leader's write order. (co-12)
- **ex-24 · access-pattern-first-sketch** — write the two dominant queries first, then derive the document shape from them — verify the shape answers both with one fetch each. (co-08)
- **ex-25 · license-check-redis-valkey** — read and record the current Redis license (tri-license RSALv2/SSPLv1/AGPLv3) vs Valkey's BSD-3-Clause — verify the citation matches the official page. (co-28)
- **ex-26 · license-check-mongodb** — read and record MongoDB's SSPLv1 license — verify the citation matches the official page. (co-28)
- **ex-27 · license-check-cassandra** — read and record Apache Cassandra's Apache-2.0 license — verify the citation matches the official page. (co-28)

### Intermediate

- **ex-28 · redis-transaction-multi-exec** — `MULTI`/`EXEC` atomically transferring a value between two keys — verify both updates apply together (note: no rollback on a runtime error inside the block). (co-27)
- **ex-29 · redis-watch-optimistic-lock** — `WATCH` + `MULTI`/`EXEC` implementing optimistic concurrency — verify the transaction aborts (`nil` reply) when the watched key changes concurrently. (co-27)
- **ex-30 · redis-pipeline-vs-transaction** — contrast a pipeline (no atomicity guarantee) with `MULTI`/`EXEC` (queued-then-atomic, but not ACID-isolated) — verify only the pipelined case can show a partial-apply race. (co-27)
- **ex-31 · mongo-aggregation-match-group** — `$match` + `$group` computing a per-category total — verify the aggregated counts. (co-19)
- **ex-32 · mongo-aggregation-lookup-join** — `$lookup` joining two collections in one pipeline (5.0+ correlated syntax) — verify the joined array field on each output document. (co-19)
- **ex-33 · mongo-aggregation-pipeline-stages** — chain `$match` → `$group` → `$sort` — verify the intermediate and final stage output. (co-19)
- **ex-34 · mongo-multi-document-transaction** — a session-scoped multi-document transaction moving a value between two documents — verify atomic commit (or full rollback on error). (co-27)
- **ex-35 · mongo-transaction-abort** — force an error mid-transaction — verify no partial write is visible outside the transaction. (co-27)
- **ex-36 · mongo-compound-index** — a compound index over two query fields — verify `explain()` shows the compound index selected by the query planner. (co-17)
- **ex-37 · mongo-covered-query** — a query answered entirely from the index — verify `explain()` shows no document fetch (`totalDocsExamined: 0`). (co-17)
- **ex-38 · quorum-read-write-math** — compute `W + R > N` for three `(N, W, R)` configurations — verify which configurations guarantee a strongly consistent read. (co-07)
- **ex-39 · cassandra-quorum-tuning** — write at `QUORUM`, read at `ONE` vs `QUORUM` on a 3-node local cluster — verify the consistency/latency contrast. (co-07)
- **ex-40 · leaderless-replication-sim** — a toy leaderless store where any of 3 replicas accepts a write, reconciled by a quorum read — verify the client observes the latest write once the read quorum overlaps the write quorum. (co-13)
- **ex-41 · lww-conflict-resolution** — two concurrent writes to the same key resolved by last-write-wins — verify the later timestamp wins and the earlier write is silently dropped. (co-14)
- **ex-42 · vector-clock-detect-conflict** — two replicas with divergent vector clocks on the same key — verify the conflict is flagged as concurrent, not auto-resolved. (co-15)
- **ex-43 · crdt-g-counter** — a grow-only counter CRDT merged from two replicas — verify the merge is commutative and yields the correct total regardless of merge order. (co-16)
- **ex-44 · crdt-lww-register** — a CRDT LWW-register merging two replica states — verify deterministic convergence to the same value on both replicas. (co-16)
- **ex-45 · cassandra-table-partition-clustering** — `CREATE TABLE` with a partition key + clustering column for a time-series feed — verify rows return ordered within a partition. (co-22)
- **ex-46 · cassandra-partition-query** — `SELECT` scoped to one partition key — verify a fast, single-partition read. (co-22)
- **ex-47 · cassandra-query-without-partition-key** — a query missing the partition key — verify Cassandra rejects it unless `ALLOW FILTERING` is explicit, and note why. (co-22)
- **ex-48 · cassandra-ttl-row** — `INSERT ... USING TTL <seconds>` — verify the row expires after the TTL elapses. (co-24)
- **ex-49 · dynamodb-put-get-item** — `put_item`/`get_item` via `boto3` against `amazon/dynamodb-local` — verify a round-trip on partition key. (co-22)
- **ex-50 · dynamodb-composite-key-query** — `Query` with a partition key + a sort-key range condition — verify ordered items returned within the partition. (co-22)
- **ex-51 · dynamodb-single-table-two-entities** — one table storing two entity types via prefixed sort-key values — verify both entity types retrievable under the same partition key. (co-23)
- **ex-52 · dynamodb-gsi-access-pattern** — a Global Secondary Index serving a second access pattern the base table's key can't — verify a query the base table alone couldn't answer. (co-23, co-17)
- **ex-53 · dynamodb-ttl-attribute** — enable TTL on a Number attribute — verify the item is auto-purged after its expiry epoch time passes (note: best-effort, typically within a couple of days; expired items may still read until purged). (co-24)
- **ex-54 · dynamodb-consistent-read-toggle** — `GetItem` with `ConsistentRead=False` vs `True` right after a write — verify the eventually-consistent case can return a stale value while the strongly consistent case cannot. (co-06, co-07)

### Advanced

- **ex-55 · lsm-tree-write-path-sim** — simulate memtable → flush → SSTable → compaction — verify writes land in an immutable SSTable only after a flush. (co-25)
- **ex-56 · btree-vs-lsm-write-amplification** — measure simulated total bytes written for a B-tree-style in-place update vs an LSM append-then-compact path for the same logical writes — verify the LSM path has higher write amplification but higher raw write throughput. (co-25)
- **ex-57 · lsm-read-amplification** — a read that must check the memtable plus N SSTables before compaction — verify read cost (number of files checked) drops once compaction reduces the SSTable count. (co-25)
- **ex-58 · cassandra-lightweight-transaction** — `INSERT ... IF NOT EXISTS` (Paxos-backed compare-and-set) — verify a second insert with the same key is rejected (`[applied] = false`); note only the qualitative "LWTs are expensive, reserve them" cost. (co-27)
- **ex-59 · cassandra-secondary-index-cost** — a secondary index on a non-partition column — verify the query still works, and note the cross-node fan-out it requires versus a partition-scoped query. (co-17, co-22)
- **ex-60 · polyglot-persistence-three-stores** — one small app using Redis for session state, MongoDB for a catalog, and Cassandra for event history — verify each store is exercised for the access pattern it fits. (co-26)
- **ex-61 · denormalize-vs-normalize-tradeoff** — model the same one-to-many relation normalized (referenced) vs denormalized (embedded), and count queries for a common read — verify the denormalized shape needs one query where the referenced shape needs N+1. (co-09)
- **ex-62 · access-pattern-driven-schema-redesign** — given two named access patterns, redesign a naive document schema to serve both with a single query each — verify both patterns are single-query-served after the redesign. (co-08)
- **ex-63 · secondary-index-vs-denormalization** — contrast adding a secondary index vs denormalizing to avoid a query the primary key can't serve — verify both approaches return the identical result with a different cost profile. (co-17, co-09)
- **ex-64 · redis-durability-rdb-aof** — configure RDB snapshotting vs AOF append-only persistence — verify data survives a simulated restart under each, and note the recovery-window difference. (co-21)
- **ex-65 · mongo-write-concern-tuning** — write concern `w: 1` vs `w: "majority"` — verify the difference in when the write is acknowledged. (co-07)
- **ex-66 · mongo-read-concern-tuning** — read concern `"local"` vs `"majority"` — verify a read at `"local"` can observe data a rollback could later discard, while `"majority"` cannot. (co-07)
- **ex-67 · cap-tradeoff-written-rationale** — for each of the three configured stores (from ex-39/ex-58/ex-66), write the CAP/PACELC position and justify it from the actually configured consistency level — verify the rationale matches the observed behavior. (co-03, co-04)
- **ex-68 · schema-on-read-migration** — add a new field to some but not all existing documents, then have the reader default the missing field — verify old and new documents both read correctly with no migration step run. (co-18)
- **ex-69 · dynamodb-conditional-write** — `put_item`/`update_item` with a `ConditionExpression` (e.g. `attribute_not_exists`) — verify a conflicting concurrent write raises `ConditionalCheckFailedException`. (co-27)
- **ex-70 · dynamodb-hot-partition-diagnose** — a skewed partition key that concentrates traffic on one partition — verify a more selective/composite key spreads the load evenly. (co-10)
- **ex-71 · wide-column-vs-document-tradeoff** — model the same unbounded feed as a Cassandra wide-column partition vs a MongoDB embedded array — verify both serve the read, then contrast update cost as the feed grows without bound. (co-22, co-18)
- **ex-72 · nosql-transactions-cost-comparison** — compare the added latency of MongoDB multi-document transactions, Cassandra lightweight transactions, and Redis `MULTI`/`EXEC` on the same toy workload against the non-transactional path — verify each adds measurable overhead. (co-27)
- **ex-73 · crdt-vs-vector-clock-tradeoff** — contrast CRDT auto-merge vs vector-clock-detected app-level merge on the same concurrent-edit scenario — verify the CRDT converges with no app merge code while the vector-clock path requires one. (co-15, co-16)
- **ex-74 · replication-leader-follower-failover** — simulate a leader failure and follower promotion — verify writes resume once a new leader is elected, and note the availability gap during failover. (co-12)
- **ex-75 · tunable-consistency-latency-tradeoff-measured** — measure simulated latency at `W=1` vs `W=QUORUM` vs `W=ALL` for the same write — verify latency increases as `W` increases. (co-07)
- **ex-76 · secondary-indexes-cross-store-contrast** — contrast a MongoDB secondary index, a Cassandra secondary index, and a DynamoDB GSI answering the same shaped query — verify each is index-served but built and maintained differently. (co-17)
- **ex-77 · capstone-preview-kv-session-store** — a Valkey-backed session store with TTL-based expiry wired into a small app — verify sessions round-trip and auto-expire. (co-20, co-24, co-21)
- **ex-78 · capstone-preview-document-access-pattern** — the capstone's two named access patterns modeled as one MongoDB collection with a supporting index — verify each pattern is index-served. (co-08, co-17, co-19)
- **ex-79 · capstone-preview-wide-column-feed** — the capstone's time-series/feed access pattern modeled as a Cassandra partition-plus-clustering table — verify a partition query returns ordered rows. (co-22, co-25)
- **ex-80 · capstone-preview-license-and-cap-rationale** — draft the per-store CAP/PACELC + license rationale document for all three chosen stores — verify every store's choice cites its access pattern and its checked license. (co-03, co-04, co-28)

### Time-series

- **ex-81 · timescale-hypertable-create** — create a TimescaleDB hypertable from a regular table via the current generalized API `create_hypertable('metrics', by_range('ts'))` (the positional `create_hypertable('metrics', 'ts')` still works as the backward-compatible old interface), then insert timestamped readings via `psycopg` — verify a time-range `SELECT` returns points ordered by time and that inserts land across time-partitioned chunks. (co-29)
- **ex-82 · time-bucket-downsample-query** — a `time_bucket('1 hour', ts)` query rolling raw per-second readings into hourly averages — verify the bucketed aggregate matches a hand-computed rollup of the raw points. (co-30)
- **ex-83 · retention-policy-drop-old** — add a retention policy (`add_retention_policy('metrics', INTERVAL '30 days')`) that drops chunks older than the window — verify old-partition data is purged while recent data is retained. (co-30)
- **ex-84 · continuous-aggregate-rollup** — define a continuous aggregate materializing hourly averages over `time_bucket()`, refreshed as new data lands — verify a range query reads the pre-aggregated view (fewer rows scanned) rather than re-scanning the raw hypertable. (co-31)
- **ex-85 · time-series-vs-wide-column-feed** — model the same metrics feed as a TimescaleDB hypertable vs a Cassandra wide-column partition (contrast with ex-71/ex-79) — verify both serve the time-range read, then contrast the built-in retention/downsampling of the TSDB against the hand-rolled TTL + clustering approach of the wide-column store. (co-29, co-22, co-30)

### OLAP & columnar analytics

- **ex-86 · duckdb-columnar-scan** — load a CSV into in-process DuckDB (MIT) and run a `SELECT sum(amount) ... GROUP BY` over one column of many rows from typed Python — verify the aggregate is correct and the query projects only the referenced columns. (co-32, co-33)
- **ex-87 · row-vs-column-scan-contrast** — run the same wide-scan aggregation on a Postgres row-store vs DuckDB columnar — verify both return the identical aggregate, and annotate why the columnar layout reads far less data for the analytical query. (co-33, co-34)
- **ex-88 · parquet-roundtrip-projection** — write a table to Apache Parquet and read back only two columns via `pyarrow` — verify the projected read touches only those column chunks rather than the whole file. (co-35)
- **ex-89 · arrow-zero-copy-interop** — build an Apache Arrow table in memory and hand it to DuckDB (or pandas) without a serialization copy — verify the same buffer backs both (zero-copy interchange). (co-35)
- **ex-90 · clickhouse-mergetree-aggregate** — create a ClickHouse `MergeTree` table (Apache-2.0), insert rows, and run a partitioned `GROUP BY` aggregation via `clickhouse-client` — verify the aggregate is correct and the scan prunes partitions it cannot match. (co-32, co-33)
- **ex-91 · wide-column-vs-columnar-same-query** — model the same event data as a Cassandra wide-column partition vs a DuckDB columnar table and run one analytical aggregate on each (contrast with ex-85) — verify the columnar store scans fewer bytes for the analytical scan while the wide-column store wins the partition point-read, making the co-36 distinction concrete. (co-36, co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: model one domain across the NoSQL families — a key-value cache/session store (Valkey), a
  document model driven by real access patterns (MongoDB), and a wide-column table (Cassandra) — from
  Python, with a written CAP/PACELC + license rationale for each choice.
- **Concepts exercised**: [ ] key-value CRUD (co-20) [ ] access-pattern-first document modeling (co-08,
  co-18) [ ] a wide-column data model (co-22, co-25) [ ] a CAP/PACELC trade-off stated per store (co-03,
  co-04) [ ] a license check recorded per store (co-28).
- **Ordered steps**:
  1. `.../learning/capstone/code/kv.py` — session/cache CRUD against Valkey/Redis. Verify set/get/expire
     round-trips from the CLI.
  2. `doc.py` — a document schema shaped by two named access patterns + an index. Verify each query is
     index-served and returns expected data.
  3. `wide.py` — a wide-column model (partition + clustering keys) for a time-series/feed access pattern.
     Verify a partition query returns ordered rows.
  4. `rationale.md` — per store, state the CAP/PACELC position and the license (with the actual license
     name). Verify each choice is justified by the access pattern.
- **Acceptance criteria**: all three stores are exercised from Python with correct results; each modeling
  choice is justified by an access pattern; the license of each product is named and checked.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Designing Data-Intensive Applications** — Martin Kleppmann (2017). The modern canonical text spanning replication, partitioning, and consistency models across relational and NoSQL systems.
- **NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence** — Pramod J. Sadalage & Martin Fowler (2012). The standard short introduction to document, key-value, column-family, and graph NoSQL data models.
- **Seven Databases in Seven Weeks** — Eric Redmond & Jim R. Wilson (2012; 2nd ed. 2018). Practical tour of relational and NoSQL databases including Redis, MongoDB, Cassandra, and Neo4j.

**Papers & articles**

- **Dynamo: Amazon's Highly Available Key-value Store** — Giuseppe DeCandia et al. (2007). The paper whose design — consistent hashing, vector clocks, quorum reads/writes — inspired Cassandra, Riak, and Voldemort. <https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf>
- **Bigtable: A Distributed Storage System for Structured Data** — Fay Chang et al. (2006). The paper defining the wide-column store model behind Bigtable, HBase, and Cassandra's data model. <https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/>
- **Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services** — Seth Gilbert & Nancy Lynch (2002). The formal proof of the CAP theorem that frames every NoSQL consistency trade-off. <https://dl.acm.org/doi/10.1145/564585.564601>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Data depth — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Data depth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 6 · Databases & data depth.

> _Content originated in the now-closed FS-SE plan (topic 34); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
