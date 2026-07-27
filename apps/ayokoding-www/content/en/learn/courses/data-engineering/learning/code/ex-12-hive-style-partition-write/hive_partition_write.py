"""Worked Example 12: Hive-Style Partition Write."""  # => co-07: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => co-07: writes real Parquet files under a throwaway directory tree
from pathlib import Path  # => co-07: walks the written directory tree to inspect its layout

import duckdb  # => co-07: DuckDB's COPY ... PARTITION_BY writes genuine hive-style directories

SALES_ROWS = [(1, "east", 100.0), (2, "east", 150.0), (3, "west", 80.0), (4, "north", 60.0)]  # => co-07: four rows across three regions

if __name__ == "__main__":  # => co-07: entry point -- runs only when this file executes directly, not on import
    with tempfile.TemporaryDirectory() as tmp_dir:  # => co-07: a throwaway root -- this course never writes outside a temp dir
        con = duckdb.connect()  # => co-07: a fresh warehouse stand-in
        con.sql("CREATE TABLE sales (sale_id INTEGER, region VARCHAR, amount DOUBLE)")  # => co-07: the table to be partition-written
        con.executemany("INSERT INTO sales VALUES (?, ?, ?)", SALES_ROWS)  # => co-07: land all four rows

        output_dir = Path(tmp_dir) / "sales_partitioned"  # => co-07: the partitioned dataset's root directory
        con.sql(f"COPY sales TO '{output_dir}' (FORMAT PARQUET, PARTITION_BY (region))")  # => co-07: Hive-style layout: region=value/data_0.parquet

        written_paths = sorted(p.relative_to(output_dir).as_posix() for p in output_dir.rglob("*.parquet"))  # => co-07: every Parquet file actually written
        print("Partition files written:")  # => co-07: frames the file listing
        for path in written_paths:  # => co-07: one line per written file
            print(f"  {path}")  # => co-07: prints each relative path -- region=<value>/data_0.parquet

        directory_names = sorted(p.name for p in output_dir.iterdir() if p.is_dir())  # => co-07: the partition directories themselves
        print(f"Partition directories: {directory_names}")  # => co-07: prints the directory names
        expected_directories = ["region=east", "region=north", "region=west"]  # => co-07: exactly key=value, one per distinct region value
        assert directory_names == expected_directories, "the directory layout must encode key=value for each region"  # => co-07
        print(f"MATCH: {len(written_paths)} Parquet files written under {len(directory_names)} key=value partition directories")  # => co-07
        # => co-07: a directory path can itself communicate a column's value -- a query can use that to skip files it can't match
