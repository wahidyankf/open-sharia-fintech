---
title: "Overview"
date: 2026-07-27T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Data Engineering topic: recall first, then
applied judgment, then hands-on katas, then a self-check checklist, then elaborative-interrogation
prompts that ask _why_, not just _what_. Every answer is hidden in a `<details>` block; try each
item yourself before opening it.

Every kata below is self-contained and deterministic -- pure Python 3.13 standard library only, no
`duckdb`, no `pandas`, no network, and no dependency on this topic's own worked-example or capstone
code.

## Recall Q&A

Twenty-one short-answer questions, one per concept (`co-01` through `co-21`). Answer from memory,
then check.

**Q1 (co-01 -- batch vs. streaming).** Batch and streaming can compute the identical aggregate.
What actually distinguishes the two approaches?

<details>
<summary>Answer</summary>

Not the result, but the shape of the input and when the result becomes available: batch processes a
bounded dataset in one pass and produces a result once that pass finishes; streaming processes an
unbounded, ongoing feed record by record, updating the aggregate continuously as each new record
arrives.

</details>

**Q2 (co-02 -- ETL vs. ELT).** What is the actual difference between ETL and ELT, and what made ELT
practical at scale?

<details>
<summary>Answer</summary>

The difference is purely _when_ transformation happens: ETL transforms the data before loading it
into the warehouse; ELT loads the raw data first and transforms it afterward, in-warehouse, using
SQL. ELT became practical once cloud warehouses made elastic in-warehouse compute cheap enough that
paying for transformation inside the warehouse stopped being a bottleneck.

</details>

**Q3 (co-03 -- modern data stack shape).** Name the four stages of the canonical modern-data-stack
pipeline, in order.

<details>
<summary>Answer</summary>

Source &rarr; ingest (EL, extract and load) &rarr; transform (T, in-warehouse) &rarr; serve
(BI/ML). Ingest and transform are split into two distinct stages because ELT loads raw data first
and only transforms it afterward.

</details>

**Q4 (co-04 -- medallion bronze/silver/gold).** What does each medallion layer hold, and why does
layering matter?

<details>
<summary>Answer</summary>

Bronze keeps source data exactly as it arrived, plus load metadata (e.g. a `load_ts` column);
silver cleans, types, dedupes, and conforms it; gold serves consumption-ready, often aggregated
data. Layering matters because it isolates raw data from what gets served -- a mistake made while
cleaning silver never has to be reconciled against a raw bronze row that has already been
overwritten, since bronze is never mutated.

</details>

**Q5 (co-05 -- idempotent transforms).** What makes a transform idempotent, and what mechanism
usually achieves it?

<details>
<summary>Answer</summary>

A transform is idempotent when re-running it against the same input produces the same result as
running it once -- no duplicated rows, no double-counted totals. It is usually achieved by merging
or upserting on a natural key (an anti-join before insert, or a `MERGE ... WHEN MATCHED /
WHEN NOT MATCHED` statement) rather than blindly appending every row on every run.

</details>

**Q6 (co-06 -- incremental and backfill).** How do incremental processing and backfill relate to
each other, and why does backfill depend on idempotency?

<details>
<summary>Answer</summary>

Incremental processing handles only the rows newer than a watermark, for efficiency on the common
case. Backfill is the deliberate exception: reprocessing an explicit past date range, often the
whole range again. Backfill is only safe because the transform is idempotent -- reprocessing rows
that were already processed once must not duplicate or corrupt what is already there.

</details>

**Q7 (co-07 -- partitioning).** What does Hive-style partitioning actually do, and what query
benefit does it enable?

<details>
<summary>Answer</summary>

It encodes a column's value directly in the storage directory path, as `key=value/` segments (e.g.
`region=east/`). This lets a query engine prune -- skip reading -- every partition directory whose
encoded value cannot match the query's filter, without opening or scanning those files at all.

</details>

**Q8 (co-08 -- facts vs. dimensions).** What is the structural difference between a fact and a
dimension in dimensional modeling?

