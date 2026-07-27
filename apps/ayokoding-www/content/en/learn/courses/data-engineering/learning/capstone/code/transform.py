"""Capstone step 2: transform.py -- bronze to silver to a star schema (exercises co-04, co-08, co-09)."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => co-04: this step's own standalone demo re-ingests a source drop to have bronze to transform
from pathlib import Path  # => co-04: builds the standalone demo's temp source-drop path

import duckdb  # => co-04: silver and the star schema are both built with in-warehouse SQL

from ingest import SOURCE_DROP_1, _write_csv, ingest_to_bronze  # => co-04: reuse step 1's own ingest -- this capstone's files import from one another


def transform_to_silver(con: duckdb.DuckDBPyConnection) -> None:  # => co-04: bronze -> silver -- typed, deduped, validated
    """Clean bronze_order_lines into silver_order_lines: typed, deduped, validated, with a computed amount."""  # => co-04: documents transform_to_silver's contract -- no runtime output, just sets its __doc__
    silver_sql = "CREATE OR REPLACE TABLE silver_order_lines AS SELECT DISTINCT order_id, line_number, customer_name, region, product_name, quantity, unit_price, quantity * unit_price AS amount FROM bronze_order_lines WHERE customer_name IS NOT NULL AND quantity > 0 AND unit_price > 0"  # => co-16: DQ gates inline
    con.sql(silver_sql)  # => co-04: DISTINCT dedupes; the WHERE clause drops any incomplete or invalid row before it reaches the star schema


def transform_to_star_schema(con: duckdb.DuckDBPyConnection) -> None:  # => co-08: silver -> fact + dimension tables
    """Split silver_order_lines into dim_customer, dim_product, and fact_order_line."""  # => co-08: documents transform_to_star_schema's contract -- no runtime output, just sets its __doc__
    dim_customer_sql = "CREATE OR REPLACE TABLE dim_customer AS SELECT ROW_NUMBER() OVER () AS customer_key, customer_name FROM (SELECT DISTINCT customer_name FROM silver_order_lines)"  # => co-08: DIMENSION 1 -- customer
    con.sql(dim_customer_sql)  # => co-08: the descriptive-attribute half of the split, given its own surrogate key
    dim_product_sql = "CREATE OR REPLACE TABLE dim_product AS SELECT ROW_NUMBER() OVER () AS product_key, product_name FROM (SELECT DISTINCT product_name FROM silver_order_lines)"  # => co-08: DIMENSION 2 -- product
    con.sql(dim_product_sql)  # => co-08: the SECOND dimension -- product, its own surrogate key
    sql = "CREATE OR REPLACE TABLE fact_order_line AS SELECT order_id, line_number, customer_key, product_key, region, quantity, unit_price, amount FROM silver_order_lines s JOIN dim_customer c ON s.customer_name = c.customer_name JOIN dim_product p ON s.product_name = p.product_name"  # => co-09: FACT
    con.sql(sql)  # => co-09: the fact table -- numeric measurements (quantity, unit_price, amount) with FK context


if __name__ == "__main__":  # => co-04: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-04: a fresh warehouse stand-in
    with tempfile.TemporaryDirectory() as tmp_dir:  # => co-04: a throwaway directory standing in for a source drop location
        drop_1_path = _write_csv(SOURCE_DROP_1, Path(tmp_dir), "drop_1.csv")  # => co-04: reuse step 1's own fixture data
        ingest_to_bronze(con, drop_1_path)  # => co-04: run step 1's OWN function -- sets up this step's own precondition

    transform_to_silver(con)  # => co-04: STEP 2a -- bronze -> silver
    transform_to_star_schema(con)  # => co-08: STEP 2b -- silver -> star schema

    silver_count = con.sql("SELECT COUNT(*) FROM silver_order_lines").fetchone()[0]  # => co-04: silver's own row count
    fact_count = con.sql("SELECT COUNT(*) FROM fact_order_line").fetchone()[0]  # => co-09: the fact table's row count -- must match silver's grain
    print(f"Silver rows: {silver_count} | Fact rows: {fact_count}")  # => co-04: prints both counts for a quick reconciliation check
    assert silver_count == fact_count, "the fact table must have exactly one row per silver row, matching the declared grain"  # => co-09

    unresolved_customers_sql = "SELECT COUNT(*) FROM fact_order_line f LEFT JOIN dim_customer c ON f.customer_key = c.customer_key WHERE c.customer_key IS NULL"  # => co-08: does EVERY fact row's customer_key resolve?
    unresolved_customers = con.sql(unresolved_customers_sql).fetchone()[0]  # => co-08: a left join finding ZERO means every foreign key resolves
    unresolved_products_sql = "SELECT COUNT(*) FROM fact_order_line f LEFT JOIN dim_product p ON f.product_key = p.product_key WHERE p.product_key IS NULL"  # => co-08: does EVERY fact row's product_key resolve?
    unresolved_products = con.sql(unresolved_products_sql).fetchone()[0]  # => co-08: a left join finding ZERO means every foreign key resolves
    print(f"Unresolved customer FKs: {unresolved_customers} | Unresolved product FKs: {unresolved_products}")  # => co-08
    assert unresolved_customers == 0 and unresolved_products == 0, "every fact row's foreign keys must resolve to real dimension rows"  # => co-08
    print(f"MATCH: {fact_count} fact rows reconcile with silver's {silver_count} rows, every foreign key resolves")  # => co-09
    # => co-08,co-09: the star schema's grain and referential integrity both hold -- ready for gold aggregation
