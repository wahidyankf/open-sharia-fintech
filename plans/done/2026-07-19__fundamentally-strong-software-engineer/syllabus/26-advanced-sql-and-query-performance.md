# 26 · Advanced SQL & Query Performance (By Example, SQL + Python †)

**prd row**: Pass 2 · Depth, Design & Craft · By Example · SQL + Python † (PostgreSQL) · Learn 126 / Drill 226 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: deep SQL and the performance engineering around it — advanced query features, ACID and
isolation internals, indexing, query planning (`EXPLAIN`), and the N+1/denormalization/partitioning
trade-offs. Basics are the prerequisite [`10-sql-essentials`](./10-sql-essentials.md); PostgreSQL is the
teaching engine (`†` platform-mandated for `EXPLAIN ANALYZE`/MVCC realism).

## Why this exists · the big idea

- **The problem before the solution**: correct SQL can still be catastrophically slow — the query that
  flew on 100 rows melts at 10 million, and you cannot see _why_ without the planner.
- **Keep-this-if-you-forget-everything**: the database does what you ask, well or badly; `EXPLAIN` is how
  you see the _how_, and an index is a space-and-write-cost bargain you make to buy read speed.
- **Big ideas touched**: `consistency-latency-throughput` — isolation levels and locking trade correctness
  guarantees against concurrency and speed; `abstraction-and-its-cost` — indexes and denormalization buy
  reads by charging writes and storage.

## Prerequisites

- **Prior topics**: [topic 10 SQL Essentials](./10-sql-essentials.md) (schema, CRUD, joins, transactions,
  parameterized queries) and [topic 4 Just Enough Python](./04-just-enough-python.md) for the DAL side;
  [topic 11 Backend Essentials](./11-backend-essentials.md) provides the N+1 scenario.
- **Tools & environment**: a macOS/Linux terminal; a local **PostgreSQL** (pinned, CVE-clean); the `psql`
  CLI; **Python 3.x** with a pinned driver for the N+1 example; a seed dataset large enough for `EXPLAIN`
  to matter.
- **Assumed knowledge**: writing `SELECT`/`JOIN`/`INSERT`, transactions, and a parameterized query from
  topic 10; reading a table schema.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). **Re-check the PG major at authoring.**

- 2026-07-12 — verified (CORRECTION, version-sensitive): latest stable is **PostgreSQL 18** (18.4);
  **PG 19 Beta 1** released 2026-06-04, GA targeted Sept 2026 — pin content to PG 18 (or 19 if GA lands
  first). **PG 18 changed `EXPLAIN ANALYZE`**: buffer stats now show **automatically by default** (explicit
  `BUFFERS` no longer required; restore old behavior with `EXPLAIN (ANALYZE, BUFFERS OFF)`). (postgresql.org
  news / neon.com/postgresql/postgresql-18)
- 2026-07-17 — verified (CORRECTION, command misattribution): the syllabus previously claimed
  `EXPLAIN ... VERBOSE` gained WAL/CPU/per-row-average stats in PG 18 — **wrong command**. That addition is
  on `ANALYZE VERBOSE` (the statistics-gathering command, relevant to co-25), not `EXPLAIN`'s own `VERBOSE`
  option (relevant to co-23/co-24, unchanged in PG 18: still output column lists, schema-qualified names,
  range-table aliases, trigger names, query identifier). What `EXPLAIN` itself gained in PG 18: full WAL
  buffer count in `EXPLAIN (..., WAL)` output, index-lookup-per-scan counts, fractional row counts, and
  memory/disk usage on Material/WindowAgg/CTE nodes. Reflect the corrected attribution in the body.
  (postgresql.org/docs/current/release-18.html)
- 2026-07-12 — verified: window functions, recursive CTEs (`WITH RECURSIVE`), set operations, and
  MVCC isolation-level behavior (Read Committed default, Repeatable Read, Serializable via SSI) are stable
  unchanged across recent PostgreSQL releases. (postgresql.org/docs/current)
