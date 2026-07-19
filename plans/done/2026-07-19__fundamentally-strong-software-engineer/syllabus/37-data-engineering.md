# 37 · Data Engineering (Annotated-concept, Python)

**prd row**: Pass 3 · Build for the Real World · Annotated-concept · Python · Learn 137 / Drill 237 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: moving and shaping data at rest — batch vs streaming, ETL/ELT pipelines, the medallion
(bronze/silver/gold) layering, dimensional modeling (star schema), data quality, and orchestration — as
runnable Python against local files/DB. Operational SQL depth is
[`26-advanced-sql-and-query-performance`](./26-advanced-sql-and-query-performance.md); the AI/RAG data
path is [`56-creating-ai-powered-apps`](./56-creating-ai-powered-apps.md).

## Why this exists · the big idea

- **The problem before the solution**: data pipelines fail in ways application code doesn't — a re-run
  double-counts, a late-arriving batch corrupts yesterday's totals, and one bad upstream row silently
  poisons every downstream report.
- **Keep-this-if-you-forget-everything**: make every transform idempotent and layered — raw kept immutable
  (bronze), cleaned and conformed (silver), served (gold) — so a re-run is safe and a bad batch is caught at
  a gate before it reaches anyone.
- **Big ideas touched**: `layering-and-leaks` (medallion bronze/silver/gold isolates raw from served),
  `taming-state` (idempotent, backfill-safe transforms control reprocessing state).

## Prerequisites

- **Prior topics**: [topic 10 SQL Essentials](./10-sql-essentials.md) + [topic 26 Advanced SQL](./26-advanced-sql-and-query-performance.md)
  (the warehouse target, star schema, window functions), and [topic 4 Just Enough Python](./04-just-enough-python.md).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with pinned CVE-clean data libs
  (a dataframe lib + a local analytical engine such as DuckDB); a local SQL DB; sample CSV/JSON datasets.
- **Assumed knowledge**: SQL joins + aggregation (topic 10); window functions + EXPLAIN (topic 26); Python
  functions + files (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28) and re-verified under the DD-35
> no-hallucination pass against primary sources (Databricks/dbt/Kafka/Flink/Airflow docs + Kimball Group + a16z + OpenLineage).

- 2026-07-12 — verified: medallion architecture (bronze/silver/gold), ETL vs ELT, Kimball-style
  dimensional modeling (star schema, SCDs), and DAG-based orchestration are evergreen data-engineering
  vocabulary, unchanged in current (2026) usage (Databricks medallion terminology, dbt ELT framing). No
  version/license-sensitive claims to correct.
