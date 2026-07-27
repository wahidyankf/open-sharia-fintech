"""Worked Example 19: SCD Type 1 -- Overwrite, No History."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-11: a Type 1 SCD update is an ordinary UPDATE statement -- the whole point is that it keeps no history

if __name__ == "__main__":  # => co-11: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-11: a fresh warehouse stand-in
    con.sql("CREATE TABLE dim_customer (customer_id INTEGER, city VARCHAR)")  # => co-11: a slowly-changing dimension attribute -- city
    con.execute("INSERT INTO dim_customer VALUES (?, ?)", (301, "Jakarta"))  # => co-11: the ORIGINAL value -- before any change

    original_city = con.sql("SELECT city FROM dim_customer WHERE customer_id = 301").fetchone()[0]  # => co-11: the value BEFORE the change
    print(f"Original city: {original_city!r}")  # => co-11: prints the pre-change value

    con.execute("UPDATE dim_customer SET city = ? WHERE customer_id = ?", ("Surabaya", 301))  # => co-11: TYPE 1 -- overwrite in place, no new row
    updated_city = con.sql("SELECT city FROM dim_customer WHERE customer_id = 301").fetchone()[0]  # => co-11: the value AFTER the change
    print(f"Updated city: {updated_city!r}")  # => co-11: prints the post-change value

    row_count = con.sql("SELECT COUNT(*) FROM dim_customer WHERE customer_id = 301").fetchone()[0]  # => co-11: how many rows exist for this customer
    print(f"Row count for customer 301: {row_count}")  # => co-11: prints the row count -- must still be exactly 1
    assert row_count == 1, "Type 1 must never add a row -- it overwrites the existing one in place"  # => co-11: the claim
    assert updated_city == "Surabaya" and original_city != updated_city, "the value must change, with nothing retaining the old one"  # => co-11
    no_prior_value_anywhere = con.sql("SELECT COUNT(*) FROM dim_customer WHERE city = ?", params=["Jakarta"]).fetchone()[0] == 0  # => co-11: the OLD value is gone
    print(f"No row anywhere retains the prior value 'Jakarta': {no_prior_value_anywhere}")  # => co-11
    assert no_prior_value_anywhere, "Type 1 must retain no prior value anywhere in the table"  # => co-11: the defining property
    print("MATCH: one row, overwritten in place -- the prior value is gone, with no history retained")  # => co-11
    # => co-11: Type 1 is the simplest SCD type -- correct for attributes where history genuinely does not matter
