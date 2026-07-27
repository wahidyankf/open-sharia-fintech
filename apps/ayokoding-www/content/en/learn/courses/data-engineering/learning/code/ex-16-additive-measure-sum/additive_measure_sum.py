"""Worked Example 16: Additive Measure -- Sums Across Every Dimension."""  # => co-10: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-10: an additive fact is checked by summing it multiple different ways and comparing

FACT_ROWS = [  # => co-10: revenue -- an ADDITIVE measure -- across two regions and two products
    ("east", "widget", 100.0),  # => co-10: east/widget row
    ("east", "gadget", 50.0),  # => co-10: east/gadget row
    ("west", "widget", 30.0),  # => co-10: west/widget row
    ("west", "gadget", 70.0),  # => co-10: west/gadget row -- 100+50+30+70 = 250.0 grand total
]  # => co-10: closes FACT_ROWS -- revenue sums correctly no matter which dimensions you group or drop

if __name__ == "__main__":  # => co-10: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-10: a fresh warehouse stand-in
    con.sql("CREATE TABLE fact_revenue (region VARCHAR, product VARCHAR, revenue DOUBLE)")  # => co-10: revenue is additive across BOTH dims
    con.executemany("INSERT INTO fact_revenue VALUES (?, ?, ?)", FACT_ROWS)  # => co-10: land all four fact rows

    grand_total = con.sql("SELECT SUM(revenue) FROM fact_revenue").fetchone()[0]  # => co-10: sum across EVERY dimension at once
    by_region = con.sql("SELECT SUM(revenue) FROM fact_revenue GROUP BY region").fetchdf()["sum(revenue)"].sum()  # => co-10: sum the per-region sums
    by_product = con.sql("SELECT SUM(revenue) FROM fact_revenue GROUP BY product").fetchdf()["sum(revenue)"].sum()  # => co-10: sum the per-product sums
    print(f"Grand total: {grand_total} | Sum of per-region sums: {by_region} | Sum of per-product sums: {by_product}")  # => co-10

    all_equal = grand_total == by_region == by_product == 250.0  # => co-10: additive means EVERY grouping still reconciles to the same total
    print(f"All three totals agree at 250.0: {all_equal}")  # => co-10: prints the reconciliation check
    assert all_equal, "an additive measure must sum consistently regardless of which dimension you group by"  # => co-10: the claim
    print("MATCH: revenue sums to the identical grand total, whether grouped by region, by product, or not at all")  # => co-10
    # => co-10: additive facts are the SAFEST default -- summing across any subset of dimensions never produces a wrong answer
