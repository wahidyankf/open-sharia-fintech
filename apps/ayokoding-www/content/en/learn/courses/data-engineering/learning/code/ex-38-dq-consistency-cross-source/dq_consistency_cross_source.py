"""Worked Example 38: Data Quality -- Consistency (Cross-Source Reconciliation)."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-16: consistency is checked by comparing an aggregate computed from TWO independent sources

if __name__ == "__main__":  # => co-16: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-16: a fresh warehouse stand-in
    con.sql("CREATE TABLE orders_from_app_db (order_id INTEGER, amount DOUBLE)")  # => co-16: SOURCE 1 -- the application database's own record
    con.sql("CREATE TABLE orders_from_payment_gateway (order_id INTEGER, amount DOUBLE)")  # => co-16: SOURCE 2 -- an independent, external record of the same orders
    con.executemany("INSERT INTO orders_from_app_db VALUES (?, ?)", [(1, 100.0), (2, 50.0), (3, 75.0)])  # => co-16: the app DB's own totals
    con.executemany("INSERT INTO orders_from_payment_gateway VALUES (?, ?)", [(1, 100.0), (2, 50.0), (3, 60.0)])  # => co-16: order 3 DISAGREES -- 60 vs. 75

    app_total = con.sql("SELECT SUM(amount) FROM orders_from_app_db").fetchone()[0]  # => co-16: SOURCE 1's total
    gateway_total = con.sql("SELECT SUM(amount) FROM orders_from_payment_gateway").fetchone()[0]  # => co-16: SOURCE 2's INDEPENDENT total
    print(f"App DB total: {app_total} | Payment gateway total: {gateway_total}")  # => co-16: prints both independent totals

    consistency_passed = app_total == gateway_total  # => co-16: the consistency check -- do two independent sources agree?
    print(f"Consistency check passed (totals reconcile): {consistency_passed}")  # => co-16: prints the reconciliation verdict
    assert not consistency_passed, "a mismatch between two independent sources' totals must fail the consistency check"  # => co-16: the claim ex-38 makes

    mismatch_sql = "SELECT a.order_id, a.amount AS app_amount, g.amount AS gateway_amount FROM orders_from_app_db a JOIN orders_from_payment_gateway g ON a.order_id = g.order_id WHERE a.amount != g.amount"  # => co-16: pinpoint WHICH order caused the mismatch
    mismatched_orders = con.sql(mismatch_sql).df()  # => co-16: a per-row join comparison, pinpointing the exact disagreement
    print(mismatched_orders)  # => co-16: prints the exact order where the two sources disagree
    assert mismatched_orders["order_id"].tolist() == [3], "the mismatch must be traceable to exactly order_id 3"  # => co-16
    print(f"MATCH: totals disagree ({app_total} vs {gateway_total}), pinpointed to order_id 3's conflicting amount")  # => co-16
    # => co-16: consistency catches errors NEITHER individual source's own completeness/validity/uniqueness checks can see alone
