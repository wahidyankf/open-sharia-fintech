"""Worked Example 5: Bronze -- Land Raw Data As-Is."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => co-04: writes the source CSV to a real file -- read_csv_auto needs a path, not an in-memory string
from pathlib import Path  # => co-04: builds the temp CSV's path

import duckdb  # => co-04: bronze lands INTO a local analytical engine, standing in for a lakehouse table

SOURCE_CSV_LINES = [  # => co-04: a small, invented CSV, built one row at a time -- includes a BLANK amount and a DUPLICATE, both left AS-IS
    "order_id,amount,region",  # => co-04: the CSV header row
    "3001,150.25,east",  # => co-04: row 1 -- clean
    "3002,,west",  # => co-04: row 2 -- a BLANK amount, left as-is in bronze
    "3002,,west",  # => co-04: row 3 -- an exact DUPLICATE of row 2
    "3003,72.10,north",  # => co-04: row 4 -- clean
]  # => co-04: closes SOURCE_CSV_LINES -- four data rows plus a header
SOURCE_CSV_TEXT = "\n".join(SOURCE_CSV_LINES) + "\n"  # => co-04: joined into the exact text a real CSV file drop would contain

if __name__ == "__main__":  # => co-04: entry point -- runs only when this file executes directly, not on import
    with tempfile.TemporaryDirectory() as tmp_dir:  # => co-04: a throwaway directory standing in for a source drop location
        csv_path = Path(tmp_dir) / "orders.csv"  # => co-04: the "source file" bronze will land as-is
        csv_path.write_text(SOURCE_CSV_TEXT, encoding="utf-8")  # => co-04: this course's rule -- data is generated, never downloaded

        con = duckdb.connect()  # => co-04: the bronze layer's home -- an in-memory local warehouse
        land_sql = f"CREATE TABLE bronze_orders AS SELECT *, now() AS load_ts FROM read_csv_auto('{csv_path}')"  # => co-04: LAND raw + load_ts -- Databricks docs: bronze keeps data "as-is" + load metadata
        con.sql(land_sql)  # => co-04: the whole bronze contract in one statement -- no cleaning, no dedup, no type coercion beyond CSV inference

        source_row_count = len(SOURCE_CSV_TEXT.strip().splitlines()) - 1  # => co-04: minus 1 for the CSV header line
        bronze_row_count = con.sql("SELECT COUNT(*) FROM bronze_orders").fetchone()[0]  # => co-04: what actually landed
        print(f"Source CSV rows: {source_row_count} | Bronze table rows: {bronze_row_count}")  # => co-04: prints both counts
        assert bronze_row_count == source_row_count, "bronze must land EVERY source row, including the duplicate and the blank"  # => co-04

        columns = con.sql("DESCRIBE bronze_orders").df()["column_name"].tolist()  # => co-04: what columns bronze actually has
        print(f"Bronze columns: {columns}")  # => co-04: prints the column list
        has_load_ts = "load_ts" in columns  # => co-04: the ONE thing bronze adds beyond the raw source
        print(f"Has load_ts metadata column: {has_load_ts}")  # => co-04: True -- metadata present, business columns untouched
        assert has_load_ts, "bronze must carry a load_ts metadata column alongside the untouched source columns"  # => co-04
        print(f"MATCH: {bronze_row_count} rows landed as-is, plus a load_ts metadata column")  # => co-04
        # => co-04: bronze is a faithful copy of the source PLUS load metadata -- cleaning is silver's job, not bronze's
