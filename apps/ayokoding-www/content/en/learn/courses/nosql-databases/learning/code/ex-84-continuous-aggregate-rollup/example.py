"""Example 84: Continuous Aggregate Rollup."""  # => co-31,co-28: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import LiteralString  # => co-31: both call sites below pass a compile-time string constant -- LiteralString states that honestly

import psycopg  # => co-31: psycopg, the official typed Python driver for PostgreSQL (TimescaleDB is a PG extension)
from psycopg import sql  # => co-31: composes the literal query into a genuinely typed Composed object, not a plain f-string


def seed_raw_events(conn: psycopg.Connection, hours: int, points_per_hour: int) -> None:  # => co-31: many raw points, the expensive source a cagg pre-summarizes
    """Create a hypertable and seed points_per_hour raw points for each of hours hours."""  # => documents the contract, no runtime output
    conn.execute("DROP MATERIALIZED VIEW IF EXISTS events_hourly")  # => resets state FIRST -- the cagg view depends on events_raw, so it must drop before the table below
    conn.execute("DROP TABLE IF EXISTS events_raw")  # => resets state -- this example is fully self-contained
    conn.execute("CREATE TABLE events_raw (ts TIMESTAMPTZ NOT NULL, value DOUBLE PRECISION NOT NULL)")  # => a plain table
    conn.execute("SELECT create_hypertable('events_raw', by_range('ts'))")  # => co-29: converts it to a hypertable, same API Example 81 used
    for hour in range(hours):  # => co-31: HOURS worth of raw data -- this is what re-scanning the raw hypertable would cost
        for point in range(points_per_hour):  # => co-31: POINTS_PER_HOUR raw rows land in EACH hourly bucket
            offset_seconds = point * (3600 // points_per_hour)  # => spreads points_per_hour points evenly across the hour
            minute, second = divmod(offset_seconds, 60)  # => converts the raw offset into a valid minute:second pair, avoiding an out-of-range seconds field
            conn.execute(  # => co-31: each raw point is its OWN row -- no pre-aggregation happens at insert time
                "INSERT INTO events_raw (ts, value) VALUES (%s, %s)",  # => positional placeholders bind this one raw point's own timestamp and value
                (f"2026-07-27 {hour:02d}:{minute:02d}:{second:02d}+00", 10.0 + hour + point * 0.001),  # => this loop iteration's own raw point
            )  # => closes this one execute() call -- runs once per raw point


def create_and_refresh_continuous_aggregate(conn: psycopg.Connection) -> None:  # => co-31: TSL tier (per co-28) -- pre-computed, incrementally maintained hourly rollups
    """Define an hourly continuous aggregate over events_raw, then manually refresh it once."""  # => documents the contract
    conn.execute(  # => co-31: WITH (timescaledb.continuous) -- the exact syntax that marks this as a continuous aggregate, not a plain view
        # => CREATE MATERIALIZED VIEW ... WITH (timescaledb.continuous) cannot run inside a transaction
        # => block, which is why this connection runs in autocommit mode (co-31)
        "CREATE MATERIALIZED VIEW events_hourly WITH (timescaledb.continuous) AS "  # => the continuous-aggregate marker clause
        "SELECT time_bucket('1 hour', ts) AS bucket, avg(value) AS avg_value "  # => the aggregate-per-bucket projection this view maintains
        "FROM events_raw GROUP BY bucket"  # => concatenated onto the lines above -- ONE SQL statement string
    )  # => closes the execute() call -- events_hourly now exists as a continuous aggregate
    conn.execute("CALL refresh_continuous_aggregate('events_hourly', NULL, NULL)")  # => co-31: refreshes the WHOLE aggregate now, instead of waiting for a scheduled policy


def actual_rows_scanned(conn: psycopg.Connection, query: LiteralString, params: tuple[str, ...]) -> int:  # => co-31: the REAL row count EXPLAIN ANALYZE observed, not an estimate
    """Run EXPLAIN (ANALYZE, FORMAT JSON) on query and return the top plan node's Actual Rows."""  # => documents the contract
    composed_query = sql.SQL("EXPLAIN (ANALYZE, FORMAT JSON) {}").format(sql.SQL(query))  # => co-31: a Composed object, not a plain f-string -- resolves psycopg's own typed overload
    plan_row = conn.execute(composed_query, params).fetchone()  # => co-31: FORMAT JSON makes the plan machine-parseable
    assert plan_row is not None  # => confirms the EXPLAIN row genuinely came back
    plan_json = plan_row[0]  # => the single JSON plan value this EXPLAIN query returns
    return plan_json[0]["Plan"]["Actual Rows"]  # => co-31: the ACTUAL (not estimated) row count the top-level plan node returned


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    conn = psycopg.connect(
        "host=localhost port=5433 dbname=nosqldb user=postgres password=nosqldb", autocommit=True
    )  # => co-31: autocommit=True -- CREATE MATERIALIZED VIEW ... WITH (timescaledb.continuous) cannot run inside a transaction block
    conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")  # => enables the extension, idempotent if already present

    hours, points_per_hour = 5, 100  # => co-31: 5 hours x 100 points/hour = 500 raw rows, rolling up into 5 hourly buckets
    seed_raw_events(conn, hours, points_per_hour)  # => seeds 500 raw points across 5 hours
    create_and_refresh_continuous_aggregate(conn)  # => co-31: defines and refreshes the hourly continuous aggregate

    raw_rows_scanned = actual_rows_scanned(  # => co-31: re-scanning the RAW hypertable for the same 5-hour range
        conn,
        "SELECT ts, value FROM events_raw WHERE ts >= %s AND ts < %s",
        ("2026-07-27 00:00:00+00", "2026-07-27 05:00:00+00"),  # => the SAME 5-hour range read raw
    )  # => closes this actual_rows_scanned() call
    cagg_rows_scanned = actual_rows_scanned(  # => co-31: reading the SAME 5-hour range from the pre-aggregated continuous aggregate instead
        conn,
        "SELECT bucket, avg_value FROM events_hourly WHERE bucket >= %s AND bucket < %s",
        ("2026-07-27 00:00:00+00", "2026-07-27 05:00:00+00"),  # => the SAME 5-hour range read pre-aggregated
    )  # => closes this actual_rows_scanned() call

    print(f"Raw hypertable range read:        {raw_rows_scanned} rows scanned")  # => Output: Raw hypertable range read:        500 rows scanned
    print(f"Continuous aggregate range read:  {cagg_rows_scanned} rows scanned")  # => Output: Continuous aggregate range read:  5 rows scanned
    assert raw_rows_scanned == hours * points_per_hour  # => co-31: confirms the raw path genuinely re-scans EVERY one of the 500 raw points
    assert cagg_rows_scanned == hours  # => co-31: confirms the cagg path reads only the 5 pre-computed hourly buckets
    assert cagg_rows_scanned < raw_rows_scanned  # => co-31: the pre-aggregated view is scanned, NOT the raw hypertable -- exactly what this example verifies
    print(f"The continuous aggregate scanned {raw_rows_scanned // cagg_rows_scanned}x fewer rows for the identical 5-hour range query")  # => Output: The continuous aggregate scanned 100x fewer rows for the identical 5-hour range query
    # => co-28: continuous aggregates are a TSL / Community feature (source-available, NOT OSI-approved),
    # => the same license tier Example 83's retention policy carries -- distinct from the Apache-2.0
    # => create_hypertable/time_bucket API Examples 81-82 used
    conn.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
