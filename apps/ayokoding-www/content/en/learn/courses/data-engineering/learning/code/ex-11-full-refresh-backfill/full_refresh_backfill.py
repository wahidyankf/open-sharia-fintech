"""Worked Example 11: Full-Refresh Backfill."""  # => co-06: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-06: both the incremental build and the full-refresh backfill target the same warehouse

SOURCE_ROWS = [(9001, 10.0), (9002, 25.0), (9003, 40.0), (9004, 5.0), (9005, 60.0)]  # => co-06: the SAME five source rows, used both ways


def build_incremental(con: duckdb.DuckDBPyConnection) -> None:  # => co-06: builds the table using ONLY the incremental filter's logic
    """Build gold_totals from scratch, ignoring the incremental filter -- as if every row were new."""  # => co-06: documents build_incremental's contract -- no runtime output, just sets its __doc__
    con.sql("CREATE OR REPLACE TABLE gold_totals AS SELECT SUM(amount) AS total FROM source_events")  # => co-06: a from-scratch, full aggregate


if __name__ == "__main__":  # => co-06: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-06: a fresh warehouse stand-in
    con.sql("CREATE TABLE source_events (event_id INTEGER, amount DOUBLE)")  # => co-06: the full, unfiltered source
    con.executemany("INSERT INTO source_events VALUES (?, ?)", SOURCE_ROWS)  # => co-06: land every source row, all five

    build_incremental(con)  # => co-06: the "routine incremental run" build, in this demo equivalent to a from-scratch aggregate
    incremental_total = con.sql("SELECT total FROM gold_totals").fetchone()[0]  # => co-06: the total AFTER the routine build
    print(f"Total after routine (incremental-shaped) build: {incremental_total}")  # => co-06: prints the routine total

    con.sql("CREATE OR REPLACE TABLE gold_totals AS SELECT SUM(amount) AS total FROM source_events")  # => co-06: FULL REFRESH -- ignores any watermark entirely
    backfill_total = con.sql("SELECT total FROM gold_totals").fetchone()[0]  # => co-06: the total AFTER the full-refresh backfill
    print(f"Total after full-refresh backfill: {backfill_total}")  # => co-06: prints the backfill total

    hand_computed_total = sum(amount for _, amount in SOURCE_ROWS)  # => co-06: 10+25+40+5+60, computed BY HAND from the source
    print(f"Hand-computed total: {hand_computed_total}")  # => co-06: prints the independently-computed expected value
    assert incremental_total == backfill_total == hand_computed_total, "a full-refresh backfill must equal a from-scratch build"  # => co-06
    print(f"MATCH: routine build, full-refresh backfill, and hand-computed total all equal {hand_computed_total}")  # => co-06
    # => co-06: because the transform is idempotent (co-05), a full backfill and a routine incremental build agree exactly
