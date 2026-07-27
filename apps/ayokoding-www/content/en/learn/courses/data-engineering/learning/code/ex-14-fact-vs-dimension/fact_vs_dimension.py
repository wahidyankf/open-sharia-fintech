"""Worked Example 14: Fact vs. Dimension."""  # => co-08: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-08: splits one flat table into a fact table and a dimension table via SQL

FLAT_ROWS = [  # => co-08: a single denormalized table -- customer NAME repeated once per order, a classic flat-file shape
    (1, "Alice", 120.0),  # => co-08: order 1, Alice
    (2, "Alice", 45.0),  # => co-08: order 2, Alice again -- the REPEATED name flat data forces
    (3, "Bob", 300.0),  # => co-08: order 3, Bob
    (4, "Carol", 15.0),  # => co-08: order 4, Carol
]  # => co-08: closes FLAT_ROWS -- four orders, three distinct customers, one repeated (Alice)

if __name__ == "__main__":  # => co-08: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-08: a fresh warehouse stand-in
    con.sql("CREATE TABLE flat_orders (order_id INTEGER, customer_name VARCHAR, amount DOUBLE)")  # => co-08: the flat, denormalized source
    con.executemany("INSERT INTO flat_orders VALUES (?, ?, ?)", FLAT_ROWS)  # => co-08: land all four flat rows

    dim_sql = "CREATE TABLE dim_customer AS SELECT ROW_NUMBER() OVER () AS customer_key, customer_name FROM (SELECT DISTINCT customer_name FROM flat_orders)"  # => co-08: DIMENSION -- the descriptive attribute, given its OWN surrogate key
    con.sql(dim_sql)  # => co-08: one row PER DISTINCT customer -- exactly the descriptive-attribute half of the split
    fact_sql = "CREATE TABLE fact_orders AS SELECT f.order_id, d.customer_key, f.amount FROM flat_orders f JOIN dim_customer d ON f.customer_name = d.customer_name"  # => co-08: FACT -- numeric measurement + FK, Kimball's own definition
    con.sql(fact_sql)  # => co-08: fact = numeric measurement (amount) + FK context (customer_key)

    dim_customer = con.sql("SELECT * FROM dim_customer ORDER BY customer_key").df()  # => co-08: read back the dimension
    fact_orders = con.sql("SELECT * FROM fact_orders ORDER BY order_id").df()  # => co-08: read back the fact table
    print("dim_customer:")  # => co-08: frames the dimension table's printout
    print(dim_customer)  # => co-08: prints the dimension -- one row per distinct customer
    print("fact_orders:")  # => co-08: frames the fact table's printout
    print(fact_orders)  # => co-08: prints the fact table -- one row per order, FK to dim_customer

    unresolved_sql = "SELECT COUNT(*) FROM fact_orders f LEFT JOIN dim_customer d ON f.customer_key = d.customer_key WHERE d.customer_key IS NULL"  # => co-08: does EVERY fact row's FK resolve to a real dimension row?
    unresolved = con.sql(unresolved_sql).fetchone()[0]  # => co-08: a left join that finds ZERO means every FK resolves
    print(f"Fact rows with an unresolved customer_key: {unresolved}")  # => co-08: prints the count -- expected 0
    assert unresolved == 0, "every fact row's foreign key must resolve to a real dimension row"  # => co-08: the claim ex-14 makes
    assert len(dim_customer) == 3, "the dimension must have exactly one row per distinct customer, not one per order"  # => co-08
    print(f"MATCH: all {len(fact_orders)} fact rows resolve to one of {len(dim_customer)} dimension rows")  # => co-08
    # => co-08: splitting flat data into fact + dimension is what makes "rename Alice" a ONE-row update, not a four-row one