- 2026-07-12 — DD-35 primary-source pass (author fetched and read each cited page):
  - **Medallion** — Databricks docs (lakehouse/medallion): bronze lands source data "as-is" + load
    metadata; silver is "matched, merged, conformed and cleansed"; gold is consumption-ready, de-normalized,
    read-optimized. `[Needs Verification]` — Databricks' own docs do **not** self-attribute _coining_ the
    term; frame it as "the bronze/silver/gold pattern popularized by Databricks", not "coined in [year]".
  - **ETL vs ELT** (dbt Labs) — the difference is _when_ transform happens (before load = ETL, after load =
    ELT); ELT rose because cloud-warehouse elastic compute makes in-warehouse transform cheap.
  - **Kimball dimensional modeling** (Kimball Group) — facts = numeric measurements with FK context;
    dimensions = descriptive attributes; the grain is "the business definition of the measurement event";
    additive (sum across all dims) / semi-additive (all but time, e.g. balances) / non-additive (ratios —
    store the components, divide at query time).
  - **SCD types** (Kimball Group, numbers formalized in _DW Toolkit_ 3rd ed. 2013) — Type 0 retain-original,
    Type 1 overwrite (no history), **Type 2 = new row + effective-date range + current flag + surrogate key**,
    Type 3 add-a-column (one prior value), Type 4 mini-dimension, **Type 6 = 1+2+3 hybrid** (Type-2 rows plus
    an overwritten Type-1 current column). Do not renumber these.
  - **Kafka** (Apache Kafka / Confluent docs) — topic → partitions → per-partition monotonic offsets; a
    consumer group assigns each partition to exactly one member. **Ordering is guaranteed only within a
    partition, not across partitions.** **At-least-once is the default**; exactly-once (since 0.11) needs the
    idempotent producer (producer-id + sequence dedup) plus transactions.
  - **Stream windows** — naming collision to teach carefully: **Flink** calls time-advancing overlapping
    windows "sliding"; **Kafka Streams** calls the same thing "hopping" and reserves "sliding" for a
    _record-triggered_ join window. This file uses the vendor-neutral trio **tumbling / hopping / session**
    and flags the Kafka-Streams "sliding" meaning. Event-time vs processing-time, watermarks, and
    allowed-lateness / grace-period for late data are per Flink & Kafka Streams docs.
  - **Exactly-once ≠ idempotent sink** (Google Cloud Dataflow docs) — exactly-once _inside_ an engine does
    NOT make an external write exactly-once; the sink write must itself be idempotent (merge on a
    natural/dedup key). Teach "idempotent upsert", not "the engine guarantees it end-to-end".
  - **Data-quality dimensions** — completeness / validity / uniqueness / timeliness / consistency / accuracy
    (Great Expectations taxonomy, corroborated by DAMA-DMBOK). `[Needs Verification]` — any exact "DMBOK
    defines N dimensions" count (book is paywalled); cite the six-dimension core, not a hard count.
  - **Data contracts** — a practitioner-coined pattern (Chad Sanderson / Andrew Jones, ~2022-2024), not a
    formal standard; dbt "model contracts" enforce columns/types/constraints by **failing the build** on
    drift rather than silently drifting.
  - **Orchestration** (Apache Airflow docs) — DAG encapsulates schedule + tasks + deps; tasks run via
    operators; retries set in `default_args`; the scheduler triggers dependency-met tasks; backfill re-runs
    an explicit past date range.
  - **Lineage** (OpenLineage spec, LF AI & Data) — table-level answers "does X feed Y"; column-level answers
    "which input column produced which output column, via what transform" (impact analysis).
  - **CDC** (Debezium) — log-based CDC reads the DB transaction log (MySQL binlog, Postgres logical
    replication) and captures inserts/updates/**deletes**; query-based polling misses deletes and
    between-poll changes. `[Needs Verification]` — `debezium.io` returned HTTP 403 on direct fetch;
    corroborated via Red Hat's mirror + consistent search, re-fetch before content lock.
  - **Modern data stack** (a16z, Bornstein/Li/Casado) — source → ingest (EL, e.g. Fivetran) → transform
    (dbt) → serve (BI); core = replication + cloud warehouse + SQL modeling. `[Needs Verification]` — the
    a16z page is a living document; cite the URL, not a fixed publication year.
  - `[Needs Verification]` — the Jay Kreps "The Log" (2013) URL 404'd on this pass (likely transient; it
    fetched earlier same day); re-confirm the live link before content lock.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept topic). Each example below cites the co-NN it exercises. -->

- **co-01 · batch-vs-streaming** — batch processes a bounded dataset in one pass; streaming processes an unbounded feed record-by-record; the same aggregate can be computed either way.
- **co-02 · etl-vs-elt** — the difference is _when_ transformation happens: ETL transforms before loading, ELT loads raw then transforms in-warehouse (which cloud elastic compute made cheap).
- **co-03 · modern-data-stack-shape** — the canonical pipeline is source → ingest (EL) → transform (T) → serve (BI/ML).
- **co-04 · medallion-bronze-silver-gold** — bronze keeps raw source data as-is + load metadata, silver cleans/conforms, gold serves consumption-ready aggregates; layering isolates raw from served.
- **co-05 · idempotent-transforms** — a transform that produces the same result on re-run (via merge/upsert on a natural key), so re-processing is safe.
- **co-06 · incremental-and-backfill** — process only new rows since a watermark for efficiency, and reprocess an explicit past range (backfill) safely because transforms are idempotent.
- **co-07 · partitioning** — Hive-style partitioning encodes column values in the directory path (`key=value/`) so a query can prune partitions it can't match.
- **co-08 · dimensional-modeling-facts-dims** — facts are numeric measurements with foreign keys to context; dimensions are the descriptive attributes around them.
- **co-09 · star-schema-and-grain** — a star schema links a fact table to dimension tables; the grain is the business definition of one fact row (declare it, keep to it).
- **co-10 · additive-semi-non-additive** — additive facts sum across all dimensions, semi-additive across all but time (e.g. balances), non-additive not at all (ratios — store the components, divide at query time).
- **co-11 · slowly-changing-dimensions** — SCD types manage attribute change: Type 1 overwrite (no history), Type 2 new row + effective dates + current flag, Type 3 add-a-column, Type 6 = 1+2+3 hybrid.
- **co-12 · log-based-streaming** — a broker (Kafka) models a topic as partitions of an append-only log; each record gets a per-partition monotonic offset; a consumer group assigns each partition to exactly one member.
- **co-13 · ordering-and-delivery-semantics** — ordering is guaranteed only within a partition, not across; at-least-once is the default (retries can duplicate); exactly-once needs an idempotent + transactional producer.
- **co-14 · stream-windows** — bounded aggregation over an unbounded stream: tumbling (fixed, non-overlapping), hopping (overlapping, advance < size), session (activity gap).
- **co-15 · event-time-vs-processing-time** — window by when an event occurred (event-time) vs when it arrived (processing-time); a watermark tracks event-time progress and controls how long a window waits for late data.
- **co-16 · data-quality-dimensions** — completeness, validity, uniqueness, timeliness, consistency, accuracy — each a checkable assertion that can fail a batch.
- **co-17 · data-contracts** — a producer-side, enforceable schema guarantee (columns/types/constraints) that fails the build on drift instead of silently corrupting downstream.
- **co-18 · orchestration-dag** — a DAG wires tasks (operators) with dependencies, a schedule, retries, and backfill; the scheduler runs a task once its dependencies are met.
- **co-19 · data-lineage** — table-level lineage records that dataset X feeds Y; column-level records which input column produced which output column, for impact analysis.
- **co-20 · change-data-capture** — CDC surfaces source-database changes: log-based reads the transaction log and captures inserts/updates/deletes; query-based polling misses deletes and between-poll changes.
- **co-21 · exactly-once-sink-idempotent-write** — exactly-once _inside_ an engine does not make an external write exactly-once; the sink write must itself be idempotent (merge on a dedup key).

## Worked examples

Colocated under `data-engineering/learning/code/` as runnable, annotated Python against local files/DB
(DuckDB + a dataframe lib) (DD-20/DD-30). Contiguous `ex-01..ex-52`. Every example cites the `co-NN` it
exercises; every concept above is exercised by ≥ 1 example.

### Beginner

- **ex-01 · batch-vs-streaming-contrast** — compute a running total as one batch pass and as an incremental append — verify both yield the same total. (co-01)
- **ex-02 · etl-order** — transform-then-load: clean/type in Python before writing — verify the loaded table is already typed and deduped. (co-02)
- **ex-03 · elt-order** — load-then-transform: land raw into DuckDB, then transform via SQL — verify the raw landing table is left untouched. (co-02)
- **ex-04 · modern-stack-shape** — wire source → ingest → transform → serve stubs — verify a record flows end to end through all four. (co-03)
- **ex-05 · bronze-land-raw** — land a CSV as-is into bronze with a `load_ts` column — verify row count equals the source and the metadata column is present. (co-04)
- **ex-06 · silver-clean-conform** — transform bronze → silver (typed, deduped, null-dropped) — verify types are cast and duplicate/null rows are gone. (co-04)
- **ex-07 · gold-serve-aggregate** — aggregate silver → gold — verify the served total matches a hand-computed value. (co-04)
- **ex-08 · idempotent-rerun** — run an ETL step twice — verify the second run adds zero duplicate rows. (co-05)
- **ex-09 · upsert-merge-key** — MERGE on a natural key — verify a changed row updates in place rather than duplicating. (co-05)
- **ex-10 · incremental-filter** — process only rows newer than the last watermark — verify only new rows are transformed. (co-06)
- **ex-11 · full-refresh-backfill** — rebuild the whole table ignoring the incremental filter — verify the result equals a from-scratch build. (co-06)
- **ex-12 · hive-style-partition-write** — write Parquet under `key=value/` partition directories — verify the directory layout encodes the partition column. (co-07)
- **ex-13 · partition-pruning-read** — query one partition value — verify only that partition's file is read. (co-07)
- **ex-14 · fact-vs-dimension** — split a flat table into a fact + dimension tables — verify every fact foreign key resolves to a dimension row. (co-08)
- **ex-15 · star-schema-grain** — declare a grain (one row per order line) — verify no row is finer or coarser than the declared grain. (co-09)
- **ex-16 · additive-measure-sum** — sum an additive fact across every dimension — verify the total is consistent regardless of grouping. (co-10)
- **ex-17 · semi-additive-balance** — sum a balance across all dimensions except time — verify a time-sum is flagged as invalid. (co-10)
- **ex-18 · non-additive-ratio** — store numerator + denominator and divide at query time — verify averaging ratios differs from ratio-of-sums. (co-10)

### Intermediate

- **ex-19 · scd-type1-overwrite** — overwrite a changed attribute — verify no prior value is retained. (co-11)
- **ex-20 · scd-type2-new-row** — insert a new row with effective-date range + current flag — verify two versions with disjoint date ranges and one current. (co-11)
- **ex-21 · scd-type3-alt-field** — add a prior-value column — verify both the current and one prior value are readable. (co-11)
- **ex-22 · scd-type6-hybrid** — Type-2 rows plus an overwritten Type-1 current column — verify group-by-current and group-by-value-at-event give different totals. (co-11)
- **ex-23 · kafka-topic-partition-offset** — model a partitioned append-only log — verify each append gets a monotonic offset within its partition. (co-12)
- **ex-24 · consumer-group-assignment** — assign partitions across group members — verify each partition is consumed by exactly one member. (co-12)
- **ex-25 · per-partition-ordering** — interleave two partitions — verify order is preserved within a partition but not across partitions. (co-13)
- **ex-26 · at-least-once-redelivery** — crash a consumer before offset commit — verify the message is redelivered (a duplicate). (co-13)
- **ex-27 · exactly-once-idempotent-producer** — dedup by `(producer_id, seq)` — verify a retried message lands exactly once. (co-13)
- **ex-28 · tumbling-window** — bucket events into fixed non-overlapping windows — verify each event falls in exactly one window. (co-14)
- **ex-29 · hopping-window** — overlapping windows advancing by less than their size — verify one event appears in multiple windows. (co-14)
- **ex-30 · session-window** — group events by an inactivity gap — verify a new session starts after the gap elapses. (co-14)
- **ex-31 · event-time-vs-processing-time** — window by event timestamp vs arrival order — verify a late event lands in its event-time window, not its arrival window. (co-15)
- **ex-32 · watermark-progress** — advance a watermark past a window end — verify the window emits only once the watermark passes. (co-15)
- **ex-33 · late-data-side-output** — route post-watermark events to a side output — verify late events are captured, not silently dropped. (co-15)
- **ex-34 · dq-completeness-null-check** — assert a required column is non-null — verify a null row fails the check. (co-16)
- **ex-35 · dq-uniqueness-dup-check** — assert a key is unique — verify a duplicate key fails the check. (co-16)
- **ex-36 · dq-validity-range-check** — assert a value is within range — verify an out-of-range row fails the check. (co-16)
- **ex-37 · dq-timeliness-freshness** — assert the max timestamp is within N hours — verify a stale batch fails the check. (co-16)
- **ex-38 · dq-consistency-cross-source** — assert a total reconciles across two sources — verify a mismatch fails the check. (co-16)

### Advanced

- **ex-39 · data-contract-schema-enforce** — enforce a producer contract (columns + types + not-null) — verify a schema-drifting build fails instead of silently drifting. (co-17)
- **ex-40 · contract-close-to-producer** — co-locate the contract with the producing model — verify the check runs at produce time, before downstream reads. (co-17)
- **ex-41 · dag-task-dependencies** — define a DAG extract → transform → load with dependencies — verify tasks run in topological order. (co-18)
- **ex-42 · dag-retry-on-failure** — a flaky task with a retry policy — verify it succeeds after N retries. (co-18)
- **ex-43 · dag-schedule-and-catchup** — schedule with catchup over missed intervals — verify one run is created per missed interval. (co-18)
- **ex-44 · dag-quality-gate-blocks** — a data-quality gate task in the DAG — verify a bad batch fails the gate and downstream tasks are skipped. (co-18, co-16)
- **ex-45 · dag-backfill-range** — backfill an explicit past date range — verify only those partitions reprocess. (co-18, co-06)
- **ex-46 · table-level-lineage** — record dataset → dataset edges — verify the downstream of a changed table is discoverable. (co-19)
- **ex-47 · column-level-lineage** — record input-column → output-column edges — verify which input column feeds a given output column. (co-19)
- **ex-48 · cdc-query-based-poll** — poll a table for rows newer than a cursor — verify the poll misses a deleted row. (co-20)
- **ex-49 · cdc-log-based-capture** — read an append-only change log — verify inserts, updates, and deletes are all captured. (co-20)
- **ex-50 · exactly-once-inside-not-sink** — exactly-once inside the pipeline but a non-idempotent sink — verify a retry double-writes at the sink. (co-21)
- **ex-51 · idempotent-sink-merge** — the same retry against a merge-on-key sink — verify exactly one row lands at the sink. (co-21)
- **ex-52 · log-as-source-of-truth** — rebuild table state by replaying the change log — verify the replay reconstructs the current state idempotently. (co-12, co-05)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a complete local data pipeline — ingest raw source files to a bronze layer, clean and
  conform to a silver layer, model a star schema and serve gold aggregates, all wrapped in a small
  orchestrated DAG with retries and a data-quality gate — idempotent and backfill-safe, verified end to
  end in Python.
- **Concepts exercised**: [ ] idempotent + incremental ingest (bronze) (co-04, co-05, co-06) [ ] cleaning/conforming (silver)
  (co-04) [ ] a star schema (facts + dimensions) (co-08, co-09) [ ] gold serving aggregates (co-04, co-10) [ ] data-quality checks that fail a
  bad batch (co-16) [ ] a small orchestrated DAG with retries + gate (co-18).
- **Ordered steps**:
  1. `.../learning/capstone/code/ingest.py` — raw files → bronze, idempotent. Verify a re-run adds no
     duplicate rows.
  2. `transform.py` — bronze → silver (typed, deduped, validated) → a star schema. Verify facts join to
     every dimension and row counts reconcile.
  3. `serve.sql` / `serve.py` — gold aggregates from the star schema. Verify a serving query matches a
     hand-computed expected total.
  4. `pipeline.py` — a DAG wiring the steps with retries + a quality gate. Verify a deliberately bad batch
     fails the quality gate and does not reach gold.
- **Acceptance criteria**: the pipeline is idempotent + backfill-safe; the star schema reconciles; gold
  aggregates are correct; a bad batch is caught by the quality gate before serving.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Designing Data-Intensive Applications** — Martin Kleppmann (2017). Core reference for the batch/stream processing and replication foundations of data pipelines.
- **Fundamentals of Data Engineering** — Joe Reis & Matt Housley (2022). The modern standard introductory text organizing the data engineering lifecycle end to end.
- **The Data Warehouse Toolkit** — Ralph Kimball & Margy Ross (1996; 3rd ed. 2013). The classic reference for dimensional modeling and warehouse design.

**Papers & articles**

- **The Log: What Every Software Engineer Should Know About Real-Time Data's Unifying Abstraction** — Jay Kreps (2013). Canonical article framing the append-only log as the unifying abstraction behind Kafka, replication, and stream processing pipelines. <https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying>

---

← Previous: [36 · Database Internals & Storage Engines](./36-database-internals-and-storage-engines.md) · Next: [38 · Search & Information Retrieval](./38-search-and-information-retrieval.md) →