- 2026-07-17 — verified (content note, not a correction): `pg_stat_statements` (ex-82) is **not enabled by
  default** — requires `shared_preload_libraries = 'pg_stat_statements'` (server restart) plus
  `CREATE EXTENSION pg_stat_statements`. The `total_exec_time` column name is current and correct. Ensure
  ex-82 states the setup prerequisite. `REFRESH MATERIALIZED VIEW CONCURRENTLY` (ex-75) requires at least
  one plain `UNIQUE` index on the view and a prior non-concurrent population — ensure ex-75 states this.
  (postgresql.org/docs/current)
- 2026-07-17 — verified (CORRECTION, version-sensitive landmine for ex-40): PG 18 introduced **B-tree skip
  scan**, letting the planner use a composite index even when the query omits the leading column (via
  per-distinct-leading-value iteration), when the planner judges it cheaper — typically for a
  low-cardinality leading column. This is a new exception to the classic left-most-prefix rule that
  ex-40 ("composite-index-order") is built to demonstrate. **Fix for authoring**: seed ex-40 with a
  high-cardinality leading column so skip scan does not trigger and the classic "used only with the
  leading column" behavior holds cleanly; optionally add a follow-on callout naming skip scan as the
  PG-18-specific exception. (postgresql.org/docs/current/indexes-multicolumn.html;
  neon.com/postgresql/18/skip-scan-btree)

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

This topic **extends** [topic 10 SQL Essentials](./10-sql-essentials.md) — where topic 10 taught `SELECT`/`JOIN`/
`INSERT`, transactions, and parameterized queries, here SQL gains window functions, recursive CTEs, the
planner, indexing strategy, and the concurrency internals underneath `BEGIN`. The concepts do not re-teach
basic CRUD; they deepen it into performance and correctness engineering.

- **co-01 · subqueries-and-derived-tables** — correlated vs uncorrelated subqueries and subqueries used as derived tables in `FROM`.
- **co-02 · common-table-expressions** — `WITH` factoring a query into named, readable steps.
- **co-03 · recursive-ctes** — `WITH RECURSIVE` walking hierarchies and graphs with a termination guard.
- **co-04 · window-functions** — `OVER()` computing across a row set without collapsing rows into groups.
- **co-05 · window-frames-and-partitions** — `PARTITION BY` / `ORDER BY` / the `ROWS` vs `RANGE` frame clause.
- **co-06 · ranking-and-analytic-functions** — `ROW_NUMBER`/`RANK`/`DENSE_RANK`, `LAG`/`LEAD`, `NTILE`, `PERCENT_RANK`.
- **co-07 · set-operations** — `UNION`/`INTERSECT`/`EXCEPT` and their `ALL` variants.
- **co-08 · grouping-sets-rollup-cube** — multi-level aggregation (subtotals, grand totals, crosstabs) in one pass.
- **co-09 · lateral-joins** — `LATERAL` correlating a subquery to each row of the left side.
- **co-10 · conditional-aggregation** — `FILTER (WHERE ...)` and `CASE`-based aggregates for pivots.
- **co-11 · acid-properties** — atomicity, consistency, isolation, and durability defined concretely.
- **co-12 · mvcc** — multi-version concurrency control: readers see a snapshot and don't block writers.
- **co-13 · isolation-levels** — Read Committed, Repeatable Read, and Serializable and the anomalies each forbids.
- **co-14 · read-phenomena** — dirty read, non-repeatable read, phantom, and write skew as named anomalies.
- **co-15 · serializable-snapshot-isolation** — PostgreSQL SSI detecting dangerous dependency structures and aborting.
- **co-16 · explicit-locking** — row locks (`FOR UPDATE`/`FOR SHARE`), advisory locks, and lock modes.
- **co-17 · database-deadlocks** — how the engine detects a lock cycle and how consistent lock ordering avoids it.
- **co-18 · btree-index-mechanics** — the sorted-tree index and why equality, range, and ordering all benefit.
- **co-19 · composite-and-covering-indexes** — column order, index-only scans, and `INCLUDE` columns.
- **co-20 · specialized-indexes** — hash, GIN, GiST, and BRIN indexes and the workload each fits.
- **co-21 · partial-and-expression-indexes** — indexing a predicate subset or a computed expression.
- **co-22 · index-cost-tradeoff** — write amplification, bloat, and when an index hurts more than it helps.
- **co-23 · explain-and-explain-analyze** — estimated vs actual plans; PG 18 shows buffer stats by default.
- **co-24 · reading-a-query-plan** — scan and join node types (nested loop / hash / merge), cost, rows, width.
- **co-25 · table-statistics-and-analyze** — the planner depends on `ANALYZE` stats; stale stats cause bad plans.
- **co-26 · n-plus-1-diagnosis-and-fix** — the app-side query explosion and its join / batch fixes.
- **co-27 · denormalization-and-materialized-views** — trading write cost and storage for read speed.
- **co-28 · partitioning-pooling-and-oltp-vs-olap** — declarative partitioning, connection pooling, and workload-shaped schema.

