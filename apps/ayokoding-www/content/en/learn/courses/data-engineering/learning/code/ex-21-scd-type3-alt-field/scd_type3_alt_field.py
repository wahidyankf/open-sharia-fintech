"""Worked Example 21: SCD Type 3 -- Add a Prior-Value Column."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-11: Type 3 adds one extra column instead of adding a row or overwriting in place

if __name__ == "__main__":  # => co-11: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-11: a fresh warehouse stand-in
    con.sql("CREATE TABLE dim_customer (customer_id INTEGER, city VARCHAR, prior_city VARCHAR)")  # => co-11: ONE extra column -- prior_city
    con.execute("INSERT INTO dim_customer VALUES (?, ?, ?)", (501, "Bandung", None))  # => co-11: no prior value yet -- this is the FIRST value

    type3_update_sql = "UPDATE dim_customer SET prior_city = city, city = ? WHERE customer_id = ?"  # => co-11: TYPE 3 -- update BOTH columns in one statement
    type3_params = ("Medan", 501)  # => co-11: the new city value, and the customer this update targets
    con.execute(type3_update_sql, type3_params)  # => co-11: no new row (unlike Type 2), no lost value (unlike Type 1) -- ONE prior value retained
    row = con.sql("SELECT city, prior_city FROM dim_customer WHERE customer_id = 501").fetchone()  # => co-11: read back the single row
    current_city, prior_city = row  # => co-11: unpack the row's two relevant columns
    print(f"Current city: {current_city!r} | Prior city: {prior_city!r}")  # => co-11: prints both, readable from ONE row

    row_count = con.sql("SELECT COUNT(*) FROM dim_customer WHERE customer_id = 501").fetchone()[0]  # => co-11: still one row, like Type 1
    print(f"Row count for customer 501: {row_count}")  # => co-11: prints the row count -- expected 1
    assert row_count == 1, "Type 3 must never add a row -- like Type 1, it stays a single row"  # => co-11: the claim
    assert current_city == "Medan" and prior_city == "Bandung", "both the current AND the one prior value must be readable"  # => co-11
    print("MATCH: one row, both current and prior values readable side by side, no history beyond one step back")  # => co-11
    # => co-11: Type 3 trades Type 2's full history for a cheaper, single-row "what changed last time" query