<details>
<summary>Answer</summary>

A fact table holds numeric measurements (quantities, amounts) plus foreign keys pointing to the
dimensions that give those numbers context. A dimension table holds the descriptive, mostly
non-numeric attributes -- names, categories, dates -- that a fact's foreign keys reference.

</details>

**Q9 (co-09 -- star schema and grain).** What is "the grain" of a fact table, and why must it be
declared before building anything else?

<details>
<summary>Answer</summary>

The grain is the business definition of exactly what one fact row represents -- e.g. "one row per
order line," not "one row per order." It must be declared first because every later modeling
decision (which columns are facts vs. dimensions, whether a measure is additive) depends on knowing
precisely what one row means; mixing rows at two different grains in the same fact table silently
corrupts any aggregate computed over it.

</details>

**Q10 (co-10 -- additive, semi-additive, non-additive).** Give one example measure for each of the
three additivity categories, and state the rule for handling the non-additive case.

<details>
<summary>Answer</summary>

Additive: revenue -- sums correctly across every dimension. Semi-additive: an account balance --
sums correctly across every dimension except time (summing balances across days produces nonsense).
Non-additive: a ratio, like a conversion rate -- never sum a ratio directly; store its numerator and
denominator as separate additive facts and divide them at query time, after aggregating each
component.

</details>

**Q11 (co-11 -- Slowly Changing Dimensions).** Name the four SCD types this topic teaches and, for
each, the one-line mechanism it uses to handle a changed attribute.

<details>
<summary>Answer</summary>

Type 1: overwrite the value in place, no history retained. Type 2: insert a new row with an
effective-date range and a current-flag, keeping every prior version. Type 3: add a dedicated
column holding the one immediately-prior value alongside the current one. Type 6: a hybrid --
Type-2 historical rows, plus one column on each row that is kept overwritten Type-1-style to always
reflect the current value.

</details>

**Q12 (co-12 -- log-based streaming).** How does a Kafka-style broker model a topic internally, and
what does a consumer group guarantee about partition assignment?

<details>
<summary>Answer</summary>

A topic is modeled as one or more partitions, each an append-only log; every record appended to a
partition gets a monotonically increasing offset unique within that partition. A consumer group
assigns each partition to exactly one member of the group at a time, so within a group no two
consumers ever process the same partition concurrently.

</details>

**Q13 (co-13 -- ordering and delivery semantics).** Where is ordering actually guaranteed in a
Kafka-style system, and what is the default delivery semantic?

<details>
<summary>Answer</summary>

Ordering is guaranteed only within a single partition -- records appended to the same partition are
read back in the same order. There is no ordering guarantee across different partitions of the same
topic. The default delivery semantic is at-least-once: a retry after a failure can redeliver a
message, producing a duplicate; exactly-once requires an idempotent, transactional producer on top
of that default.

</details>

**Q14 (co-14 -- stream windows).** Name the three window shapes this topic teaches and the one
structural property that distinguishes each from the other two.

<details>
<summary>Answer</summary>

Tumbling: fixed-size, non-overlapping -- every event falls in exactly one window. Hopping:
fixed-size but overlapping, because the window advances by less than its own size -- one event can
land in more than one window. Session: variable-size, defined by an inactivity gap rather than a
fixed duration -- a new session starts only after the gap has elapsed since the last event.

</details>

**Q15 (co-15 -- event-time vs. processing-time).** What is the difference between windowing by
event-time and windowing by processing-time, and what does a watermark do?

<details>
<summary>Answer</summary>

Event-time windowing buckets a record by when the event actually happened (a timestamp carried in
the record itself); processing-time windowing buckets it by when the system happened to receive it,
which can differ from event-time due to network delay or replay. A watermark tracks how far
event-time processing has progressed and controls how long a window stays open waiting for
late-arriving events before it is considered complete and emits its result.

</details>

**Q16 (co-16 -- data-quality dimensions).** Name the data-quality dimensions this topic teaches and
give one example checkable assertion for any two of them.

<details>
<summary>Answer</summary>

