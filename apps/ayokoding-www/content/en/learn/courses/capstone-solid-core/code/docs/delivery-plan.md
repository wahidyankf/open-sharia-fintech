# Delivery plan: re-engineer the Habit Tracker into a professional core

**Author**: capstone-solid-core (Pass-2 boundary)
**Date**: 2026-07-19

## Staging (topic 09/33 delivery discipline: small, independently verifiable steps)

| Step | Change                                                              | Verify before proceeding                                           |
| ---- | ------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 1    | Import the Pass-1 baseline; write ADR-0001                          | Suite green against the UNCHANGED baseline                         |
| 2    | SOLID + functional-core/imperative-shell refactor; ADR-0002         | Suite still green; OCP demonstrated (new repo, zero edits)         |
| 3    | Concurrent digest + O(n) algorithm + EXPLAIN-guided index; ADR-0003 | Suite green; three benchmarks show a real, measured improvement    |
| 4    | CI gate + clean commit history + docs; ADR-0004                     | Local CI gate green; the SAME gate genuinely fails on a bad commit |

Each step is a checkpoint a reader can stop at and have a working, tested app -- no step leaves
the suite red for another step to fix later (topic 15/30: never commit on top of a known-red
suite).

## Risk register

- **Risk**: the O(n) algorithm could be slower than the O(n log n) baseline at real-world sizes
  (constant-factor overhead). **Mitigation**: measured before shipping (`bench/benchmark_algorithm.py`)
  -- it initially WAS slower with the first `date`/`timedelta`-based implementation; the ordinal-based
  rewrite that actually ships was chosen because it measured faster, not assumed to be faster (see
  ADR-0003).
- **Risk**: `ProcessPoolExecutor` could add overhead that outweighs its benefit at small scale.
  **Mitigation**: measured at two scales; documented BOTH the small-scale loss and the
  larger-scale win (ADR-0003) rather than only reporting the flattering number.
- **Risk**: denormalizing `checkins.user_id` could drift from `habits.user_id` over time.
  **Mitigation**: `SqliteHabitRepository.record_checkin` is the ONE place a `checkins` row is
  ever created; no other code path writes to this table.

## Rollback

Every step's change is additive at the schema level (`migration_v3.sql` only adds a column and
an index) and behavior-preserving at the API level (no endpoint signature changed; one new
endpoint was added). Rolling back to the Pass-1 baseline requires no data migration undo beyond
dropping the new column/index, which is safe because nothing downstream depends on their
absence.

## Communicating the trade-off (topic 33 co-14)

The one trade-off a stakeholder outside engineering would actually care about: this capstone
adds ONE new read endpoint (`GET /habits/activity/recent`) whose entire purpose is to give the
SQL-tuning story something real to measure -- it is small, additive, and does not change any
existing endpoint's contract, so it ships with zero migration risk to existing API consumers.