## Worked examples

Colocated under `advanced-sql-and-query-performance/learning/code/`; each runnable against a seeded
PostgreSQL (DD-20/DD-30). Contiguous `ex-01..ex-85`. Every example cites the `co-NN` it exercises; every
concept above is exercised by ≥1 example.

### Beginner

- **ex-01 · uncorrelated-subquery** — filter with a scalar subquery — verify the result equals the join rewrite. (co-01)
- **ex-02 · correlated-subquery** — per-row `EXISTS` subquery — verify rows are filtered as expected. (co-01)
- **ex-03 · derived-table-in-from** — aggregate over an aliased subquery in `FROM` — verify the summary. (co-01)
- **ex-04 · simple-cte** — factor a filter step into a `WITH` clause — verify it equals the inline query. (co-02)
- **ex-05 · multi-step-cte** — chain three CTEs into a staged transform — verify the final output. (co-02)
- **ex-06 · recursive-cte-counter** — `WITH RECURSIVE` generating `1..N` — verify the series length. (co-03)
- **ex-07 · recursive-cte-tree** — walk an org hierarchy — verify all descendants of a node. (co-03)
- **ex-08 · window-running-total** — `SUM() OVER (ORDER BY)` — verify the cumulative matches hand calc. (co-04)
- **ex-09 · window-partition-avg** — `AVG() OVER (PARTITION BY dept)` — verify the per-group average on every row. (co-05)
- **ex-10 · row-number-rank** — `ROW_NUMBER` vs `RANK` vs `DENSE_RANK` on ties — verify tie handling differs. (co-06)
- **ex-11 · lag-lead-delta** — `LAG` for period-over-period change — verify the delta column. (co-06)
- **ex-12 · ntile-quartiles** — `NTILE(4)` bucketing — verify four balanced buckets. (co-06)
- **ex-13 · union-vs-union-all** — dedup vs keep-dups — verify row counts differ on overlap. (co-07)
- **ex-14 · intersect-except** — set intersection and difference — verify against expected sets. (co-07)
- **ex-15 · group-by-rollup** — `ROLLUP` subtotals + grand total — verify subtotal rows appear. (co-08)
- **ex-16 · grouping-sets** — multiple groupings in one query — verify each grouping is present. (co-08)
- **ex-17 · filter-aggregate** — `COUNT(*) FILTER (WHERE ...)` — verify conditional count vs `CASE`. (co-10)
- **ex-18 · conditional-sum-case** — `SUM(CASE WHEN ...)` pivot — verify the pivoted columns. (co-10)
- **ex-19 · begin-commit-rollback** — a transaction wrapping two writes — verify `ROLLBACK` undoes both. (co-11)
- **ex-20 · atomicity-failure** — force an error mid-transaction — verify no partial write survives. (co-11)
- **ex-21 · create-btree-index** — `CREATE INDEX` on a filter column — verify it exists via `\d`. (co-18)
- **ex-22 · explain-basic** — `EXPLAIN` a simple `SELECT` — verify a plan node prints. (co-23)
- **ex-23 · explain-analyze-basic** — `EXPLAIN ANALYZE` with actual rows/time (PG 18 buffers shown by default) — verify actual vs estimate. (co-23)
- **ex-24 · seq-scan-vs-index-scan** — read the plan before/after adding an index — verify the node becomes Index Scan. (co-24, co-18)
- **ex-25 · analyze-refresh-stats** — run `ANALYZE`, re-`EXPLAIN` — verify row estimates improve. (co-25)
- **ex-26 · for-update-row-lock** — `SELECT ... FOR UPDATE` inside a txn — verify a second session blocks. (co-16)
- **ex-27 · read-committed-default** — observe a non-repeatable read allowed under the default level — verify the reread changes and the snapshot model. (co-13, co-14, co-12)
- **ex-28 · psql-timing** — `\timing` a query — verify a measurable duration prints. (co-23)

