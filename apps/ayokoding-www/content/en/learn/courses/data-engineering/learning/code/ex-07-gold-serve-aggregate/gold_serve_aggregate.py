"""Worked Example 7: Gold -- Serve a Consumption-Ready Aggregate."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-04: gold is one more in-warehouse SQL step downstream of silver

if __name__ == "__main__":  # => co-04: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-04: a single connection carries silver -> gold in this worked example
    con.sql("CREATE TABLE silver_orders (order_id INTEGER, amount DOUBLE, region VARCHAR)")  # => co-04: silver -- already typed, deduped, clean
    silver_rows = [  # => co-04: five already-clean silver rows across three regions
        (5001, 100.0, "east"),  # => co-04: east, row 1
        (5002, 250.0, "east"),  # => co-04: east, row 2
        (5003, 75.0, "west"),  # => co-04: west, row 1
        (5004, 40.0, "west"),  # => co-04: west, row 2
        (5005, 60.0, "north"),  # => co-04: north, row 1
    ]  # => co-04: closes silver_rows -- silver's clean state means gold never re-types or re-dedupes anything, only aggregates
    con.executemany("INSERT INTO silver_orders VALUES (?, ?, ?)", silver_rows)  # => co-04: land every already-clean silver row

    gold_sql = "CREATE TABLE gold_region_totals AS SELECT region, SUM(amount) AS total_amount, COUNT(*) AS order_count FROM silver_orders GROUP BY region"  # => co-04: GOLD -- "consumption-ready, de-normalized, read-optimized"
    con.sql(gold_sql)  # => co-04: one served row PER region -- exactly the shape a dashboard would query directly, no further joins needed
    gold = con.sql("SELECT * FROM gold_region_totals ORDER BY region").df()  # => co-04: read back the served aggregate
    print(gold)  # => co-04: prints the gold table -- region, total, count

    hand_computed_east = 100.0 + 250.0  # => co-04: the expected east total, computed BY HAND from the raw inputs above
    hand_computed_west = 75.0 + 40.0  # => co-04: the expected west total, computed BY HAND
    served_east = gold.loc[gold["region"] == "east", "total_amount"].iloc[0]  # => co-04: what gold actually served for east
    served_west = gold.loc[gold["region"] == "west", "total_amount"].iloc[0]  # => co-04: what gold actually served for west
    print(f"East: hand-computed {hand_computed_east} vs. served {served_east}")  # => co-04: prints the comparison
    print(f"West: hand-computed {hand_computed_west} vs. served {served_west}")  # => co-04: prints the comparison
    assert served_east == hand_computed_east and served_west == hand_computed_west, "gold's totals must match hand-computed values"  # => co-04
    print("MATCH: gold's served totals equal the hand-computed sums for every region")  # => co-04
    # => co-04: gold is where a dashboard or ML feature store reads FROM -- it never touches bronze or silver directly
