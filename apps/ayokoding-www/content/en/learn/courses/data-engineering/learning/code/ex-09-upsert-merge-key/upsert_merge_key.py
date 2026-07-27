"""Worked Example 9: Upsert via MERGE on a Natural Key."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-05: DuckDB 1.5.5's MERGE INTO statement backs this worked example's upsert

if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-05: a fresh warehouse stand-in
    con.sql("CREATE TABLE target_orders (order_id INTEGER PRIMARY KEY, status VARCHAR)")  # => co-05: the table an upsert lands into
    con.execute("INSERT INTO target_orders VALUES (?, ?)", (7001, "pending"))  # => co-05: one PRE-EXISTING row, natural key 7001

    con.sql("CREATE TABLE incoming_batch (order_id INTEGER, status VARCHAR)")  # => co-05: this run's incoming batch -- a natural-key CHANGE plus a brand-new row
    incoming_rows = [(7001, "shipped"), (7002, "pending")]  # => co-05: 7001 CHANGED status, 7002 is a brand-NEW order
    con.executemany("INSERT INTO incoming_batch VALUES (?, ?)", incoming_rows)  # => co-05: land the incoming batch

    merge_sql = "MERGE INTO target_orders USING incoming_batch ON target_orders.order_id = incoming_batch.order_id WHEN MATCHED THEN UPDATE SET status = incoming_batch.status WHEN NOT MATCHED THEN INSERT (order_id, status) VALUES (incoming_batch.order_id, incoming_batch.status)"  # => co-05: MERGE on natural key
    con.sql(merge_sql)  # => co-05: matched rows UPDATE in place; unmatched rows INSERT -- never a duplicate row for an existing key
    result = con.sql("SELECT * FROM target_orders ORDER BY order_id").df()  # => co-05: read back the merged table
    print(result)  # => co-05: prints the merged table -- 7001 updated, 7002 inserted, still exactly 2 rows

    row_count = len(result)  # => co-05: total rows after the merge
    status_7001 = result.loc[result["order_id"] == 7001, "status"].iloc[0]  # => co-05: 7001's status AFTER the merge
    print(f"Row count: {row_count} | Order 7001 status: {status_7001!r}")  # => co-05: prints both checks
    assert row_count == 2, "a changed existing key must UPDATE in place, not add a duplicate row"  # => co-05: the claim
    assert status_7001 == "shipped", "the matched row's status must reflect the incoming batch's new value"  # => co-05
    print("MATCH: the changed key updated in place; the new key inserted; no duplicate row exists for 7001")  # => co-05
    # => co-05: MERGE on a natural key is the SQL-native way to make a load idempotent -- the same guarantee ex-08 built by hand