Completeness, validity, uniqueness, timeliness, consistency, and accuracy. Example assertions: a
completeness check that a required column is never null; a uniqueness check that a declared key
never repeats within a batch. Each dimension names a specific, checkable class of assertion that can
fail a batch before it reaches downstream consumers.

</details>

**Q17 (co-17 -- data contracts).** What does a data contract enforce, and how does it differ in
effect from an ordinary data-quality check?

<details>
<summary>Answer</summary>

A data contract is a producer-side, enforceable guarantee about a dataset's shape -- its columns,
their types, and constraints like not-null -- that lives close to the model or system producing the
data. Rather than merely flagging a violation downstream after the fact (as a data-quality check
does), a contract violation **fails the build** at the point of production, stopping schema drift
from ever reaching a consumer in the first place.

</details>

**Q18 (co-18 -- orchestration DAG).** What four things does a DAG-based orchestrator wire together,
and what triggers a given task to run?

<details>
<summary>Answer</summary>

Tasks (run by operators), their dependencies on one another, a schedule, and a retry policy. A given
task runs once the scheduler determines every one of its declared dependencies has already completed
successfully -- dependency-met, not simply "next in a list," is what triggers execution.

</details>

**Q19 (co-19 -- data lineage).** What is the difference between table-level and column-level
lineage, and what question does each answer?

<details>
<summary>Answer</summary>

Table-level lineage records that dataset X feeds into dataset Y -- it answers "does this table feed
that one," a coarse dependency question. Column-level lineage records, more precisely, which
specific input column produced which specific output column via which transform -- it answers the
finer "if I change this one column, exactly what downstream columns does that affect," which is what
real impact analysis needs.

</details>

**Q20 (co-20 -- Change Data Capture).** What is the structural difference between query-based and
log-based CDC, and what does query-based CDC systematically miss?

<details>
<summary>Answer</summary>

Query-based CDC polls a source table for rows that look newer than a cursor value it tracked last
time. Log-based CDC instead reads the database's own transaction log directly. Query-based polling
systematically misses deletes (a deleted row simply vanishes from the poll, leaving no trace of the
delete event) and any change that happened and was then overwritten again between two poll
intervals; log-based CDC captures inserts, updates, and deletes because every one of them is a
distinct entry in the log it reads.

</details>

**Q21 (co-21 -- exactly-once inside vs. an idempotent sink).** Why doesn't an engine's internal
exactly-once guarantee automatically make an external write exactly-once?

<details>
<summary>Answer</summary>

Exactly-once processing guarantees are scoped to what happens _inside_ the engine -- how it tracks
offsets and state during computation. The moment the engine writes to something external (a
database, a file, another system), that external system has no idea what "exactly-once inside the
engine" even means; a retried write after a crash can still land twice at the sink unless the sink
write is itself made idempotent, typically via a merge-on-a-dedup-key operation rather than a plain
append or insert.

</details>

## Applied problems

Seven scenarios spanning the whole topic. Each describes a realistic situation without naming the
specific concept -- decide what applies and why, then check your reasoning against the worked
solution. Every scenario below is invented for this drill and does not reuse any function, fixture,
or domain from the 52 worked examples or the capstone.

**AP1.** A finance team's hourly batch job computes yesterday's total revenue for a dashboard.
After a stakeholder complains the number is "a whole hour stale sometimes," an engineer proposes
rebuilding the entire pipeline on a streaming platform so the dashboard updates continuously. Is the
rewrite justified?

<details>
<summary>Worked solution</summary>

