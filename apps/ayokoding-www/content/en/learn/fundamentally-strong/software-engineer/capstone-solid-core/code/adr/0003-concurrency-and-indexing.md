# ADR-0003: Concurrent digest, an O(n) algorithm, and an EXPLAIN-guided index

**Status**: Accepted
**Date**: 2026-07-19

## Context

Step 3 needed a genuine hot path to parallelize (topic 24), a genuine algorithmic improvement
(topic 25), and a genuine index tuned by reading a real query plan (topic 26). All three
numbers on this page are MEASURED, not assumed -- two of the three measurements below
contradicted the naive expectation on the first attempt, which is exactly why they were
measured instead of asserted.

## Decision 1: `longest_streak_ever` -- O(n) over integer ordinals, not `date`/`timedelta`

A first O(n) implementation, written directly against `date`/`timedelta` objects, was
benchmarked (`bench/benchmark_algorithm.py`) against the O(n log n) `sorted()`-based baseline
and was SLOWER at every size up to n=500,000 -- Python's built-in `sorted()` runs in optimized C
with low per-comparison overhead, while constructing a fresh `timedelta` object on every loop
iteration in pure Python is comparatively expensive. Converting each `date` to its integer
`toordinal()` once, then running the identical algorithm over `set[int]` with plain `+1`/`-1`
arithmetic, measured 2.59x-2.86x FASTER than the baseline across the same range. **Decision**:
ship the ordinal-based version. Big-O describes asymptotic growth; it does not by itself
guarantee a win at any one concrete n in a language with non-trivial per-object overhead --
that has to be measured, and here it changed which implementation actually shipped.

## Decision 2: digest concurrency -- `ProcessPoolExecutor`, sized for real, not toy, workloads

`app/digest.py` computes each habit's streak data independently -- CPU-bound Python work
(rebuilding a hash-set from every stored check-in row, then the O(n) scan), which a THREAD pool
would not meaningfully parallelize (GIL-bound), so a `ProcessPoolExecutor` was chosen. It is
called directly as a batch job (not behind a synchronous HTTP route -- see digest.py's own
docstring for why). First benchmarked at a modest scale (16 habits x 8,000 check-ins --
reproducible via `python3 -m bench.benchmark_concurrency --num-habits 16
--checkins-per-habit 8000`), `concurrent_digest` was measurably SLOWER than
`sequential_digest` on every repeated run -- spawning worker processes and importing
`pydantic` fresh in each one costs tens of milliseconds per process, which dominated a
workload whose real per-habit work was only a few milliseconds. The exact ratio is itself
noisy at this small a scale (eight repeated runs on the machine that authored this ADR
measured between 0.13x and 0.69x -- roughly 1.4x to 8x slower than sequential, never
faster) because a fixed, OS-scheduled process-spawn cost competes with whatever else the
machine is doing at that instant; the DIRECTION (slower) reproduces every run, so no single
precise ratio is quoted here. At a larger, still realistic scale (40 habits x 25,000
check-ins = 1,000,000 rows), `concurrent_digest` measured 1.7x-2.3x FASTER across repeated
runs -- the fixed process-pool startup cost is paid ONCE per `with
ProcessPoolExecutor(...)` block, and is only worth paying
when the total real work clears that fixed cost by a wide margin. **Decision**: ship
`concurrent_digest`, and document the small-workload finding here rather than hide it -- it is
the actual engineering lesson topic 24 teaches: concurrency has overhead, and the right call
depends on the workload's real size, not on "concurrent is always faster."

## Decision 3: denormalize `checkins.user_id`, guided by real `EXPLAIN QUERY PLAN` output

This app's database is SQLite, not PostgreSQL -- topic 26's own teaching engine is PostgreSQL
specifically for `EXPLAIN ANALYZE`'s execution-time statistics (confirmed by reading
sqlite.org/lang_explain.html directly: SQLite's grammar has `EXPLAIN` and
`EXPLAIN QUERY PLAN`, no `ANALYZE` keyword). Reading this app's OWN engine's real
`EXPLAIN QUERY PLAN` output for a "recent activity across all my habits" query showed TWO
indexed searches -- `SEARCH h USING COVERING INDEX idx_habits_user_id (user_id=?)` then
`SEARCH c USING COVERING INDEX sqlite_autoindex_checkins_1 (habit_id=?)` -- plus
`USE TEMP B-TREE FOR ORDER BY` (NOT a full table scan; see `bench/explain_query_plan.sh`):
the normalized schema still forces a join from `checkins` to `habits` just to filter by
`user_id`, then a sort, even with both sides of the join reached through an index.
**Decision**: denormalize `user_id` onto `checkins` (it never changes after a habit is
created, so this specific denormalization introduces no update-anomaly risk) and add a
composite index `(user_id, checkin_date DESC)` (`migration_v3.sql`). The SAME query re-read via
`EXPLAIN QUERY PLAN` afterward shows a single `SEARCH checkins USING INDEX
idx_checkins_user_id_date (user_id=?)` -- no join, no sort.

## Consequences

- **Positive**: all three changes are measured, not assumed, and two of the three measurements
  overturned the naive first guess -- documented here rather than silently discarded.
- **Trade-off**: `checkins.user_id` duplicates data already reachable via `habit_id ->
habits.user_id` -- an accepted, documented redundancy (topic 26 denormalization trade-off),
  not an oversight; `repository_sqlite.SqliteHabitRepository.record_checkin` is the ONE place
  this app ever writes a `checkins` row, so the copy cannot drift.

## Verification

`tests/test_domain.py::TestLongestStreakEver` cross-checks the O(n) and O(n log n)
implementations agree on 20 randomized histories before either is trusted. `tests/test_app.py`'s
`TestDigestSequentialAndConcurrentAgree` asserts `sequential_digest` and `concurrent_digest`
return identical results. `bench/explain_query_plan.sh` + `bench/benchmark_sql_tuning.py`
confirm the before/after rows are identical (`diff` + an `assert`) -- the index changed the
PLAN, never the RESULT.
