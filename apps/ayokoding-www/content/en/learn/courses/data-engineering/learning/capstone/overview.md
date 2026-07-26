---
title: "Overview"
date: 2026-07-27T00:00:00+07:00
draft: false
weight: 1
---

## The capstone: Aurora Retail's local pipeline

The capstone builds a complete local data pipeline for "Aurora Retail," a small invented retailer
selling Widgets, Gadgets, and Gizmos across three regions (east, west, north): idempotent bronze
ingest of raw order-line files, a silver clean/conform step, a star schema (facts + dimensions),
gold-served region totals, all wrapped in a small orchestrated DAG with retries and a data-quality
gate that blocks a deliberately bad batch. Every script lives under `learning/capstone/code/`,
actually run against **Python 3.13**, `duckdb==1.5.5`, and `pandas==3.0.5` to capture the output
shown below. Unlike every other worked example in this topic, the capstone's four files import from
one another as one small project -- this topic's one deliberate exception to the
"no cross-example imports" rule.

- **Step 1 -- `ingest.py`**: raw order-line CSV drops land into an idempotent `bronze_order_lines`
  table via an anti-join on `(order_id, line_number)`. Ties together co-04, co-05, co-06.
- **Step 2 -- `transform.py`**: bronze cleans and conforms into silver, then silver splits into a
  star schema (`dim_customer`, `dim_product`, `fact_order_line`). Ties together co-04, co-08, co-09.
- **Step 3 -- `serve.py`** / **`serve.sql`**: the star schema aggregates into
  `gold_region_totals`, one served row per region. Ties together co-04, co-10.
- **Step 4 -- `pipeline.py`**: a DAG wires all three steps with a retry policy on ingest and a
  data-quality gate between the star schema and serve. Ties together co-16, co-18.

**Concepts exercised**: [x] idempotent + incremental ingest (bronze) (co-04, co-05, co-06)
[x] cleaning/conforming (silver) (co-04) [x] a star schema (facts + dimensions) (co-08, co-09)
[x] gold serving aggregates (co-04, co-10) [x] data-quality checks that fail a bad batch (co-16)
[x] a small orchestrated DAG with retries + gate (co-18).

---

## Step 1: ingest.py -- raw order-line files to an idempotent bronze layer

**Context**: Beginner examples ex-05 (bronze-land-raw) and ex-08 (idempotent-rerun) taught landing
raw data as-is and checking a natural key before inserting. This step combines both into Aurora
Retail's own bronze ingest: two source drops, land via an anti-join on `(order_id, line_number)` so
a rerun of the same drop adds zero duplicate rows, and a later drop's genuinely new rows still land.

```python
# learning/capstone/code/ingest.py
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
```

**Run**: `python3 ingest.py`

**Output**:

```text
Run 1 (drop 1): 3 new rows added
Run 2 (drop 1 rerun): 0 new rows added
Run 3 (drop 2, new data): 1 new rows added
Total bronze rows: 4
MATCH: 3 + 0 + 1 = 4 bronze rows, idempotent across reruns
```

**Acceptance criteria**: a re-run of the identical drop 1 must add zero duplicate rows (co-05) --
confirmed, run 2 adds `0` new rows. A later, genuinely new drop must still land its new rows
(co-06) -- confirmed, drop 2 adds exactly `1` new row, bringing the total to `4`. Both hold, matching
this capstone's own step-1 acceptance criterion of "a re-run adds no duplicate rows."

**Key takeaway**: an anti-join on the natural key `(order_id, line_number)` is enough to make bronze
ingest both idempotent (a rerun of the same drop is a no-op) and incremental (a later drop's
genuinely new rows still land) in one SQL statement.

**Why It Matters**: this is the exact foundation every later capstone step builds on -- if bronze
ingest weren't idempotent, every retry, every operator rerun, and every scheduler-triggered re-run
of `pipeline.py`'s DAG (Step 4) would risk corrupting the whole pipeline's totals with duplicated
order lines.

---

## Step 2: transform.py -- bronze to silver to a star schema

