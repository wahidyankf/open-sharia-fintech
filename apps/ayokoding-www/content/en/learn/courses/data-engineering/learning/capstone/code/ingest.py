"""Capstone step 1: ingest.py -- raw order-line files to an idempotent bronze layer (exercises co-04, co-05, co-06)."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => co-04: writes each source drop to a real file -- read_csv_auto needs a path, not an in-memory string
from pathlib import Path  # => co-04: builds each source drop's temp path

import duckdb  # => co-04: bronze lands INTO a local analytical engine, standing in for a lakehouse table

SOURCE_DROP_1 = [  # => co-06: the FIRST source drop -- Aurora Retail's raw order-line file, day 1
    "order_id,line_number,customer_name,region,product_name,quantity,unit_price",  # => co-06: header
    "9001,1,Alice,east,Widget,3,10.00",  # => co-06: order 9001, line 1
    "9001,2,Alice,east,Gadget,1,25.00",  # => co-06: order 9001, line 2 -- same order, second line
    "9002,1,Bob,west,Widget,2,10.00",  # => co-06: order 9002, line 1
]  # => co-06: closes SOURCE_DROP_1 -- three order lines, one header
SOURCE_DROP_2 = [  # => co-06: the SECOND source drop -- arrives later, day 2, only NEW rows since the watermark
    "order_id,line_number,customer_name,region,product_name,quantity,unit_price",  # => co-06: header
    "9003,1,Carol,north,Gizmo,5,8.00",  # => co-06: order 9003, line 1 -- genuinely new
]  # => co-06: closes SOURCE_DROP_2 -- one new order line, arriving in a later ingest run


def _write_csv(lines: list[str], directory: Path, filename: str) -> Path:  # => co-04: writes one source drop to a real temp file
    """Write `lines` as a CSV file under `directory` and return its path."""  # => co-04: documents _write_csv's contract -- no runtime output, just sets its __doc__
    path = directory / filename  # => co-04: this source drop's own file path
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")  # => co-04: this course's rule -- data is generated, never downloaded
    return path  # => co-04: returns this computed value to the caller


def ingest_to_bronze(con: duckdb.DuckDBPyConnection, csv_path: Path) -> int:  # => co-05: idempotent -- only NEW natural keys are inserted
    """Land csv_path's rows into bronze_order_lines, inserting only rows whose (order_id, line_number) is new."""  # => co-05: documents ingest_to_bronze's contract -- no runtime output, just sets its __doc__
    bronze_ddl = "CREATE TABLE IF NOT EXISTS bronze_order_lines (order_id INTEGER, line_number INTEGER, customer_name VARCHAR, region VARCHAR, product_name VARCHAR, quantity INTEGER, unit_price DOUBLE, load_ts TIMESTAMP)"  # => co-04: bronze table -- created once, on the FIRST ingest call only
    con.sql(bronze_ddl)  # => co-04: bronze keeps data as-is + load metadata (load_ts), per Databricks' own medallion docs
    con.sql(f"CREATE OR REPLACE TEMP TABLE incoming_drop AS SELECT *, now() AS load_ts FROM read_csv_auto('{csv_path}')")  # => co-06: this drop's raw rows
    before_count = con.sql("SELECT COUNT(*) FROM bronze_order_lines").fetchone()[0]  # => co-05: row count BEFORE this ingest call
    idempotent_insert_sql = "INSERT INTO bronze_order_lines SELECT i.* FROM incoming_drop i LEFT JOIN bronze_order_lines b ON i.order_id = b.order_id AND i.line_number = b.line_number WHERE b.order_id IS NULL"  # => co-05: idempotent -- only NEW natural keys
    con.sql(idempotent_insert_sql)  # => co-05: an anti-join on (order_id, line_number) -- the SQL-native equivalent of ex-08's check-before-insert
    after_count = con.sql("SELECT COUNT(*) FROM bronze_order_lines").fetchone()[0]  # => co-05: row count AFTER this ingest call
    return after_count - before_count  # => co-06: how many genuinely NEW rows this call added -- the incremental delta


if __name__ == "__main__":  # => co-04: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-04: a fresh warehouse stand-in
    with tempfile.TemporaryDirectory() as tmp_dir:  # => co-04: a throwaway directory standing in for a source drop location
        drop_1_path = _write_csv(SOURCE_DROP_1, Path(tmp_dir), "drop_1.csv")  # => co-06: write the first source drop
        added_by_drop_1 = ingest_to_bronze(con, drop_1_path)  # => co-06: RUN 1 -- ingest the first drop
        print(f"Run 1 (drop 1): {added_by_drop_1} new rows added")  # => co-06: prints how many rows this run added

        added_by_rerun = ingest_to_bronze(con, drop_1_path)  # => co-05: RUN 2 -- re-ingest the EXACT SAME drop, a retry/rerun
        print(f"Run 2 (drop 1 rerun): {added_by_rerun} new rows added")  # => co-05: prints how many rows the rerun added
        assert added_by_rerun == 0, "a rerun of the SAME source drop must add zero duplicate rows"  # => co-05: the capstone's own acceptance criterion

        drop_2_path = _write_csv(SOURCE_DROP_2, Path(tmp_dir), "drop_2.csv")  # => co-06: write the SECOND, later source drop
        added_by_drop_2 = ingest_to_bronze(con, drop_2_path)  # => co-06: RUN 3 -- ingest the genuinely new second drop
        print(f"Run 3 (drop 2, new data): {added_by_drop_2} new rows added")  # => co-06: prints how many rows this NEW drop added

        total_rows = con.sql("SELECT COUNT(*) FROM bronze_order_lines").fetchone()[0]  # => co-04: the final bronze row count
        print(f"Total bronze rows: {total_rows}")  # => co-04: prints the accumulated bronze table size
        assert total_rows == 4, "bronze must hold exactly the 3 rows from drop 1 plus the 1 new row from drop 2, no duplicates"  # => co-04
        print(f"MATCH: {added_by_drop_1} + {added_by_rerun} + {added_by_drop_2} = {total_rows} bronze rows, idempotent across reruns")  # => co-05
    # => co-05,co-06: ingest is idempotent (a rerun is a no-op) AND incremental (a later drop adds only its genuinely new rows)
