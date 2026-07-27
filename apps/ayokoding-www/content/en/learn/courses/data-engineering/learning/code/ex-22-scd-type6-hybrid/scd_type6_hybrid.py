"""Worked Example 22: SCD Type 6 -- The 1+2+3 Hybrid."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-11: Type 6 combines Type 2's versioned rows with a Type-1-style overwritten "current value" column

if __name__ == "__main__":  # => co-11: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-11: a fresh warehouse stand-in
    type6_ddl = "CREATE TABLE dim_customer (surrogate_key INTEGER, customer_id INTEGER, city_at_event VARCHAR, current_city VARCHAR, effective_from DATE, effective_to DATE, is_current BOOLEAN)"  # => co-11: Type 2 rows PLUS a Type-1-style current_city
    con.sql(type6_ddl)  # => co-11: city_at_event is the Type-2 historical value; current_city is overwritten on EVERY row, Type-1-style
    type6_rows = [  # => co-11: two historical versions of ONE customer -- both rows share the SAME current_city after the update
        (1, 601, "Jakarta", "Jakarta", "2026-01-01", "2026-06-30", False),  # => co-11: version 1, before the Type-1 overwrite ran
        (2, 601, "Surabaya", "Surabaya", "2026-07-01", "9999-12-31", True),  # => co-11: version 2, current
    ]  # => co-11: closes type6_rows -- before the hybrid's Type-1 step, current_city still matches each row's own city_at_event
    con.executemany("INSERT INTO dim_customer VALUES (?, ?, ?, ?, ?, ?, ?)", type6_rows)  # => co-11: land both versions

    type1_half_sql = "UPDATE dim_customer SET current_city = ? WHERE customer_id = ?"  # => co-11: the TYPE-1 HALF of Type 6 -- overwrite EVERY row
    con.execute(type1_half_sql, ("Surabaya", 601))  # => co-11: this is the step that makes Type 6 a HYBRID -- both rows share the SAME current_city

    group_by_current_sql = "SELECT current_city, COUNT(*) FROM dim_customer WHERE customer_id = 601 GROUP BY current_city"  # => co-11: "total events by CURRENT city"
    group_by_current = con.sql(group_by_current_sql).df()  # => co-11: both versions collapse into ONE group, because current_city is now identical
    group_by_at_event_sql = "SELECT city_at_event, COUNT(*) FROM dim_customer WHERE customer_id = 601 GROUP BY city_at_event ORDER BY city_at_event"  # => co-11: "total events by city AT THE TIME" -- ORDER BY makes row order deterministic across runs (GROUP BY alone does not guarantee it)
    group_by_at_event = con.sql(group_by_at_event_sql).df()  # => co-11: two DIFFERENT groups, because city_at_event preserves history
    print("Grouped by current_city (Type-1-style, overwritten):")  # => co-11: frames the current-city grouping
    print(group_by_current)  # => co-11: prints ONE group -- both rows now say "Surabaya"
    print("Grouped by city_at_event (Type-2-style, historical):")  # => co-11: frames the historical grouping
    print(group_by_at_event)  # => co-11: prints TWO groups -- "Jakarta" and "Surabaya", each with one row

    totals_differ = len(group_by_current) != len(group_by_at_event)  # => co-11: the claim -- the two groupings disagree in shape
    print(f"Grouping counts differ ({len(group_by_current)} vs {len(group_by_at_event)}): {totals_differ}")  # => co-11
    assert totals_differ, "grouping by current value must give a different result than grouping by value-at-event"  # => co-11
    print("MATCH: current_city collapses history away; city_at_event preserves it -- both live on the same rows")  # => co-11
    # => co-11: Type 6 gives one dimension BOTH lenses at once -- "as it was" and "as it is now" -- at the cost of extra columns
