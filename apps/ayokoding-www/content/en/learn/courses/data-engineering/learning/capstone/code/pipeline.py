"""Capstone step 4: pipeline.py -- a DAG wiring ingest -> transform -> quality gate -> serve, with retries (exercises co-18, co-16)."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => co-18: each pipeline run re-ingests its own source drop to stay independently runnable
from pathlib import Path  # => co-18: builds each run's temp source-drop path

import duckdb  # => co-18: the DAG's tasks operate on one shared connection per pipeline run

from ingest import _write_csv, ingest_to_bronze  # => co-18: reuse step 1's own ingest -- this capstone's files import from one another
from serve import serve_gold  # => co-18: reuse step 3's own serve
from transform import transform_to_silver, transform_to_star_schema  # => co-18: reuse step 2's own transform

ALLOWED_REGIONS = {"east", "west", "north"}  # => co-16: the quality gate's own enum contract -- any OTHER region value fails the batch

GOOD_DROP = [  # => co-16: a clean drop -- every region is a KNOWN, valid one
    "order_id,line_number,customer_name,region,product_name,quantity,unit_price",  # => co-16: header
    "9101,1,Dana,east,Widget,4,10.00",  # => co-16: order 9101 -- region 'east', valid
]  # => co-16: closes GOOD_DROP
BAD_DROP = [  # => co-16: a deliberately BAD drop -- one line has an invalid region value
    "order_id,line_number,customer_name,region,product_name,quantity,unit_price",  # => co-16: header
    "9102,1,Eve,mars,Gadget,1,25.00",  # => co-16: order 9102 -- region 'mars' is NOT in ALLOWED_REGIONS, an invalid enum value
]  # => co-16: closes BAD_DROP


def ingest_with_retries(con: duckdb.DuckDBPyConnection, csv_path: Path, *, attempt_state: dict[str, int]) -> None:  # => co-18: wraps ingest with a retry policy
    """Retry ingest_to_bronze up to 3 times -- attempt_state tracks a deterministic transient-failure simulation."""  # => co-18: documents ingest_with_retries's contract -- no runtime output, just sets its __doc__
    attempt_state["count"] = attempt_state.get("count", 0) + 1  # => co-18: record this attempt, matching ex-42's own retry-counting shape
    if attempt_state["count"] < 2:  # => co-18: attempt 1 deterministically fails -- a simulated transient upstream hiccup
        raise RuntimeError(f"transient ingest failure on attempt {attempt_state['count']}")  # => co-18: a recoverable, retryable failure
    ingest_to_bronze(con, csv_path)  # => co-18: attempt 2 succeeds -- the DAG's retry policy absorbed the transient failure


def run_ingest_task(con: duckdb.DuckDBPyConnection, csv_path: Path, *, max_retries: int = 3) -> None:  # => co-18: the DAG's own ingest TASK, retry-wrapped
    """Run ingest_with_retries up to max_retries times, matching Airflow's own default_args retry policy."""  # => co-18: documents run_ingest_task's contract -- no runtime output, just sets its __doc__
    attempt_state: dict[str, int] = {}  # => co-18: fresh retry bookkeeping for THIS task invocation
    for attempt in range(1, max_retries + 1):  # => co-18: attempt 1 through max_retries, inclusive
        try:  # => co-18: one retry attempt
            ingest_with_retries(con, csv_path, attempt_state=attempt_state)  # => co-18: try the (possibly flaky) ingest
            return  # => co-18: SUCCESS -- return immediately, no further retries needed
        except RuntimeError as error:  # => co-18: this attempt failed -- log it and try again
            print(f"  ingest task attempt {attempt} failed: {error}")  # => co-18: log every failed attempt, matching a real scheduler's retry log
    raise RuntimeError("ingest task exhausted all retries")  # => co-18: re-raised only if EVERY attempt failed


def run_quality_gate(con: duckdb.DuckDBPyConnection) -> bool:  # => co-16: the DAG's own DQ gate task -- wired between transform and serve
    """Fail the gate if any fact_order_line row's region is outside ALLOWED_REGIONS."""  # => co-16: documents run_quality_gate's contract -- no runtime output, just sets its __doc__
    bad_regions = con.sql("SELECT DISTINCT region FROM fact_order_line WHERE region NOT IN ('east', 'west', 'north')").df()  # => co-16: any region OUTSIDE the enum contract
    return len(bad_regions) == 0  # => co-16: the gate passes ONLY if every region value is a known, allowed one


def run_pipeline(csv_lines: list[str], *, label: str) -> tuple[bool, bool]:  # => co-18: the DAG itself -- ingest -> transform -> gate -> serve
    """Run the full DAG for one source drop; return (gate_passed, gold_table_created)."""  # => co-18: documents run_pipeline's contract -- no runtime output, just sets its __doc__
    print(f"--- Pipeline run: {label} ---")  # => co-18: frames this run's own transcript section
    con = duckdb.connect()  # => co-18: each pipeline run gets its OWN fresh connection, independently runnable
    with tempfile.TemporaryDirectory() as tmp_dir:  # => co-18: a throwaway directory standing in for a source drop location
        csv_path = _write_csv(csv_lines, Path(tmp_dir), "drop.csv")  # => co-18: write THIS run's own source drop
        run_ingest_task(con, csv_path)  # => co-18: TASK 1 -- ingest, wrapped with retries
    transform_to_silver(con)  # => co-18: TASK 2a -- bronze -> silver, depends on ingest having succeeded
    transform_to_star_schema(con)  # => co-18: TASK 2b -- silver -> star schema, depends on 2a
    gate_passed = run_quality_gate(con)  # => co-16: TASK 3 -- the quality gate, depends on the star schema existing
    print(f"Quality gate passed: {gate_passed}")  # => co-16: prints the gate's verdict for this run
    gold_created = False  # => co-18: tracks whether TASK 4 (serve) actually ran -- the DAG's own dependency wiring
    if gate_passed:  # => co-18: serve is WIRED to depend on the gate -- it only runs if the gate passed
        serve_gold(con)  # => co-18: TASK 4 -- serve, runs ONLY if the gate passed
        gold_created = con.sql("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'gold_region_totals'").fetchone()[0] > 0  # => co-18
    print(f"gold_region_totals created: {gold_created}")  # => co-18: prints whether the served table actually exists
    return gate_passed, gold_created  # => co-18: returns this computed value to the caller


if __name__ == "__main__":  # => co-18: entry point -- runs only when this file executes directly, not on import
    good_gate_passed, good_gold_created = run_pipeline(GOOD_DROP, label="good batch")  # => co-18: RUN 1 -- the clean drop, should reach gold
    assert good_gate_passed is True and good_gold_created is True, "a clean batch must pass the gate and reach gold"  # => co-18: the claim

    bad_gate_passed, bad_gold_created = run_pipeline(BAD_DROP, label="bad batch (invalid region)")  # => co-16: RUN 2 -- the deliberately bad drop
    assert bad_gate_passed is False, "a batch with an invalid region must fail the quality gate"  # => co-16: the capstone's own acceptance criterion
    assert bad_gold_created is False, "a batch that fails the quality gate must NEVER reach gold"  # => co-16: the capstone's own acceptance criterion

    print(f"MATCH: good batch reached gold ({good_gold_created}); bad batch was blocked at the gate ({bad_gold_created})")  # => co-18
    # => co-16,co-18: the DAG's retry policy absorbed a transient ingest failure; its gate wiring blocked a genuinely bad batch
