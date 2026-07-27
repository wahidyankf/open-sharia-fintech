"""Worked Example 34: Data Quality -- Completeness (Null Check)."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-16: a completeness check is an ordinary COUNT ... WHERE column IS NULL query

if __name__ == "__main__":  # => co-16: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-16: a fresh warehouse stand-in
    con.sql("CREATE TABLE orders (order_id INTEGER, customer_email VARCHAR)")  # => co-16: customer_email is REQUIRED -- a completeness dimension target
    order_rows = [  # => co-16: three good rows, one row with a missing (NULL) required field
        (1, "a@example.com"),  # => co-16: order 1 -- complete
        (2, "b@example.com"),  # => co-16: order 2 -- complete
        (3, None),  # => co-16: order 3 -- customer_email is NULL, the completeness violation this check must catch
        (4, "d@example.com"),  # => co-16: order 4 -- complete
    ]  # => co-16: closes order_rows
    con.executemany("INSERT INTO orders VALUES (?, ?)", order_rows)  # => co-16: land all four rows, including the incomplete one

    null_count = con.sql("SELECT COUNT(*) FROM orders WHERE customer_email IS NULL").fetchone()[0]  # => co-16: the completeness check itself
    completeness_passed = null_count == 0  # => co-16: the batch passes ONLY if every required field is populated
    print(f"Null customer_email rows: {null_count} | Completeness check passed: {completeness_passed}")  # => co-16
    assert not completeness_passed, "a batch with a null required field must fail the completeness check"  # => co-16: the claim ex-34 makes

    con.sql("DELETE FROM orders WHERE customer_email IS NULL")  # => co-16: fix the batch -- remove the row missing its required field
    null_count_after_fix = con.sql("SELECT COUNT(*) FROM orders WHERE customer_email IS NULL").fetchone()[0]  # => co-16: re-run the SAME check
    completeness_passed_after_fix = null_count_after_fix == 0  # => co-16: now the batch should pass
    print(f"Null customer_email rows after fix: {null_count_after_fix} | Completeness check passed: {completeness_passed_after_fix}")  # => co-16
    assert completeness_passed_after_fix, "the same check must pass once the null-valued row is removed"  # => co-16
    print("MATCH: the completeness check correctly fails a batch with a null required field, and passes once fixed")  # => co-16
    # => co-16: completeness is the cheapest data-quality dimension to check -- a required column must never be null
