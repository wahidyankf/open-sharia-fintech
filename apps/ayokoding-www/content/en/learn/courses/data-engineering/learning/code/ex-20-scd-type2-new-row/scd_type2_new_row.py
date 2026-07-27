"""Worked Example 20: SCD Type 2 -- New Row, Effective-Date Range, Current Flag."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-11: Type 2 is modeled with real DATE columns and a boolean current-row flag

if __name__ == "__main__":  # => co-11: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-11: a fresh warehouse stand-in
    type2_ddl = "CREATE TABLE dim_customer (surrogate_key INTEGER, customer_id INTEGER, city VARCHAR, effective_from DATE, effective_to DATE, is_current BOOLEAN)"  # => co-11: the Type 2 shape -- surrogate key, natural key, attribute, effective range, current flag
    con.sql(type2_ddl)  # => co-11: exactly the five Type-2-specific columns Kimball's own definition names
    version_1 = (1, 401, "Jakarta", "2026-01-01", "2026-06-30", False)  # => co-11: VERSION 1 -- original city, CLOSED on 2026-06-30
    con.execute("INSERT INTO dim_customer VALUES (?, ?, ?, ?, ?, ?)", version_1)  # => co-11: insert version 1 -- range closed the day before the change
    version_2 = (2, 401, "Surabaya", "2026-07-01", "9999-12-31", True)  # => co-11: VERSION 2 -- NEW city, starting where version 1 closed, current
    con.execute("INSERT INTO dim_customer VALUES (?, ?, ?, ?, ?, ?)", version_2)  # => co-11: a new ROW, not an overwrite -- both versions coexist

    both_versions = con.sql("SELECT * FROM dim_customer WHERE customer_id = 401 ORDER BY surrogate_key").df()  # => co-11: read back both rows
    print(both_versions)  # => co-11: prints both versions -- two rows for one customer_id, disjoint date ranges

    version_count = len(both_versions)  # => co-11: how many versions exist for this customer
    current_count = int(both_versions["is_current"].sum())  # => co-11: how many are marked current -- must be exactly one
    ranges_disjoint = both_versions.iloc[0]["effective_to"] < both_versions.iloc[1]["effective_from"]  # => co-11: no date overlap between versions
    print(f"Versions: {version_count} | Current-flagged: {current_count} | Ranges disjoint: {ranges_disjoint}")  # => co-11
    assert version_count == 2, "Type 2 must retain BOTH versions as separate rows, unlike Type 1's overwrite"  # => co-11: the claim
    assert current_count == 1, "exactly one version must be marked current at any given time"  # => co-11
    assert ranges_disjoint, "the two versions' effective-date ranges must not overlap"  # => co-11
    print("MATCH: two versions, disjoint effective-date ranges, exactly one marked current")  # => co-11
    # => co-11: Type 2 is what lets a query ask "what was true as of a past date," which Type 1's overwrite can never answer
