"""Capstone step 3: serve.py -- gold aggregates from the star schema (exercises co-04, co-10)."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => co-04: this step's own standalone demo re-ingests + re-transforms to have a star schema to serve from
from pathlib import Path  # => co-04: builds the standalone demo's temp source-drop path

import duckdb  # => co-04: gold is one more in-warehouse SQL step downstream of the star schema

from ingest import SOURCE_DROP_1, SOURCE_DROP_2, _write_csv, ingest_to_bronze  # => co-04: reuse step 1's own ingest
from transform import transform_to_silver, transform_to_star_schema  # => co-04: reuse step 2's own transform -- this capstone's files import from one another

GOLD_REGION_TOTALS_SQL = (  # => co-04: GOLD -- Databricks docs: "consumption-ready, de-normalized, read-optimized"
    "CREATE OR REPLACE TABLE gold_region_totals AS "  # => co-04: opens the gold-serving statement
    "SELECT region, SUM(amount) AS total_revenue, COUNT(*) AS line_count "  # => co-10: revenue is additive -- sums correctly across the region dimension
    "FROM fact_order_line GROUP BY region"  # => co-04: one served row PER region -- exactly the shape a dashboard would query
)  # => co-04: closes GOLD_REGION_TOTALS_SQL -- this capstone's canonical "serve.sql" query, kept as a Python constant


def serve_gold(con: duckdb.DuckDBPyConnection) -> None:  # => co-04: builds the gold_region_totals table from the star schema
    """Build gold_region_totals -- one served, aggregate row per region -- from fact_order_line."""  # => co-04: documents serve_gold's contract -- no runtime output, just sets its __doc__
    con.sql(GOLD_REGION_TOTALS_SQL)  # => co-04: run the gold-serving aggregate


if __name__ == "__main__":  # => co-04: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-04: a fresh warehouse stand-in
    with tempfile.TemporaryDirectory() as tmp_dir:  # => co-04: a throwaway directory standing in for a source drop location
        drop_1_path = _write_csv(SOURCE_DROP_1, Path(tmp_dir), "drop_1.csv")  # => co-04: reuse step 1's own fixture data, drop 1
        drop_2_path = _write_csv(SOURCE_DROP_2, Path(tmp_dir), "drop_2.csv")  # => co-04: reuse step 1's own fixture data, drop 2
        ingest_to_bronze(con, drop_1_path)  # => co-04: run step 1's OWN function -- ingest drop 1
        ingest_to_bronze(con, drop_2_path)  # => co-04: run step 1's OWN function -- ingest drop 2 too, for a fuller demo

    transform_to_silver(con)  # => co-04: run step 2's OWN function -- bronze -> silver
    transform_to_star_schema(con)  # => co-04: run step 2's OWN function -- silver -> star schema
    serve_gold(con)  # => co-04: STEP 3 -- star schema -> gold

    gold = con.sql("SELECT * FROM gold_region_totals ORDER BY region").df()  # => co-04: read back the served aggregate
    print(gold)  # => co-04: prints the gold table -- region, total_revenue, line_count

    hand_computed_east = (3 * 10.00) + (1 * 25.00)  # => co-10: east total, computed BY HAND -- Alice's widget line + gadget line
    hand_computed_west = 2 * 10.00  # => co-10: west total, computed BY HAND -- Bob's widget line
    hand_computed_north = 5 * 8.00  # => co-10: north total, computed BY HAND -- Carol's gizmo line
    served_east = gold.loc[gold["region"] == "east", "total_revenue"].iloc[0]  # => co-10: what gold actually served for east
    served_west = gold.loc[gold["region"] == "west", "total_revenue"].iloc[0]  # => co-10: what gold actually served for west
    served_north = gold.loc[gold["region"] == "north", "total_revenue"].iloc[0]  # => co-10: what gold actually served for north
    print(f"East: hand {hand_computed_east} vs served {served_east} | West: hand {hand_computed_west} vs served {served_west}")  # => co-10
    print(f"North: hand {hand_computed_north} vs served {served_north}")  # => co-10: prints the third region's comparison

    all_match = (  # => co-10: the capstone's own acceptance criterion -- a serving query matches a hand-computed expected total
        served_east == hand_computed_east and served_west == hand_computed_west and served_north == hand_computed_north  # => co-10: all three regions must agree with their hand-computed totals
    )  # => co-10: every region's served total must equal its hand-computed value
    assert all_match, "gold's served totals must match every region's hand-computed value"  # => co-10: the claim
    print(f"MATCH: all {len(gold)} regions' served totals equal their hand-computed sums")  # => co-10
    # => co-04,co-10: gold is where a dashboard reads FROM -- never bronze or silver directly, and its totals are provably correct
