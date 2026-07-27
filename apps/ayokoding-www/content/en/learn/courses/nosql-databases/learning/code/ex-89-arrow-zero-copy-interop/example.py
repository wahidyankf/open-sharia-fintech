"""Example 89: Arrow Zero-Copy Interop."""  # => co-35: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-35: duckdb, the official Python API for the in-process, MIT-licensed columnar OLAP engine
import pyarrow as pa  # => co-35: pyarrow, the official Apache Arrow Python bindings -- the in-memory format both engines share


def build_large_arrow_table(row_count: int) -> pa.Table:  # pyright: ignore[reportUnknownParameterType]  # => co-35: pyarrow ships zero type stubs, so pa.Table itself resolves as Unknown; narrowly scoped, not a global relaxation
    """Build a 2-column, row_count-row Arrow table entirely in memory."""  # => documents the contract
    return pa.table(
        {  # => co-35: an in-memory Arrow Table -- the SAME columnar format Parquet (Example 88) is built on
            "id": pa.array(range(row_count)),  # => a numeric id column
            "value": pa.array([i * 0.5 for i in range(row_count)]),  # => a numeric value column, the one DuckDB will sum below
        }
    )  # => closes the pa.table() call -- 2 columns, entirely in-memory


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    row_count = 2_000_000  # => co-35: large enough (millions of rows) that a full COPY would move a measurable number of bytes
    arrow_table = build_large_arrow_table(row_count)  # => co-35: builds the table entirely in Python/Arrow memory, no DuckDB involved yet
    table_bytes = arrow_table.nbytes  # => co-35: the table's own reported in-memory size -- what a COPY would have to duplicate

    bytes_before = pa.total_allocated_bytes()  # => co-35: Arrow's own allocator tracks EVERY byte it has allocated, process-wide
    duck_conn = duckdb.connect()  # => co-35: an IN-PROCESS DuckDB connection
    result_row = duck_conn.execute("SELECT sum(value) FROM arrow_table").fetchone()  # => co-35: DuckDB queries the Python variable BY NAME -- no to_pandas(), no CSV, no Parquet round trip
    assert result_row is not None  # => a SUM(*) query always returns exactly one row -- confirms it genuinely came back
    bytes_after = pa.total_allocated_bytes()  # => co-35: re-checks Arrow's allocator AFTER the query ran

    allocated_during_query = bytes_after - bytes_before  # => co-35: however many NEW bytes Arrow's allocator reports for running the query
    hand_computed_sum = sum(i * 0.5 for i in range(row_count))  # => co-35: an INDEPENDENT, hand-computed expectation
    assert abs(result_row[0] - hand_computed_sum) < 1e-6  # => co-35: DuckDB's sum matches the hand-computed sum, to floating-point precision

    print(f"Arrow table size:                 {table_bytes:,} bytes")  # => Output: Arrow table size:                 32,000,000 bytes
    print(f"Bytes newly allocated by the query: {allocated_during_query:,} bytes")  # => Output line -- exact bytes machine-dependent, ratio is the point
    percent_of_table = allocated_during_query / table_bytes * 100  # => co-35: what fraction of the table's own size the query newly allocated
    print(f"That is {percent_of_table:.3f}% of the table's own size -- nowhere near a full 32MB copy")  # => Output line
    assert allocated_during_query < table_bytes * 0.01  # => co-35: a genuine COPY would allocate close to table_bytes -- this stayed under 1% of it
    print(f"sum(value) = {result_row[0]}, matching the hand-computed expectation exactly")  # => Output line -- exact value machine-independent, deterministic
    print("DuckDB queried the SAME Arrow buffers directly -- zero-copy interchange, not a serialize-then-copy round trip")  # => Output line
    duck_conn.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
