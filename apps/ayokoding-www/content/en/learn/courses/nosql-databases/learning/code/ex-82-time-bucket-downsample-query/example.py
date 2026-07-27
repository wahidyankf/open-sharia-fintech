"""Example 82: time_bucket Downsample Query."""  # => co-30: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import statistics  # => co-30: computes the hand-rolled hourly average this example verifies the SQL rollup against

import psycopg  # => co-30: psycopg, the official typed Python driver for PostgreSQL (TimescaleDB is a PG extension)


def seed_raw_readings(conn: psycopg.Connection) -> None:  # => co-30: high-resolution, per-minute readings across 2 hours
    """Seed 120 per-minute readings across 2 hours -- raw resolution, before any downsampling."""  # => documents the contract
    conn.execute("DROP TABLE IF EXISTS sensor_readings")  # => resets state -- this example is fully self-contained
    conn.execute("CREATE TABLE sensor_readings (ts TIMESTAMPTZ NOT NULL, value DOUBLE PRECISION NOT NULL)")  # => a plain table
    conn.execute("SELECT create_hypertable('sensor_readings', by_range('ts'))")  # => co-29: converts it to a hypertable, same API Example 81 used
    for minute in range(120):  # => co-30: 120 raw, per-minute points -- 2 full hours at 1-minute resolution
        hour = minute // 60  # => which hour bucket this raw point WILL roll up into
        value = 20.0 + hour * 2.0 + (minute % 60) * 0.01  # => co-30: a deterministic, gently rising value per minute
        conn.execute(  # => co-30: each raw point is its OWN row -- no pre-aggregation happens here
            "INSERT INTO sensor_readings (ts, value) VALUES (%s, %s)",  # => positional placeholders bind this one minute's own timestamp and value
            (f"2026-07-27 {hour:02d}:{minute % 60:02d}:00+00", value),  # => this loop iteration's own minute-resolution reading
        )  # => closes this one execute() call -- runs once per raw minute
    conn.commit()  # => makes all 120 raw inserts durable and visible to the queries below


def hand_computed_hourly_average(conn: psycopg.Connection, hour: int) -> float:  # => co-30: the INDEPENDENT, hand-rolled rollup this example checks against
    """Compute an hour's average by pulling ALL 60 raw points and averaging them in Python."""  # => documents the contract
    rows = conn.execute(  # => co-30: pulls every RAW point for this hour -- the expensive, non-bucketed path
        "SELECT value FROM sensor_readings WHERE ts >= %s AND ts < %s",  # => a bounded, half-open [hour, hour+1) time-range filter
        (f"2026-07-27 {hour:02d}:00:00+00", f"2026-07-27 {hour + 1:02d}:00:00+00"),  # => this call's own hour boundary, as a pair of timestamps
    ).fetchall()  # => materializes all 60 raw points this specific hour matched
    return statistics.mean(row[0] for row in rows)  # => co-30: the hand-computed average, independent of time_bucket()


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    conn = psycopg.connect("host=localhost port=5433 dbname=nosqldb user=postgres password=nosqldb")  # => connects to the local TimescaleDB Docker container
    conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")  # => enables the extension, idempotent if already present
    conn.commit()  # => makes the extension creation durable before the hypertable conversion below

    seed_raw_readings(conn)  # => seeds 120 per-minute raw readings across 2 hours

    bucketed_rows = conn.execute(  # => co-30: time_bucket('1 hour', ts) rolls raw per-minute points into hourly averages
        "SELECT time_bucket('1 hour', ts) AS bucket, avg(value) AS avg_value "  # => the aggregate-per-bucket projection
        "FROM sensor_readings GROUP BY bucket ORDER BY bucket"  # => concatenated onto the line above -- ONE SQL statement string
    ).fetchall()  # => materializes one row per hourly bucket -- 120 raw rows collapse to 2
    assert len(bucketed_rows) == 2  # => co-30: 2 hours of raw data -- exactly 2 hourly buckets

    for hour, (_bucket, bucketed_avg) in enumerate(bucketed_rows):  # => co-30: verifies EACH bucket against its own hand-computed rollup
        hand_avg = hand_computed_hourly_average(conn, hour)  # => co-30: the independent, hand-rolled average for this same hour
        assert abs(bucketed_avg - hand_avg) < 1e-9  # => co-30: the SQL rollup matches the hand-computed rollup, to floating-point precision
        print(f"Hour {hour}: time_bucket avg={bucketed_avg:.4f}, hand-computed avg={hand_avg:.4f}")  # => Output line, one per hour

    print("The bucketed aggregate exactly matches a hand-computed rollup of the same raw points, for every hour")  # => Output line
    conn.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
