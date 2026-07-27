"""Worked Example 13: Partition-Pruning Read."""  # => co-07: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => co-07: writes real Parquet files under a throwaway directory tree, then reads them back with a filter
from pathlib import Path  # => co-07: builds the partitioned dataset's glob pattern

import duckdb  # => co-07: DuckDB's read_parquet(hive_partitioning=true) prunes files using the directory path alone

SALES_ROWS = [(1, "east", 100.0), (2, "east", 150.0), (3, "west", 80.0), (4, "north", 60.0)]  # => co-07: the SAME four rows ex-12 partitioned

if __name__ == "__main__":  # => co-07: entry point -- runs only when this file executes directly, not on import
    with tempfile.TemporaryDirectory() as tmp_dir:  # => co-07: a throwaway root -- this course never writes outside a temp dir
        con = duckdb.connect()  # => co-07: a fresh warehouse stand-in
        con.sql("CREATE TABLE sales (sale_id INTEGER, region VARCHAR, amount DOUBLE)")  # => co-07: the table to be partition-written
        con.executemany("INSERT INTO sales VALUES (?, ?, ?)", SALES_ROWS)  # => co-07: land all four rows

        output_dir = Path(tmp_dir) / "sales_partitioned"  # => co-07: the partitioned dataset's root directory
        con.sql(f"COPY sales TO '{output_dir}' (FORMAT PARQUET, PARTITION_BY (region))")  # => co-07: writes 3 files, one per region

        glob_pattern = str(output_dir / "*" / "*.parquet")  # => co-07: matches all THREE partition files
        plan_text = con.sql(  # => co-07: EXPLAIN, not EXPLAIN ANALYZE -- shows the planned file pruning without running it
            f"EXPLAIN SELECT * FROM read_parquet('{glob_pattern}', hive_partitioning=true) WHERE region = 'east'"  # => co-07: filters on region -- the same column encoded in the partition directory path
        ).fetchone()[1]  # => co-07: the plan's text -- DuckDB prints "Scanning Files: N/M" when a filter prunes candidates
        pruning_line = [line for line in plan_text.splitlines() if "Scanning Files" in line][0].strip()  # => co-07: isolate the one relevant plan line
        print(f"Query plan pruning line: {pruning_line!r}")  # => co-07: prints exactly what the planner decided

        result = con.sql(f"SELECT * FROM read_parquet('{glob_pattern}', hive_partitioning=true) WHERE region = 'east'").df()  # => co-07: run it for real
        print(result)  # => co-07: prints the actual rows -- only east's two rows, region column reconstructed from the path
        assert "Scanning Files: 1/3" in pruning_line, "the planner must show only 1 of 3 partition files scanned for region='east'"  # => co-07
        assert set(result["region"]) == {"east"}, "the query must return only east rows, having pruned west and north entirely"  # => co-07
        print("MATCH: the planner scans 1 of 3 partition files, matching the directory-encoded region filter")  # => co-07
        # => co-07: partition pruning turns a filter on the PATH into work the query never has to do on the OTHER files' bytes
