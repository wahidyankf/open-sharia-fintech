"""Worked Example 2: ETL Order -- Transform Before Load."""  # => co-02: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-02: the "load" target -- a local analytical SQL engine, standing in for a warehouse

RAW_ROWS = [  # => co-02: RAW, untyped source rows -- strings, a duplicate, and a stray blank
    {"order_id": "1001", "amount": "129.50"},  # => co-02: row 1, amount arrives as TEXT
    {"order_id": "1002", "amount": "40.00"},  # => co-02: row 2, amount arrives as TEXT
    {"order_id": "1002", "amount": "40.00"},  # => co-02: row 3 -- an exact DUPLICATE of row 2
    {"order_id": "1003", "amount": ""},  # => co-02: row 4 -- a blank amount, unusable downstream
]  # => co-02: closes RAW_ROWS -- exactly what ETL's "T" step must fix before anything is loaded


def clean_and_type(raw_rows: list[dict[str, str]]) -> list[dict[str, object]]:  # => co-02: the "T" in ETL -- runs in PYTHON, before load
    """Type, dedupe, and drop unusable rows -- entirely in Python, before any row reaches the warehouse."""  # => co-02: documents clean_and_type's contract -- no runtime output, just sets its __doc__
    seen_ids: set[str] = set()  # => co-02: tracks which order_id values have already been kept
    cleaned: list[dict[str, object]] = []  # => co-02: accumulates only typed, deduped, non-blank rows
    for row in raw_rows:  # => co-02: one raw row at a time
        if row["order_id"] in seen_ids or row["amount"] == "":  # => co-02: reject a duplicate id OR a blank amount
            continue  # => co-02: this row never reaches the load step at all
        seen_ids.add(row["order_id"])  # => co-02: record this id as kept, so a later duplicate is rejected
        cleaned.append({"order_id": int(row["order_id"]), "amount": float(row["amount"])})  # => co-02: TYPED here, in Python
    return cleaned  # => co-02: returns this computed value to the caller


if __name__ == "__main__":  # => co-02: entry point -- runs only when this file executes directly, not on import
    typed_rows = clean_and_type(RAW_ROWS)  # => co-02: transform happens BEFORE load -- this is the "T" then "L" order
    print(f"Transformed {len(typed_rows)} of {len(RAW_ROWS)} raw rows (deduped + typed + non-blank)")  # => co-02
    con = duckdb.connect()  # => co-02: an in-memory warehouse stand-in -- the "L" step writes into THIS
    con.sql("CREATE TABLE orders (order_id INTEGER, amount DOUBLE)")  # => co-02: the load target's schema, already TYPED
    con.executemany("INSERT INTO orders VALUES (?, ?)", [(r["order_id"], r["amount"]) for r in typed_rows])  # => co-02: LOAD -- already-clean rows only
    loaded = con.sql("SELECT * FROM orders ORDER BY order_id").df()  # => co-02: read back exactly what landed
    print(loaded)  # => co-02: prints the loaded table -- already typed, already deduped

    types_ok = str(loaded["amount"].dtype) == "float64"  # => co-02: the loaded column is DOUBLE, not text
    dedup_ok = len(loaded) == 2  # => co-02: two order_ids kept -- 1001 and 1002 (1003's blank amount dropped it)
    print(f"Loaded table already typed (float64): {types_ok} | already deduped (2 rows): {dedup_ok}")  # => co-02
    assert types_ok and dedup_ok, "ETL's load step must receive already-typed, already-deduped rows"  # => co-02: the claim
    print("MATCH: transformation ran in Python BEFORE the warehouse ever saw a row")  # => co-02
    # => co-02: ETL = transform, THEN load -- the warehouse never stores the raw, untyped, duplicate-laden rows at all