### Intermediate

- **ex-29 · correlated-subquery-to-join** — rewrite a correlated subquery as a join — verify same result, better plan. (co-01, co-24)
- **ex-30 · recursive-cte-graph-cycle** — recursive walk with a cycle guard — verify no infinite loop. (co-03)
- **ex-31 · recursive-cte-bom** — a bill-of-materials explosion — verify total component counts. (co-03)
- **ex-32 · window-moving-average** — `ROWS BETWEEN N PRECEDING` frame — verify the sliding window. (co-05)
- **ex-33 · window-range-frame** — `RANGE` vs `ROWS` on duplicate `ORDER BY` keys — verify differing results. (co-05)
- **ex-34 · window-first-last-value** — `FIRST_VALUE`/`LAST_VALUE` with a frame — verify correct edge values. (co-04, co-05)
- **ex-35 · window-percent-rank** — `PERCENT_RANK`/`CUME_DIST` — verify the distribution statistics. (co-06)
- **ex-36 · top-n-per-group** — `ROW_NUMBER` filter for top-3 per partition — verify N rows per group. (co-06)
- **ex-37 · lateral-join-topn** — `LATERAL` fetching top-N related rows per parent — verify the per-parent limit. (co-09)
- **ex-38 · lateral-vs-subquery** — contrast `LATERAL` against a correlated subquery — verify equivalence + plan diff. (co-09, co-01)
- **ex-39 · cube-crosstab** — `CUBE` for a two-dimensional summary — verify all combinations appear. (co-08)
- **ex-40 · composite-index-order** — a two-column index; query uses the prefix — verify used only with the leading column. (co-19)
- **ex-41 · covering-index-only-scan** — `INCLUDE` columns → Index Only Scan — verify the heap is not touched. (co-19, co-24)
- **ex-42 · partial-index** — index `WHERE status='active'` — verify a smaller index used for the matching predicate. (co-21)
- **ex-43 · expression-index** — index on `lower(email)` — verify it serves a case-insensitive lookup. (co-21)
- **ex-44 · hash-index** — `CREATE INDEX USING hash` for equality — verify an equality lookup uses it. (co-20)
- **ex-45 · gin-index-jsonb** — GIN on a `jsonb` column — verify a containment query uses it. (co-20)
- **ex-46 · brin-index-timeseries** — BRIN on an append-only timestamp — verify small size + range scan. (co-20)
- **ex-47 · index-hurts-writes** — measure `INSERT` throughput with N indexes vs none — verify the write slowdown. (co-22)
- **ex-48 · index-bloat-observe** — bloat after many updates, then `REINDEX` — verify the size shrinks. (co-22)
- **ex-49 · explain-nested-loop** — force + read a nested-loop join plan — verify the node and when it's chosen. (co-24)
- **ex-50 · explain-hash-join** — read a hash-join plan on large tables — verify the node's build/probe phases. (co-24)
- **ex-51 · explain-merge-join** — a merge join on sorted inputs — verify the node and its sort children. (co-24)
- **ex-52 · buffers-in-plan** — read shared hit/read buffers (PG 18 default) — verify cache behavior. (co-23)
- **ex-53 · stale-stats-bad-plan** — skew data, skip `ANALYZE`, show a wrong estimate — verify the plan misjudges, then fixes after `ANALYZE`. (co-25)
- **ex-54 · n-plus-1-reproduce** — a Python loop issuing one query per parent — verify the query count is N+1. (co-26)
- **ex-55 · n-plus-1-fix-join** — replace the loop with a single join query — verify one query, same data. (co-26)
- **ex-56 · n-plus-1-fix-in-clause** — batch children with `WHERE ... IN` — verify two queries total. (co-26)
- **ex-57 · repeatable-read-anomaly** — a non-repeatable read under Read Committed, fixed by Repeatable Read — verify the reread becomes stable. (co-13, co-14)
- **ex-58 · phantom-read** — a phantom under RR, prevented by Serializable — verify new rows appear then are blocked. (co-13, co-14)
- **ex-59 · write-skew** — two txns violating an invariant under RR — verify the anomaly, then the SSI abort. (co-14, co-15, co-12)
- **ex-60 · serialization-failure-retry** — catch `40001` and retry — verify the retry succeeds. (co-15)
- **ex-61 · deadlock-reproduce** — two sessions lock in opposite order — verify Postgres kills one with a deadlock error. (co-17)
- **ex-62 · deadlock-avoid-ordering** — consistent lock order — verify no deadlock occurs. (co-17)
- **ex-63 · advisory-lock** — `pg_advisory_lock` as an app-level mutex — verify mutual exclusion. (co-16)
- **ex-64 · materialized-view-refresh** — `CREATE MATERIALIZED VIEW` + `REFRESH` — verify fast reads and staleness. (co-27)