Not necessarily. Batch and streaming can compute the identical aggregate (co-01); the only real
difference is latency and input shape, not correctness or capability. An hourly batch job already
meets "yesterday's total," and the actual complaint ("a whole hour stale sometimes") is a scheduling
frequency problem -- running the batch every 15 minutes instead of hourly may fully resolve the
complaint at a fraction of the cost and risk of a full streaming rewrite. This maps directly to this
topic's
[Tensions & trade-offs -- when NOT to reach for this](../overview.md#tensions--trade-offs----when-not-to-reach-for-this)
section: reach for streaming machinery once genuinely continuous, sub-minute freshness is a real
requirement, not by default whenever "more real-time" sounds appealing.

</details>

**AP2.** A new pipeline lands raw customer records -- including unmasked email addresses -- straight
into the warehouse's bronze layer before any transformation runs, following this topic's own
"transform-after-load" pattern. A reviewer flags this as risky for a dataset containing sensitive
fields, and proposes masking should happen during load instead. Which loading order does the
reviewer actually want, and is medallion layering itself the problem?

<details>
<summary>Worked solution</summary>

The reviewer wants ETL's ordering (co-02) for this specific sensitive-field case: transform (mask)
BEFORE loading, rather than ELT's load-then-transform default. This is not a medallion problem
(co-04) -- bronze can still exist as the landing layer, but the masking transform needs to run
before that landing step for genuinely sensitive fields, rather than after it as ELT's usual
in-warehouse-transform pattern would have it. The two ideas are independent: ETL vs. ELT is about
WHEN transformation happens relative to loading; medallion layering is about HOW the warehouse
organizes what it already holds.

</details>

**AP3.** A silver-layer transform is written as a plain `INSERT INTO silver_orders SELECT * FROM
bronze_orders WHERE load_date = :target_date`. During a backfill for a date range covering the past
two weeks, an operator accidentally reruns the same three-day sub-range twice. The silver table now
shows roughly 1.5x the expected row count for those three days. What's the root cause, and what's
the fix?

<details>
<summary>Worked solution</summary>

The transform is not idempotent (co-05) -- a plain `INSERT` has no mechanism to recognize "this row
already landed" and blindly appends every matching bronze row again on a rerun. Backfill safety
depends entirely on idempotency (co-06): reprocessing an already-processed range is supposed to be
safe precisely because the transform is idempotent, and here it wasn't. The fix is to replace the
plain `INSERT` with a `MERGE`/upsert keyed on the order's natural key (or a `DELETE` for the target
date range immediately before the `INSERT`, if a full overwrite is acceptable), so a rerun of the
identical range produces the identical row count either way.

</details>

**AP4.** A fact table is declared at "one row per order" grain, but an analyst notices the loading
query actually joins in a line-items table without any aggregation step, producing one row per
order LINE instead. Every revenue total computed from this fact table is now higher than the true
order-level total whenever an order has more than one line. What went wrong, and what's the fix?

<details>
<summary>Worked solution</summary>

The fact table's declared grain (co-09) and its actual, physically-loaded grain disagree -- the
loading query silently produced a finer grain (one row per line) than what was declared (one row
per order), and every downstream sum inherits that mismatch as double-counting wherever an order has
multiple lines. The fix is not a query patch; it's a modeling decision: either declare the grain as
"one row per order line" (matching what the load actually produces, an equally valid choice) and
have every consuming query aggregate up to order level explicitly, or fix the load to genuinely
aggregate down to one row per order before it lands. The grain must be declared correctly and then
matched by the actual load, in either direction, not left to silently drift.

</details>

**AP5.** A team partitions a Kafka-style topic by a random UUID key -- expecting, since messages are
appended and read from "the log," that global ordering across the whole topic is automatically
preserved. In production, they observe messages processed noticeably out of the order they were
produced. Is this a bug in the broker?

<details>
<summary>Worked solution</summary>

Not a bug -- exactly the documented ordering guarantee working as designed (co-12, co-13). Ordering
is guaranteed only WITHIN a single partition, never across partitions of the same topic. Partitioning
by a random UUID key spreads messages essentially uniformly across every partition, which is exactly
the right choice for maximizing consumer parallelism, but it also means messages produced
sequentially are very likely to land on different partitions and can legitimately be consumed in a
different relative order. If global ordering across the whole topic is a genuine requirement, the fix
is a single-partition topic (giving up parallelism) or partitioning by a key that groups
must-stay-ordered messages together (e.g. an order ID, so all of one order's events share a
partition and stay ordered relative to each other, even though ordering across DIFFERENT orders is
still not guaranteed).

