"""Example 88: Parquet Roundtrip Projection."""  # => co-35: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => generates a throwaway Parquet file path -- this example is fully self-contained
from pathlib import Path  # => co-35: typed filesystem path handling for the generated Parquet file

import pyarrow as pa  # => co-35: pyarrow, the official Apache Arrow Python bindings -- Arrow and Parquet are BOTH Apache-2.0
import pyarrow.parquet as pq  # => co-35: pyarrow.parquet -- the Parquet reader/writer built on Arrow's own in-memory format


def build_sample_table(row_count: int) -> pa.Table:  # pyright: ignore[reportUnknownParameterType]  # => co-35: pyarrow ships zero type stubs, so pa.Table itself resolves as Unknown; narrowly scoped, not a global relaxation
    """Build an in-memory Arrow table: id, category, amount, and one large raw_payload text column."""  # => documents the contract
    return pa.table(
        {  # => co-35: an Arrow Table -- the in-memory format Parquet itself is built on
            "id": pa.array(range(row_count)),  # => a small numeric column
            "category": pa.array(["electronics" if i % 2 == 0 else "books" for i in range(row_count)]),  # => a small, repetitive text column
            "amount": pa.array([i * 1.5 for i in range(row_count)]),  # => a small numeric column
            "raw_payload": pa.array([f"payload-{i}-" + ("z" * 200) for i in range(row_count)]),  # => co-35: a deliberately LARGE text column, never referenced by the projected read below
        }
    )  # => closes the pa.table() call -- 4 columns, one deliberately large


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    row_count = 1000  # => co-35: enough rows that the per-column compressed sizes below are meaningful, not noise
    table = build_sample_table(row_count)  # => co-35: builds the in-memory Arrow table this example writes to Parquet

    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tmp:  # => co-35: mktemp() is deprecated -- this creates the file (and closes it) immediately instead
        path = Path(tmp.name)  # => a throwaway Parquet file path, unique per run
    pq.write_table(table, path)  # => co-35: writes the Arrow table to an on-disk, columnar Parquet file

    parquet_file = pq.ParquetFile(path)  # => co-35: opens the file's own footer metadata WITHOUT reading any column data yet
    row_group = parquet_file.metadata.row_group(0)  # => co-35: this small file has exactly 1 row group
    column_sizes = {  # => co-35: EVERY column's compressed byte size, stored independently in the file's own footer
        row_group.column(i).path_in_schema: row_group.column(i).total_compressed_size
        for i in range(row_group.num_columns)  # => maps each column's own name to its own compressed byte size
    }  # => closes the column_sizes dict comprehension -- one entry per column in the row group
    total_bytes = sum(column_sizes.values())  # => co-35: the FULL file's total compressed column-chunk bytes

    projected_table = pq.read_table(path, columns=["category", "amount"])  # => co-35: reads back ONLY 2 of the file's 4 columns
    assert projected_table.column_names == ["category", "amount"]  # => co-35: the returned table genuinely contains ONLY the 2 requested columns
    assert projected_table.num_rows == row_count  # => confirms every row was still read for those 2 columns

    projected_bytes = column_sizes["category"] + column_sizes["amount"]  # => co-35: the compressed size of ONLY the 2 projected columns' own chunks
    print(f"Full file, all 4 columns:      {total_bytes} compressed bytes")  # => Output line -- exact bytes machine-dependent, ratio is the point
    print(f"Projected read, 2 columns:     {projected_bytes} compressed bytes")  # => Output line
    percent_of_total = projected_bytes / total_bytes * 100  # => co-35: what fraction of the whole file the projected read actually touched
    print(f"Projected read touched {percent_of_total:.1f}% of the file's total compressed bytes")  # => Output line -- percentage machine-dependent, always well under 100%
    assert projected_bytes < total_bytes  # => co-35: the projected read touched STRICTLY LESS data than the whole file
    print(f"raw_payload column alone: {column_sizes['raw_payload']} compressed bytes -- NEVER read by the projected query above")  # => Output line
    print("Parquet's column-chunk layout lets a projected read skip entire columns' worth of on-disk bytes, not just filter rows after a full read")  # => Output line
    path.unlink()  # => cleans up the throwaway Parquet file


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
