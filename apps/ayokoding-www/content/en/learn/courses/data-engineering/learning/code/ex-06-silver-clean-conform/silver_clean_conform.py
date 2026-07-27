"""Worked Example 6: Silver -- Clean and Conform."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-04: silver is built with in-warehouse SQL, one layer downstream of bronze

if __name__ == "__main__":  # => co-04: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-04: a single connection carries bronze -> silver in this worked example
    con.sql("CREATE TABLE bronze_orders (order_id VARCHAR, amount VARCHAR, region VARCHAR)")  # => co-04: bronze -- everything TEXT, as landed
    bronze_rows = [  # => co-04: the SAME kind of bronze rows ex-05 landed -- a duplicate and a blank amount, left as-is
        ("4001", "310.00", "east"),  # => co-04: row 1 -- clean
        ("4002", "", "west"),  # => co-04: row 2 -- a BLANK amount
        ("4003", "88.50", "north"),  # => co-04: row 3 -- clean
        ("4003", "88.50", "north"),  # => co-04: row 4 -- an exact DUPLICATE of row 3
    ]  # => co-04: closes bronze_rows -- 4 bronze rows, matching Databricks' "as-is" bronze contract
    con.executemany("INSERT INTO bronze_orders VALUES (?, ?, ?)", bronze_rows)  # => co-04: land every row exactly as-is

    silver_sql = "CREATE TABLE silver_orders AS SELECT DISTINCT CAST(order_id AS INTEGER) AS order_id, CAST(amount AS DOUBLE) AS amount, region FROM bronze_orders WHERE amount != ''"  # => co-04: SILVER -- "matched, merged, conformed and cleansed"
    con.sql(silver_sql)  # => co-04: DISTINCT conforms duplicates away, CAST types every column, WHERE drops the unusable blank row
    silver = con.sql("SELECT * FROM silver_orders ORDER BY order_id").df()  # => co-04: read back silver's contents
    print(f"Bronze rows: 4 | Silver rows: {len(silver)}")  # => co-04: prints both counts, showing silver shrank
    print(silver)  # => co-04: prints the typed, deduped, non-null silver table

    types_cast = str(silver["order_id"].dtype).startswith("int") and str(silver["amount"].dtype) == "float64"  # => co-04: both columns TYPED
    no_duplicates = silver["order_id"].is_unique  # => co-04: the exact-duplicate bronze row must collapse to ONE silver row
    no_blanks = (silver["amount"] > 0).all()  # => co-04: the blank-amount bronze row must be entirely absent from silver
    print(f"Types cast: {types_cast} | No duplicate order_id: {no_duplicates} | No blank/zero amount: {no_blanks}")  # => co-04
    assert types_cast and no_duplicates and no_blanks, "silver must be typed, deduped, and null/blank-dropped"  # => co-04: the claim
    print(f"MATCH: silver conforms bronze's 4 raw rows down to {len(silver)} clean, typed, unique rows")  # => co-04
    # => co-04: silver's whole job is to make bronze SAFE to join and aggregate -- gold never has to re-clean anything