### Advanced

- **ex-65 · recursive-cte-shortest-path** — weighted graph traversal in SQL — verify the shortest cost. (co-03)
- **ex-66 · window-sessionization** — a gaps-and-islands session split with windows — verify session boundaries. (co-04, co-05)
- **ex-67 · window-vs-self-join-perf** — running totals via window vs self-join — verify same result, plan/timing diff. (co-04, co-24)
- **ex-68 · lateral-cross-apply-report** — `LATERAL` powering a dashboard query — verify correctness + plan. (co-09)
- **ex-69 · covering-index-design** — design a covering index for a hot query — verify Index Only Scan + timing drop. (co-19)
- **ex-70 · multicolumn-stats** — `CREATE STATISTICS` for correlated columns — verify the estimate improves. (co-25)
- **ex-71 · partition-by-range** — declarative range partitioning by date — verify partition pruning in the plan. (co-28)
- **ex-72 · partition-pruning-explain** — `EXPLAIN` shows only relevant partitions scanned — verify pruned partitions. (co-28)
- **ex-73 · partition-vs-index-tradeoff** — partition + local index vs one big index — verify the measured difference. (co-28, co-22)
- **ex-74 · denormalization-measured** — denormalize a hot read path, measure read/write delta — verify reads faster, writes costlier. (co-27)
- **ex-75 · materialized-view-concurrent** — `REFRESH ... CONCURRENTLY` strategy — verify reads aren't blocked during refresh. (co-27)
- **ex-76 · connection-pooling-benchmark** — pooled vs per-request connections (Python) — verify the throughput/latency gain. (co-28)
- **ex-77 · isolation-level-matrix** — the same workload at all three levels — verify which anomalies each permits. (co-13, co-14)
- **ex-78 · serializable-throughput-cost** — measure Serializable overhead + retry rate — verify the correctness/throughput trade. (co-15)
- **ex-79 · explain-buffers-io-tuning** — use buffer stats to cut I/O — verify shared reads drop after an index. (co-23, co-18)
- **ex-80 · planner-cost-constants** — tweak `random_page_cost`, observe a plan flip — verify the planner's choice changes. (co-24)
- **ex-81 · slow-query-log-triage** — enable slow-query logging, find the worst query — verify the offender is identified. (co-25, co-26)
- **ex-82 · pg-stat-statements-topn** — rank queries by `total_exec_time` — verify the hottest queries surface. (co-25)
- **ex-83 · olap-vs-oltp-schema** — normalized OLTP vs star-schema OLAP query on the same data — verify each fits its workload. (co-28)
- **ex-84 · bulk-load-copy-vs-insert** — `COPY` vs row `INSERT` throughput — verify `COPY` is far faster. (co-28)
- **ex-85 · capstone-preview-tuning** — thread a window report + index tuning + N+1 fix + anomaly resolution — verify end-to-end on the seed. (co-04, co-23, co-26, co-13)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take a seeded PostgreSQL database + a Python access path and make it fast and correct: write a
  reporting query with window functions/CTEs, diagnose an N+1 and a missing-index slow query with
  `EXPLAIN ANALYZE` and fix both, and reproduce then resolve an isolation-level anomaly — with
  before/after plans and timings.
