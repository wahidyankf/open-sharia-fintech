"""Worked Example 15: Star Schema and Grain."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-09: a star schema's grain is checked with an ordinary GROUP BY / HAVING query

if __name__ == "__main__":  # => co-09: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-09: a fresh warehouse stand-in
    con.sql("CREATE TABLE dim_product (product_key INTEGER, product_name VARCHAR)")  # => co-09: a small dimension table
    con.executemany("INSERT INTO dim_product VALUES (?, ?)", [(1, "Widget"), (2, "Gadget")])  # => co-09: two products
    grain_ddl = "CREATE TABLE fact_order_line (order_id INTEGER, line_number INTEGER, product_key INTEGER, quantity INTEGER)"  # => co-09: DECLARED GRAIN -- "one row per order line"
    con.sql(grain_ddl)  # => co-09: order_id + line_number together identify exactly one grain-conforming row
    order_lines = [  # => co-09: order 101 has TWO lines (one row each); order 102 has ONE line (one row)
        (101, 1, 1, 3),  # => co-09: order 101, line 1 -- widget, qty 3
        (101, 2, 2, 1),  # => co-09: order 101, line 2 -- gadget, qty 1
        (102, 1, 1, 5),  # => co-09: order 102, line 1 -- widget, qty 5
    ]  # => co-09: closes order_lines -- three fact rows total, exactly matching the declared grain
    con.executemany("INSERT INTO fact_order_line VALUES (?, ?, ?, ?)", order_lines)  # => co-09: land every declared order line

    fact = con.sql("SELECT * FROM fact_order_line ORDER BY order_id, line_number").df()  # => co-09: read back the fact table
    print(fact)  # => co-09: prints the fact table -- one row per (order_id, line_number)

    grain_check_sql = "SELECT COUNT(*) FROM (SELECT order_id, line_number, COUNT(*) AS c FROM fact_order_line GROUP BY order_id, line_number HAVING COUNT(*) > 1)"  # => co-09: does (order_id, line_number) uniquely identify every row?
    grain_violations = con.sql(grain_check_sql).fetchone()[0]  # => co-09: any pair appearing MORE than once would violate the declared grain
    print(f"Grain violations -- (order_id, line_number) pairs appearing more than once: {grain_violations}")  # => co-09
    assert grain_violations == 0, "no row may be finer or coarser than the declared one-row-per-order-line grain"  # => co-09: the claim
    assert len(fact) == 3, "three declared order lines must produce exactly three fact rows -- neither collapsed nor split"  # => co-09
    print(f"MATCH: {len(fact)} fact rows, each an exactly-one-row-per-order-line grain match, zero violations")  # => co-09
    # => co-09: declaring the grain up front is what lets every LATER worked example know exactly what one fact row means
