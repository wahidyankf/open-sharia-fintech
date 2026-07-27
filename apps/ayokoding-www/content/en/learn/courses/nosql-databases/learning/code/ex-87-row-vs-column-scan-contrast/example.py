"""Example 87: Row vs. Column Scan Contrast."""  # => co-33,co-34: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import LiteralString  # => co-33: both call sites below pass a compile-time string constant -- LiteralString states that honestly

import duckdb  # => co-33: duckdb, the official Python API for the in-process, MIT-licensed columnar OLAP engine
import psycopg  # => co-33: psycopg, the official typed Python driver for PostgreSQL -- the row-store side of this contrast
from psycopg import sql  # => co-33: composes the literal query into a genuinely typed Composed object, not a plain f-string


def seed_postgres(conn: psycopg.Connection, row_count: int) -> None:  # => co-33: the SAME wide, 6-column shape ex-86's DuckDB table used
    """Seed row_count rows into a plain Postgres table -- a row-oriented store, no TimescaleDB hypertable involved."""  # => documents the contract
    conn.execute("DROP TABLE IF EXISTS amounts_pg")  # => resets state -- this example is fully self-contained
    conn.execute(  # => co-33: a PLAIN row-store table -- 6 columns, matching ex-86's DuckDB shape exactly
        "CREATE TABLE amounts_pg (id INT, category TEXT, amount DOUBLE PRECISION, noise1 TEXT, noise2 TEXT, noise3 TEXT)"  # => 3 real columns plus 3 UNUSED noise columns, matching ex-86's own shape
    )  # => closes the execute() call -- amounts_pg now exists as a plain, non-hypertable row store
    for i in range(row_count):  # => co-33: the IDENTICAL data ex-86 loaded into DuckDB, now in Postgres's own row-oriented heap
        category = "electronics" if i % 2 == 0 else "books"  # => the same 2-category split
        conn.execute(  # => co-33: each row lands as ONE physical row in Postgres's heap -- all 6 columns stored together
            "INSERT INTO amounts_pg VALUES (%s, %s, %s, %s, %s, %s)",  # => positional placeholders bind all 6 columns of this loop iteration's own row
            (i, category, i * 1.5, "x" * 20, "y" * 20, "z" * 20),  # => this loop iteration's own row, including the 3 noise columns
        )  # => closes this one execute() call -- runs once per row
    conn.commit()  # => makes all inserts durable before the buffer-read comparison below


def buffers_read(conn: psycopg.Connection, query: LiteralString) -> int:  # => co-33: the REAL shared-buffer block count Postgres reported reading
    """Run EXPLAIN (ANALYZE, BUFFERS) and return the total 'shared hit' block count from the plan text."""  # => documents the contract
    composed_query = sql.SQL("EXPLAIN (ANALYZE, BUFFERS) {}").format(sql.SQL(query))  # => co-33: a Composed object, not a plain f-string -- resolves psycopg's own typed overload
    plan_lines = conn.execute(composed_query).fetchall()  # => co-33: BUFFERS reports the ACTUAL blocks touched, not an estimate
    for (line,) in plan_lines:  # => scans every plan line for the "Buffers:" summary Postgres appends
        if "Buffers:" in line and "shared hit=" in line:  # => co-33: the line reporting how many shared buffer blocks this query actually touched
            return int(line.split("shared hit=")[1].split()[0].rstrip(","))  # => co-33: parses the block count out of "Buffers: shared hit=N"
    return 0  # => co-33: no buffer usage reported -- should not happen for a non-trivial table scan


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    row_count = 1000  # => co-33: the SAME row count ex-86 used, for a directly comparable aggregation

    pg_conn = psycopg.connect("host=localhost port=5433 dbname=nosqldb user=postgres password=nosqldb")  # => connects to the local Postgres/TimescaleDB Docker container -- used here as a PLAIN row store
    seed_postgres(pg_conn, row_count)  # => co-33: seeds the identical 6-column, 1000-row dataset ex-86 used

    duck_conn = duckdb.connect()  # => co-33: an IN-PROCESS DuckDB connection, columnar
    duck_conn.execute("CREATE TABLE amounts_duck (id INT, category TEXT, amount DOUBLE, noise1 TEXT, noise2 TEXT, noise3 TEXT)")  # => the SAME 6-column shape, in DuckDB
    for i in range(row_count):  # => co-33: the IDENTICAL data, loaded independently into DuckDB's own columnar storage
        category = "electronics" if i % 2 == 0 else "books"  # => the same 2-category split
        duck_conn.execute("INSERT INTO amounts_duck VALUES (?, ?, ?, ?, ?, ?)", [i, category, i * 1.5, "x" * 20, "y" * 20, "z" * 20])  # => the IDENTICAL row this loop just inserted into Postgres

    pg_result = dict(pg_conn.execute("SELECT category, sum(amount) FROM amounts_pg GROUP BY category ORDER BY category").fetchall())  # => Postgres's own aggregate
    duck_result = dict(duck_conn.execute("SELECT category, sum(amount) FROM amounts_duck GROUP BY category ORDER BY category").fetchall())  # => DuckDB's own aggregate
    assert pg_result == duck_result  # => co-33: BOTH engines return the IDENTICAL aggregate for the identical data
    print(f"Postgres (row store)   aggregate: {pg_result}")  # => Output: Postgres (row store)   aggregate: {'books': 375000.0, 'electronics': 374250.0}
    print(f"DuckDB (columnar store) aggregate: {duck_result}")  # => Output: DuckDB (columnar store) aggregate: {'books': 375000.0, 'electronics': 374250.0}

    narrow_buffers = buffers_read(pg_conn, "SELECT category, sum(amount) FROM amounts_pg GROUP BY category")  # => co-33: reading ONLY 2 of 6 columns
    wide_buffers = buffers_read(pg_conn, "SELECT * FROM amounts_pg")  # => co-33: reading ALL 6 columns
    print(f"Postgres buffers read, selecting 2 columns:  {narrow_buffers}")  # => Output line -- exact block count machine-dependent, but the EQUALITY below is the point
    print(f"Postgres buffers read, selecting all 6 columns: {wide_buffers}")  # => Output line
    assert narrow_buffers == wide_buffers  # => co-33: Postgres's heap scan reads the SAME blocks either way -- row storage cost is COLUMN-COUNT-INVARIANT
    print("Postgres reads the SAME number of buffer blocks whether 2 or all 6 columns are selected -- a row-oriented heap page holds whole rows, so narrowing the SELECT list does not reduce I/O")  # => Output line
    # => co-33: DuckDB's own EXPLAIN plan (verified directly in Example 86) shows it projects ONLY the
    # => referenced columns (category, amount) out of the table's 6 -- a columnar layout stores each
    # => column separately on disk, so a query naming fewer columns genuinely reads less data; a
    # => row-store's heap page holds an entire row together, so ANY column reference forces reading the
    # => WHOLE row regardless of how few columns the query actually names

    pg_conn.close()  # => always release what you open
    duck_conn.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