**Context**: Beginner examples ex-06 (silver-clean-conform) and ex-14/ex-15 (fact-vs-dimension,
star-schema-grain) taught cleaning bronze into silver and splitting a flat table into a star schema.
This step applies both to Aurora Retail's own order lines: silver validates and computes `amount`,
then splits into `dim_customer`, `dim_product`, and `fact_order_line` at a declared
one-row-per-order-line grain.

```python
# learning/capstone/code/transform.py
"""Capstone step 2: transform.py -- bronze to silver to a star schema (exercises co-04, co-08, co-09)."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import tempfile  # => co-04: this step's own standalone demo re-ingests a source drop to have bronze to transform
from pathlib import Path  # => co-04: builds the standalone demo's temp source-drop path

import duckdb  # => co-04: silver and the star schema are both built with in-warehouse SQL

from ingest import SOURCE_DROP_1, _write_csv, ingest_to_bronze  # => co-04: reuse step 1's own ingest -- this capstone's files import from one another


def transform_to_silver(con: duckdb.DuckDBPyConnection) -> None:  # => co-04: bronze -> silver -- typed, deduped, validated
    """Clean bronze_order_lines into silver_order_lines: typed, deduped, validated, with a computed amount."""  # => co-04: documents transform_to_silver's contract -- no runtime output, just sets its __doc__
    silver_sql = "CREATE OR REPLACE TABLE silver_order_lines AS SELECT DISTINCT order_id, line_number, customer_name, region, product_name, quantity, unit_price, quantity * unit_price AS amount FROM bronze_order_lines WHERE customer_name IS NOT NULL AND quantity > 0 AND unit_price > 0"  # => co-16: DQ gates inline
    con.sql(silver_sql)  # => co-04: DISTINCT dedupes; the WHERE clause drops any incomplete or invalid row before it reaches the star schema


def transform_to_star_schema(con: duckdb.DuckDBPyConnection) -> None:  # => co-08: silver -> fact + dimension tables
    """Split silver_order_lines into dim_customer, dim_product, and fact_order_line."""  # => co-08: documents transform_to_star_schema's contract -- no runtime output, just sets its __doc__
    dim_customer_sql = "CREATE OR REPLACE TABLE dim_customer AS SELECT ROW_NUMBER() OVER () AS customer_key, customer_name FROM (SELECT DISTINCT customer_name FROM silver_order_lines)"  # => co-08: DIMENSION 1 -- customer
    con.sql(dim_customer_sql)  # => co-08: the descriptive-attribute half of the split, given its own surrogate key
    dim_product_sql = "CREATE OR REPLACE TABLE dim_product AS SELECT ROW_NUMBER() OVER () AS product_key, product_name FROM (SELECT DISTINCT product_name FROM silver_order_lines)"  # => co-08: DIMENSION 2 -- product
    con.sql(dim_product_sql)  # => co-08: the SECOND dimension -- product, its own surrogate key
    sql = "CREATE OR REPLACE TABLE fact_order_line AS SELECT order_id, line_number, customer_key, product_key, region, quantity, unit_price, amount FROM silver_order_lines s JOIN dim_customer c ON s.customer_name = c.customer_name JOIN dim_product p ON s.product_name = p.product_name"  # => co-09: FACT
    con.sql(sql)  # => co-09: the fact table -- numeric measurements (quantity, unit_price, amount) with FK context


if __name__ == "__main__":  # => co-04: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-04: a fresh warehouse stand-in
    with tempfile.TemporaryDirectory() as tmp_dir:  # => co-04: a throwaway directory standing in for a source drop location
        drop_1_path = _write_csv(SOURCE_DROP_1, Path(tmp_dir), "drop_1.csv")  # => co-04: reuse step 1's own fixture data
        ingest_to_bronze(con, drop_1_path)  # => co-04: run step 1's OWN function -- sets up this step's own precondition

    transform_to_silver(con)  # => co-04: STEP 2a -- bronze -> silver
    transform_to_star_schema(con)  # => co-08: STEP 2b -- silver -> star schema

    silver_count = con.sql("SELECT COUNT(*) FROM silver_order_lines").fetchone()[0]  # => co-04: silver's own row count
    fact_count = con.sql("SELECT COUNT(*) FROM fact_order_line").fetchone()[0]  # => co-09: the fact table's row count -- must match silver's grain
    print(f"Silver rows: {silver_count} | Fact rows: {fact_count}")  # => co-04: prints both counts for a quick reconciliation check
    assert silver_count == fact_count, "the fact table must have exactly one row per silver row, matching the declared grain"  # => co-09

    unresolved_customers_sql = "SELECT COUNT(*) FROM fact_order_line f LEFT JOIN dim_customer c ON f.customer_key = c.customer_key WHERE c.customer_key IS NULL"  # => co-08: does EVERY fact row's customer_key resolve?
    unresolved_customers = con.sql(unresolved_customers_sql).fetchone()[0]  # => co-08: a left join finding ZERO means every foreign key resolves
    unresolved_products_sql = "SELECT COUNT(*) FROM fact_order_line f LEFT JOIN dim_product p ON f.product_key = p.product_key WHERE p.product_key IS NULL"  # => co-08: does EVERY fact row's product_key resolve?
    unresolved_products = con.sql(unresolved_products_sql).fetchone()[0]  # => co-08: a left join finding ZERO means every foreign key resolves
    print(f"Unresolved customer FKs: {unresolved_customers} | Unresolved product FKs: {unresolved_products}")  # => co-08
    assert unresolved_customers == 0 and unresolved_products == 0, "every fact row's foreign keys must resolve to real dimension rows"  # => co-08
    print(f"MATCH: {fact_count} fact rows reconcile with silver's {silver_count} rows, every foreign key resolves")  # => co-09
    # => co-08,co-09: the star schema's grain and referential integrity both hold -- ready for gold aggregation
```