</details>

**AP6.** An upstream team silently renames a column from `customer_id` to `cust_id` in their source
system. The downstream pipeline's existing data-quality check -- "the `customer_id` column must
never be null" -- does not fire, because the column it's checking for no longer exists at all; the
whole downstream job simply fails with a generic "column not found" error a full week after the
rename shipped, during which several reports quietly ran on stale data. Would a stronger
null-check have caught this sooner, and what's the actual fix?

<details>
<summary>Worked solution</summary>

No stronger null-check would have caught this -- a null-check (co-16) can only validate a column's
VALUES once that column is known to exist; it has no way to notice the column's very presence or
name changed, especially not before the consuming job even runs. The actual fix is a data contract
(co-17) on the producer's side: an enforceable schema guarantee (columns, types, constraints) that
FAILS THE BUILD on the producing side the moment `customer_id` is renamed or removed, rather than
letting the drift ship silently and only surfacing as a downstream crash a week later. Data quality
checks and data contracts are complementary, not interchangeable: a contract prevents a producer
from shipping the wrong shape at all; a data-quality check validates the values within a shape that
is already known to be correct.

</details>

**AP7.** A CDC-based sync keeps a downstream replica table in sync with a source database by
replaying an append-only change log. After an unrelated network blip causes the CDC connector to
restart, the team notices several rows in the replica now have subtly wrong totals -- specifically,
some source-side updates appear to have been applied TWICE. The change log itself is confirmed
correct and complete. What's the likely cause, and what's the general fix?

<details>
<summary>Worked solution</summary>

Log-based CDC (co-20) reading an append-only log is not itself the problem -- the log is confirmed
correct. The likely cause is that the connector's restart re-read and replayed some log entries it
had already applied once before the blip (a common at-least-once-delivery pattern for a restarting
consumer), and the downstream WRITE to the replica table was not idempotent (co-21): a plain
apply-the-update-again on an already-applied change re-applies its delta a second time rather than
converging to the same end state. The general fix is making the sink write idempotent -- a
merge/upsert keyed on the source row's primary key plus its change-log offset or version, so
replaying the identical log entry twice converges to the identical end state rather than compounding.
This is the same principle co-05's idempotent-transform mechanism uses, applied specifically to a
log-replay sink.

</details>

## Code katas

Five self-contained exercises. Every kata runs on hand-constructed, in-memory data using only the
Python 3.13 standard library -- no `duckdb`, no `pandas`, no network, and no dependency on this
topic's own worked-example or capstone files, so every kata is runnable anywhere Python 3.13 is
installed.

### Kata 1 -- An idempotent upsert, hand-built from scratch

Write `upsert(table: list[dict], record: dict, key_field: str) -> list[dict]` that returns a NEW
list: if a record in `table` already has `record[key_field]` matching the incoming record's key, its
entry is replaced in place (same position); otherwise the new record is appended. Build a table of
three records, call `upsert` twice with the SAME record (an update to an existing key) and confirm
the table's length does not grow on the second call. Then call it once more with a genuinely new key
and confirm the length grows by exactly one (co-05).

### Kata 2 -- Grain-violation detector

Write `find_grain_violations(rows: list[dict], grain_keys: list[str]) -> list[tuple]` that returns
every combination of `grain_keys` values appearing MORE THAN ONCE in `rows` (a violation of a
one-row-per-combination grain declaration). Construct a list of dict rows where `["order_id",
"line_number"]` is the declared grain, deliberately include one duplicate `(order_id, line_number)`
pair, and confirm your function returns exactly that one pair (co-09).

### Kata 3 -- Tumbling and hopping windows, from raw timestamps

Write `tumbling_windows(timestamp: int, window_size: int) -> int` returning the window's start
timestamp (`timestamp - (timestamp % window_size)`), and `hopping_windows(timestamp: int,
window_size: int, hop: int) -> list[int]` returning EVERY hopping window's start timestamp that
contains `timestamp` (there can be more than one, since hop < window_size). Using `window_size=60,
hop=20`, confirm a timestamp lands in exactly `window_size // hop` hopping windows, and confirm
`tumbling_windows` never returns more than one window for the same input (co-14).