- **Concepts exercised**: [ ] window functions (co-04) + a recursive CTE (co-03) [ ] reading
  `EXPLAIN ANALYZE` (co-23) [ ] an index that changes the plan (co-18, co-24) [ ] N+1 diagnosis + fix
  (co-26) [ ] an isolation-level anomaly reproduced + resolved (co-13, co-14, co-15) [ ] before/after
  measurements (co-25).
- **Ordered steps**:
  1. `.../learning/capstone/code/seed.sql` — schema + a dataset large enough for plans to differ. Verify
     the seed loads and row counts are as expected.
  2. `report.sql` — a window-function + recursive-CTE report. Verify it returns the correct aggregate on
     the seed.
  3. Capture a slow query's `EXPLAIN ANALYZE`, add the right index, re-capture. Verify the plan changes
     (seq scan → index) and time drops; fix the app-side N+1 and show query-count before/after.
  4. `anomaly.md` + scripts — reproduce a non-repeatable-read/write-skew anomaly, then fix it with the
     correct isolation level/locking. Verify the anomaly occurs before and is gone after.
- **Acceptance criteria**: the report is correct; the index measurably changes the plan and timing; the N+1
  is eliminated (fewer queries); the anomaly is demonstrably reproduced and resolved.
- **Done bar**: runnable end-to-end (against seeded PostgreSQL) + web-verified.

## Read more

**Books**

- **SQL Performance Explained** — Markus Winand (2012). The canonical practitioner's guide to indexing and execution-plan-driven query tuning, vendor-agnostic across major SQL databases.
- **Learning SQL** — Alan Beaulieu (2005; 3rd ed. 2020). Widely used introduction that extends into window functions, CTEs, and query construction.
- **SQL Antipatterns** — Bill Karwin (2010). Standard catalog of common SQL design and query mistakes and their fixes.

**Papers & articles**

- **Use The Index, Luke!** — Markus Winand. Free web edition covering SQL indexing across Oracle, MySQL, PostgreSQL, SQL Server, and Db2. <https://use-the-index-luke.com/>
- **Using EXPLAIN** — The PostgreSQL Global Development Group (official documentation). The canonical reference for reading query plans and diagnosing performance in PostgreSQL. <https://www.postgresql.org/docs/current/using-explain.html>

---

← Previous: [25 · Advanced Algorithms](./25-advanced-algorithms.md) · Next: [27 · Data Access: ORMs & Query Builders](./27-data-access-orms-and-query-builders.md) →
