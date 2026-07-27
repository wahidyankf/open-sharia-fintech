"""Worked Example 35: Data Quality -- Uniqueness (Duplicate Key Check)."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-16: a uniqueness check is an ordinary GROUP BY key HAVING COUNT(*) > 1 query

if __name__ == "__main__":  # => co-16: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-16: a fresh warehouse stand-in
    con.sql("CREATE TABLE customers (customer_id INTEGER, name VARCHAR)")  # => co-16: customer_id is the key -- UNIQUENESS is the dimension under test
    customer_rows = [  # => co-16: four rows, with customer_id 7 appearing TWICE -- exactly a uniqueness violation
        (5, "Alice"),  # => co-16: customer 5 -- unique
        (6, "Bob"),  # => co-16: customer 6 -- unique
        (7, "Carol"),  # => co-16: customer 7, first occurrence
        (7, "Carol-duplicate-row"),  # => co-16: customer 7, SECOND occurrence -- a genuine key-uniqueness violation
    ]  # => co-16: closes customer_rows
    con.executemany("INSERT INTO customers VALUES (?, ?)", customer_rows)  # => co-16: land all four rows

    dup_check_sql = "SELECT customer_id FROM customers GROUP BY customer_id HAVING COUNT(*) > 1"  # => co-16: the uniqueness check -- which keys appear more than once?
    duplicate_keys = con.sql(dup_check_sql).df()["customer_id"].tolist()  # => co-16: every key value that violates uniqueness
    uniqueness_passed = len(duplicate_keys) == 0  # => co-16: the batch passes ONLY if every key is genuinely unique
    print(f"Duplicate customer_id values: {duplicate_keys} | Uniqueness check passed: {uniqueness_passed}")  # => co-16
    assert not uniqueness_passed, "a batch with a duplicated key must fail the uniqueness check"  # => co-16: the claim ex-35 makes
    assert duplicate_keys == [7], "the check must identify exactly customer_id 7 as the duplicated key"  # => co-16

    con.sql("DELETE FROM customers WHERE name = 'Carol-duplicate-row'")  # => co-16: fix the batch -- remove the duplicate row
    duplicate_keys_after_fix = con.sql(dup_check_sql).df()["customer_id"].tolist()  # => co-16: re-run the SAME check -- should now be empty
    print(f"Duplicate customer_id values after fix: {duplicate_keys_after_fix}")  # => co-16: prints the post-fix check
    assert duplicate_keys_after_fix == [], "the same check must pass once the duplicate row is removed"  # => co-16
    print("MATCH: the uniqueness check correctly fails a batch with a duplicated key, and passes once fixed")  # => co-16
    # => co-16: uniqueness catches the exact failure mode co-05's idempotent-load discipline is designed to prevent in the first place
