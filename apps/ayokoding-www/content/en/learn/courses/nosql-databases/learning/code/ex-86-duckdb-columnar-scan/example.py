"""Example 86: DuckDB Columnar Scan."""  # => co-32,co-33: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import csv  # => co-32: writes the source CSV this example loads -- a realistic OLAP ingestion path
import tempfile  # => generates a throwaway CSV path -- this example is fully self-contained
from pathlib import Path  # => co-32: typed filesystem path handling for the generated CSV file

import duckdb  # => co-33: duckdb, the official Python API for the in-process, MIT-licensed columnar OLAP engine


def write_sample_csv(row_count: int) -> Path:  # => co-32: many rows, several UNUSED columns -- sets up the projection check below
    """Write row_count rows with 6 columns, only 2 of which the query below will ever reference."""  # => documents the contract
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:  # => co-32: mktemp() is deprecated -- this creates the file (and closes it) immediately instead
        path = Path(tmp.name)  # => a throwaway CSV path, unique per run
    with path.open("w", newline="") as f:  # => opens the file for writing
        writer = csv.writer(f)  # => a plain stdlib CSV writer -- no DuckDB-specific write path needed to CREATE the source data
        writer.writerow(["id", "category", "amount", "noise1", "noise2", "noise3"])  # => co-33: 3 UNUSED "noise" columns, deliberately
        for i in range(row_count):  # => co-32: row_count rows, many for a wide-scan aggregation to be meaningful
            category = "electronics" if i % 2 == 0 else "books"  # => co-32: 2 categories, evenly split
            writer.writerow([i, category, i * 1.5, "x" * 20, "y" * 20, "z" * 20])  # => co-33: the 3 noise columns are never referenced by the query below
    return path  # => hand back the path for DuckDB to load


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    row_count = 1000  # => co-32: many rows of one column -- large enough for a genuine "many rows" aggregation
    csv_path = write_sample_csv(row_count)  # => co-32: writes the source CSV this in-process query loads

    conn = duckdb.connect()  # => co-33: an IN-PROCESS DuckDB connection -- no server, no separate process to manage
    conn.execute(f"CREATE TABLE amounts AS SELECT * FROM read_csv_auto('{csv_path}')")  # => co-33: loads the CSV directly into a DuckDB table
    csv_path.unlink()  # => cleans up the throwaway CSV -- the data now lives inside DuckDB's own table

    plan_text = conn.execute(  # => co-33: EXPLAIN's own text plan reveals EXACTLY which columns the scan node reads
        "EXPLAIN SELECT category, sum(amount) AS total FROM amounts GROUP BY category"  # => the SAME aggregation query, prefixed with EXPLAIN instead of run
    ).fetchall()[0][1]  # => the plan text lives in the second column of EXPLAIN's single result row
    assert "Projections:" in plan_text  # => co-33: confirms the scan node genuinely reports which columns it projects
    assert "noise1" not in plan_text and "noise2" not in plan_text and "noise3" not in plan_text  # => co-33: the 3 UNUSED columns are absent from the scan's own projection list
    assert "category" in plan_text and "amount" in plan_text  # => co-33: only the 2 REFERENCED columns appear in the scan's projection

    rows = conn.execute(  # => co-32: the actual typed-Python aggregation query
        "SELECT category, sum(amount) AS total FROM amounts GROUP BY category ORDER BY category"  # => the SAME query EXPLAIN just analyzed, now actually run
    ).fetchall()  # => materializes one row per distinct category
    totals_by_category = dict(rows)  # => category -> summed amount, as returned by DuckDB

    expected_electronics = sum(i * 1.5 for i in range(0, row_count, 2))  # => co-32: the INDEPENDENT, hand-computed expectation for electronics (even i)
    expected_books = sum(i * 1.5 for i in range(1, row_count, 2))  # => co-32: the INDEPENDENT, hand-computed expectation for books (odd i)
    assert totals_by_category["electronics"] == expected_electronics  # => co-32: DuckDB's SUM matches the hand-computed total exactly
    assert totals_by_category["books"] == expected_books  # => co-32: DuckDB's SUM matches the hand-computed total exactly

    print(f"electronics total: {totals_by_category['electronics']}")  # => Output: electronics total: 374250.0
    print(f"books total:       {totals_by_category['books']}")  # => Output: books total:       375000.0
    print("The scan node's own EXPLAIN output confirms it projects ONLY category and amount -- noise1/noise2/noise3 never touched")  # => Output line
    conn.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