### Kata 4 -- Round-robin consumer-group assignment

Write `assign_partitions(partition_count: int, consumer_ids: list[str]) -> dict[int, str]` that
assigns each partition index `0..partition_count-1` to exactly one consumer via round-robin
(`consumer_ids[partition_index % len(consumer_ids)]`). Confirm, for `partition_count=6` and 3
consumers, that every consumer gets exactly 2 partitions, and that every partition index appears as
a key exactly once (co-12).

### Kata 5 -- A column-level lineage graph, queried both directions

Represent a pipeline's column lineage as `edges: list[tuple[str, str]]` of `(input_column,
output_column)` pairs across several chained transform steps of your own choosing (at least 6
edges, spanning at least 3 hops from an original source column to a final output column). Write
`downstream_of(edges, column: str) -> set[str]` (every column transitively produced FROM `column`,
via a breadth-first traversal) and `upstream_of(edges, column: str) -> set[str]` (every column that
transitively FEEDS `column`). Confirm that renaming or changing your originally-chosen source column
correctly reports every final output column it affects via `downstream_of` (co-19).

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can explain what actually distinguishes batch from streaming, given they can compute the
      identical aggregate. (co-01)
- [ ] I can state the difference between ETL and ELT and what made ELT practical at scale. (co-02)
- [ ] I can name the four stages of the modern-data-stack pipeline in order. (co-03)
- [ ] I can explain what each medallion layer holds and why the layering matters. (co-04)
- [ ] I can explain what makes a transform idempotent and the mechanism that usually achieves it.
      (co-05)
- [ ] I can explain why backfill safety depends on idempotency. (co-06)
- [ ] I can explain what Hive-style partitioning does and the query benefit it enables. (co-07)
- [ ] I can state the structural difference between a fact and a dimension. (co-08)
- [ ] I can define "grain" and explain why it must be declared before anything else. (co-09)
- [ ] I can give one example each of an additive, semi-additive, and non-additive measure, and the
      rule for handling the non-additive case. (co-10)
- [ ] I can name all four SCD types and the one-line mechanism each uses. (co-11)
- [ ] I can explain how a Kafka-style broker models a topic and what a consumer group guarantees
      about partition assignment. (co-12)
- [ ] I can state where ordering is actually guaranteed and the default delivery semantic. (co-13)
- [ ] I can name the three stream-window shapes and the property that distinguishes each. (co-14)
- [ ] I can explain the difference between event-time and processing-time windowing and what a
      watermark does. (co-15)
- [ ] I can name the six data-quality dimensions and give a checkable assertion for at least two.
      (co-16)
- [ ] I can explain what a data contract enforces and how it differs in effect from a data-quality
      check. (co-17)
- [ ] I can name the four things a DAG-based orchestrator wires together and what triggers a task
      to run. (co-18)
- [ ] I can explain the difference between table-level and column-level lineage and the question
      each answers. (co-19)
- [ ] I can state the structural difference between query-based and log-based CDC and what
      query-based CDC systematically misses. (co-20)
- [ ] I can explain why an engine's internal exactly-once guarantee does not automatically make an
      external write exactly-once. (co-21)

## Elaborative interrogation & self-explanation

Six prompts that ask you to explain WHY, connecting two or more concepts, rather than recall a
single fact. Write your own answer before checking the discussion.

**E1.** Why does backfill (co-06) genuinely depend on idempotency (co-05), rather than the two being
independent features you could ship separately?

<details>
<summary>Discussion</summary>

Backfill's entire value proposition is "you can safely reprocess a past range, even one you already
processed once, without worrying about the consequences." If the underlying transform is NOT
idempotent, reprocessing an already-processed range would duplicate or corrupt exactly the data
backfill is supposed to be able to safely touch -- making "just backfill it" a destructive
instruction instead of a safe one. Idempotency is not a nice-to-have alongside backfill; it is the
precondition that makes backfill a safe operation to offer at all.

</details>

**E2.** Why must a fact table's grain (co-09) be declared and settled BEFORE deciding whether a
given measure is additive, semi-additive, or non-additive (co-10)?

<details>
<summary>Discussion</summary>

Additivity is a claim about how a measure behaves when summed ACROSS ROWS at a given grain --
"revenue sums correctly across every dimension" only makes sense once you know what one row
represents. A measure that is additive at "one row per order line" grain could become subtly wrong
if the grain silently shifted to "one row per order" without re-deriving the measure (e.g. summing
an already-summed order-level total again would double-count). Declaring the grain first is what
makes any later additivity classification a meaningful, stable claim rather than one that silently
breaks the moment the grain changes underneath it.

</details>

**E3.** Kafka-style partition count (co-12) trades off against ordering (co-13) in a specific way.
What exactly is that trade-off, and why can't a system simply have both maximal parallelism AND
global ordering?

<details>
<summary>Discussion</summary>

More partitions means more consumers can process a topic in parallel (co-12's consumer-group
assignment spreads partitions across group members), but ordering is only ever guaranteed WITHIN a
single partition (co-13) -- there is no cross-partition ordering guarantee at all. Global ordering
across an entire topic can only be guaranteed by forcing every record through a single, serial
partition, which caps parallelism at exactly one consumer. The two properties are structurally in
tension: partitioning is what buys parallelism, and it is the SAME mechanism that gives up
cross-partition ordering as its cost.

</details>

**E4.** Event-time windowing with a watermark (co-15) and the timeliness data-quality dimension
(co-16) both deal with "how late is too late." What's the concrete difference between what each one
is actually protecting?

<details>
<summary>Discussion</summary>

A watermark protects the correctness of a SPECIFIC WINDOW's aggregate -- it decides how long to wait
for late-arriving events before emitting a window's final result, trading completeness against
latency for that one window. A timeliness data-quality check instead protects trust in a WHOLE
BATCH or dataset -- it asserts something like "the freshest timestamp in this batch is within N
hours of now," failing the batch outright if the data is too stale to be trustworthy at all. One is
a per-window wait-and-emit policy inside a streaming engine; the other is a pass/fail gate on an
entire batch's overall freshness.

</details>

**E5.** Why does this topic insist a data contract (co-17) lives close to the PRODUCER, while a
data-quality check (co-16) typically lives close to the CONSUMER? What failure does each position
actually prevent?

<details>
<summary>Discussion</summary>

A contract living at the producer catches a schema-shape problem at the earliest possible moment --
before a single row of drifted data ever leaves the system that created it, by failing that
system's own build. A data-quality check living downstream, at or near the consumer, catches
VALUE-level problems (a null where one shouldn't be, an out-of-range number) that can only be
detected by actually looking at the data as it arrives, regardless of how carefully-shaped its
schema is. Placing the contract upstream prevents shape drift from ever shipping; placing quality
checks downstream catches the value-level problems a correctly-shaped schema can still carry.

</details>

**E6.** Log-based CDC (co-20) and an idempotent sink write (co-21) are two entirely separate
concepts, taught in different worked examples. Why does a real CDC-based sync pipeline need BOTH,
rather than either one alone being sufficient?

<details>
<summary>Discussion</summary>

Log-based CDC alone guarantees the SOURCE side is captured completely and correctly -- every insert,
update, and delete is a real entry in the log, nothing is missed. But CDC's own delivery to a
downstream consumer is typically at-least-once (the same default co-13 names for Kafka-style
streaming), meaning a connector restart or retry can replay an already-applied log entry. Without an
idempotent sink write, that replay lands as a duplicate application of an already-applied change. A
complete, correctly-captured log (CDC's job) plus a write that converges to the same state no matter
how many times it's replayed (idempotent sink's job) are two independent halves of the same
end-to-end correctness guarantee -- neither one substitutes for the other.

</details>

---

&larr; Previous: [Capstone](../learning/capstone/overview.md)
