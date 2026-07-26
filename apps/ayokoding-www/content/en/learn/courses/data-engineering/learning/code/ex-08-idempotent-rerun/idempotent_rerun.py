"""Worked Example 8: Idempotent Rerun."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-05: the target table this idempotent step writes into

SOURCE_ROWS = [(6001, "alice", 42.0), (6002, "bob", 17.5), (6003, "carol", 90.0)]  # => co-05: the SAME source rows, loaded TWICE


def run_etl_step(con: duckdb.DuckDBPyConnection) -> None:  # => co-05: the step under test -- must be safe to run more than once
    """Insert every source row, but only if its natural key isn't already present -- an idempotent load."""  # => co-05: documents run_etl_step's contract -- no runtime output, just sets its __doc__
    for order_id, customer, amount in SOURCE_ROWS:  # => co-05: one source row at a time
        already_present = con.sql("SELECT COUNT(*) FROM orders WHERE order_id = ?", params=[order_id]).fetchone()[0] > 0  # => co-05: check the natural key FIRST -- parameterized, matching the INSERT two lines below
        if not already_present:  # => co-05: only insert a row this run has not already seen
            con.execute("INSERT INTO orders VALUES (?, ?, ?)", (order_id, customer, amount))  # => co-05: insert exactly once, ever


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-05: a fresh, empty warehouse stand-in
    con.sql("CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer VARCHAR, amount DOUBLE)")  # => co-05: order_id is the natural key
    run_etl_step(con)  # => co-05: RUN 1 -- the first execution of this ETL step
    count_after_run_1 = con.sql("SELECT COUNT(*) FROM orders").fetchone()[0]  # => co-05: row count after the first run
    print(f"Row count after run 1: {count_after_run_1}")  # => co-05: prints the count -- expected 3, one per source row

    run_etl_step(con)  # => co-05: RUN 2 -- the EXACT SAME step, run again, on the SAME source rows
    count_after_run_2 = con.sql("SELECT COUNT(*) FROM orders").fetchone()[0]  # => co-05: row count after the SECOND run
    print(f"Row count after run 2 (rerun, same source): {count_after_run_2}")  # => co-05: prints the count again

    duplicates_added = count_after_run_2 - count_after_run_1  # => co-05: the whole point of ex-08 -- how many NEW rows did the rerun add?
    print(f"Duplicate rows added by the rerun: {duplicates_added}")  # => co-05: 0 -- the rerun changed nothing
    assert duplicates_added == 0, "an idempotent step must add zero duplicate rows on a rerun"  # => co-05: the claim ex-08 makes
    print(f"MATCH: {count_after_run_1} rows after run 1, still {count_after_run_2} rows after an identical rerun")  # => co-05
    # => co-05: idempotency is what makes a retry, a re-trigger, or an operator's manual rerun SAFE instead of destructive
