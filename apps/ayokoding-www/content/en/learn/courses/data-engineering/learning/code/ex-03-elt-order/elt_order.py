"""Worked Example 3: ELT Order -- Load Before Transform."""  # => co-02: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-02: the load target AND the in-warehouse transform engine -- ELT does both in the same place
from pandas.api.types import is_string_dtype  # => co-02: backend-agnostic string check -- pandas 3.x's default string dtype prints as "str", not "object"

RAW_ROWS = [  # => co-02: the SAME raw, untyped, duplicate-laden rows ex-02 cleaned in Python FIRST
    ("1001", "129.50"),  # => co-02: row 1, amount arrives as TEXT
    ("1002", "40.00"),  # => co-02: row 2, amount arrives as TEXT
    ("1002", "40.00"),  # => co-02: row 3 -- an exact DUPLICATE of row 2
    ("1003", ""),  # => co-02: row 4 -- a blank amount, unusable downstream
]  # => co-02: closes RAW_ROWS -- ELT loads this exactly as-is, with zero Python-side cleaning

if __name__ == "__main__":  # => co-02: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-02: the warehouse stand-in -- BOTH load and transform happen inside it
    con.sql("CREATE TABLE raw_orders (order_id VARCHAR, amount VARCHAR)")  # => co-02: RAW schema -- everything stays TEXT
    con.executemany("INSERT INTO raw_orders VALUES (?, ?)", RAW_ROWS)  # => co-02: LOAD first -- untouched, untyped, unfiltered
    raw_loaded = con.sql("SELECT amount, order_id FROM raw_orders").df()  # => co-02: read back the raw landing table -- amount first so its blank cell never lands as invisible trailing whitespace when printed
    print(f"Raw landing table after LOAD ({len(raw_loaded)} rows, untouched):")  # => co-02
    print(raw_loaded)  # => co-02: prints the raw table -- still text, still has the duplicate and the blank

    transform_sql = "CREATE TABLE clean_orders AS SELECT DISTINCT CAST(order_id AS INTEGER) AS order_id, CAST(amount AS DOUBLE) AS amount FROM raw_orders WHERE amount != ''"  # => co-02: TRANSFORM, in-warehouse SQL -- the "T" AFTER "L"
    con.sql(transform_sql)  # => co-02: run the transform -- DISTINCT dedupes, CAST types, WHERE drops the blank, all AFTER load
    clean = con.sql("SELECT * FROM clean_orders ORDER BY order_id").df()  # => co-02: read back the transformed result
    print(f"Transformed in-warehouse ({len(clean)} rows):")  # => co-02
    print(clean)  # => co-02: prints the cleaned, typed table -- SQL did the work ex-02's Python did instead

    raw_untouched = len(raw_loaded) == len(RAW_ROWS) and is_string_dtype(raw_loaded["amount"])  # => co-02: still text, still 4 rows
    print(f"Raw landing table left untouched (4 rows, still text): {raw_untouched}")  # => co-02
    assert raw_untouched, "ELT's raw landing table must remain untouched by the transform step"  # => co-02: the claim ex-03 makes
    assert len(clean) == 2, "the in-warehouse transform must dedupe and drop the blank, same result as ex-02"  # => co-02
    print("MATCH: raw stayed untouched; the SAME cleaning ex-02 did in Python happened here, in SQL, after load")  # => co-02
    # => co-02: ELT = load, THEN transform -- cloud-warehouse elastic compute is what made this order cheap enough to prefer