**Run**: `python3 transform.py`

**Output**:

```text
Silver rows: 3 | Fact rows: 3
Unresolved customer FKs: 0 | Unresolved product FKs: 0
MATCH: 3 fact rows reconcile with silver's 3 rows, every foreign key resolves
```

**Acceptance criteria**: facts must join to every dimension (co-08) -- confirmed, `0` unresolved
customer and `0` unresolved product foreign keys. Row counts must reconcile (co-09) -- confirmed,
silver's `3` rows produce exactly `3` fact rows, matching the declared one-row-per-order-line grain.
Both hold, matching this capstone's own step-2 acceptance criterion.

**Key takeaway**: silver's `WHERE customer_name IS NOT NULL AND quantity > 0 AND unit_price > 0`
clause is a data-quality gate (co-16) baked directly into the transform, so only valid, complete
rows ever reach the star schema at all.

**Why It Matters**: catching invalid rows here, at transform time, is cheaper than catching them
later at the quality-gate task in Step 4's DAG -- Step 4's own gate exists as a second,
independent line of defense against a DIFFERENT class of problem (a value that's structurally valid
but not a real business-allowed value, like a region code that doesn't exist).

---

## Step 3: serve.py / serve.sql -- gold aggregates from the star schema

**Context**: Beginner example ex-07 (gold-serve-aggregate) taught aggregating silver into a served
gold table. This step applies the same idea to Aurora Retail's own star schema, aggregating
`fact_order_line` into `gold_region_totals` -- one served row per region -- and ships both a
Python (`serve.py`) and a plain-SQL (`serve.sql`) version of the identical query, so a BI tool or a
reviewer can run the query directly without going through Python.

```python
# learning/capstone/code/serve.py
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
        served_east == hand_computed_east and served_west == hand_computed_west and served_north == hand_computed_north
    )  # => co-10: every region's served total must equal its hand-computed value
    assert all_match, "gold's served totals must match every region's hand-computed value"  # => co-10: the claim
    print(f"MATCH: all {len(gold)} regions' served totals equal their hand-computed sums")  # => co-10
    # => co-04,co-10: gold is where a dashboard reads FROM -- never bronze or silver directly, and its totals are provably correct
```

The plain-SQL companion, `serve.sql`, runs the identical `GOLD_REGION_TOTALS_SQL` statement -- a
reviewer or a BI tool can run it directly against the star schema `transform.py` builds, without
going through Python at all:

<!-- prettier-ignore -->
```sql
-- learning/capstone/code/serve.sql
-- Capstone step 3 (companion to serve.py): the canonical gold-serving query.
-- serve.py runs this exact statement as GOLD_REGION_TOTALS_SQL; this file exists
-- as the plain-SQL artifact a BI tool or a reviewer could run directly against
-- the star schema built by transform.py, without going through Python at all.
CREATE OR REPLACE TABLE gold_region_totals AS
SELECT region, SUM(amount) AS total_revenue, COUNT(*) AS line_count
FROM fact_order_line
GROUP BY region;
```

**Run**: `python3 serve.py`

**Output**:

```text
  region  total_revenue  line_count
0   east           55.0           2
1  north           40.0           1
2   west           20.0           1
East: hand 55.0 vs served 55.0 | West: hand 20.0 vs served 20.0
North: hand 40.0 vs served 40.0
MATCH: all 3 regions' served totals equal their hand-computed sums
```

**Acceptance criteria**: a serving query must match a hand-computed expected total -- confirmed for
all three regions (east `55.0`, west `20.0`, north `40.0`), each independently computed by hand from
the raw order-line quantities and unit prices. Matches this capstone's own step-3 acceptance
criterion exactly.

**Key takeaway**: `revenue` is an additive measure (co-10) -- `SUM(amount) GROUP BY region` produces
a correct total regardless of how many order lines or products fed into each region, because
additive facts sum correctly across every dimension.

**Why It Matters**: shipping both a Python function and a standalone `.sql` file for the same query
is a genuinely common real-world pattern -- the Python version lets the pipeline call it
programmatically (as Step 4's DAG does), while the plain-SQL version is what a data analyst,
reviewer, or BI tool can run directly, with no Python runtime involved at all.

---

## Step 4: pipeline.py -- a DAG with retries and a quality gate

**Context**: Advanced examples ex-41 through ex-45 (DAG dependencies, retry, schedule/catchup,
quality gate, backfill) and ex-44 specifically (quality gate blocks downstream) taught the pieces
this step assembles into one real DAG. This step wires `ingest -> transform -> quality_gate ->
serve`, with a retry policy absorbing a simulated transient ingest failure, and runs the DAG twice:
once against a clean batch (region `east`, an allowed value) and once against a deliberately bad
batch (region `mars`, not in `ALLOWED_REGIONS`).

```python
# learning/capstone/code/pipeline.py
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
```

**Run**: `python3 pipeline.py`

**Output**:

```text
--- Pipeline run: good batch ---
  ingest task attempt 1 failed: transient ingest failure on attempt 1
Quality gate passed: True
gold_region_totals created: True
--- Pipeline run: bad batch (invalid region) ---
  ingest task attempt 1 failed: transient ingest failure on attempt 1
Quality gate passed: False
gold_region_totals created: False
MATCH: good batch reached gold (True); bad batch was blocked at the gate (False)
```

**Acceptance criteria**: a deliberately bad batch must fail the quality gate and must not reach
gold -- confirmed, the `mars` batch's `Quality gate passed: False` and
`gold_region_totals created: False`. The clean batch must pass the gate and reach gold -- confirmed,
`Quality gate passed: True` and `gold_region_totals created: True`. Both runs also demonstrate the
retry policy absorbing a simulated transient ingest failure on attempt 1, succeeding on attempt 2.
Matches this capstone's own step-4 acceptance criterion and the overall capstone acceptance
criteria: the pipeline is idempotent and backfill-safe (Step 1), the star schema reconciles
(Step 2), gold aggregates are correct (Step 3), and a bad batch is caught by the quality gate
before serving (Step 4).

**Key takeaway**: wiring the data-quality gate as a real DAG dependency between the star schema and
`serve_gold` -- not just logging a warning -- is what physically prevents the `mars` batch from ever
reaching `gold_region_totals`, exactly matching ex-44's own beginner-scale demonstration of the same
principle at capstone scale.

**Why It Matters**: this closes the loop on every concept this course teaches -- idempotent,
incremental ingest; a cleaned, conformed, dimensionally-modeled star schema; a correctly-aggregated
gold layer; and an orchestrated DAG whose retry policy absorbs transient failures while its quality
gate structurally blocks genuinely bad data from ever reaching a downstream consumer. A real
production pipeline is, at its core, this same shape, scaled up.

---

&larr; Previous: [Advanced](../advanced.md) &middot; Next: [Drilling](../../drilling/overview.md)
&rarr;
