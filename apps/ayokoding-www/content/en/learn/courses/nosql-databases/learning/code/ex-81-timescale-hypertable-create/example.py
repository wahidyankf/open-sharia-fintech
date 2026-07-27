"""Example 81: TimescaleDB Hypertable Create."""  # => co-29: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import psycopg  # => co-29: psycopg, the official typed Python driver for PostgreSQL (TimescaleDB is a PG extension)


def create_hypertable(conn: psycopg.Connection) -> None:  # => co-29: converts a regular table into a time-partitioned hypertable
    """Create a regular metrics table, then convert it into a TimescaleDB hypertable via the current API."""  # => documents the contract
    conn.execute("DROP TABLE IF EXISTS metrics")  # => resets state -- this example is fully self-contained
    conn.execute(  # => a PLAIN PostgreSQL table -- nothing TimescaleDB-specific about this line yet
        "CREATE TABLE metrics (ts TIMESTAMPTZ NOT NULL, sensor_id TEXT NOT NULL, value DOUBLE PRECISION NOT NULL)"  # => no partitioning declared here -- create_hypertable() below adds it
    )  # => closes the execute() call -- a plain, non-partitioned table exists at this point
    conn.execute("SELECT create_hypertable('metrics', by_range('ts'))")  # => co-29: the CURRENT (v2.13+) generalized hypertable API
    # => co-29: the older positional form create_hypertable('metrics', 'ts') still works too, as the
    # => backward-compatible interface -- by_range('ts') is the form new code should reach for


def insert_readings(conn: psycopg.Connection) -> None:  # => co-29: writes arrive roughly in time order, timestamp-keyed
    """Insert timestamped sensor readings spanning several hours -- TimescaleDB auto-routes each into its time chunk."""  # => documents contract
    readings = [  # => co-29: deliberately spans several hours so inserts land across MULTIPLE time-partitioned chunks
        ("2026-07-27 00:00:00+00", "sensor-1", 21.5),  # => the EARLIEST reading -- hour 0
        ("2026-07-27 01:00:00+00", "sensor-1", 21.8),  # => hour 1's reading
        ("2026-07-27 02:00:00+00", "sensor-1", 22.1),  # => hour 2's reading
        ("2026-07-27 03:00:00+00", "sensor-1", 22.4),  # => the LATEST reading -- hour 3
    ]  # => closes the readings list -- 4 tuples spanning 3 hours, one sensor
    for ts, sensor_id, value in readings:  # => co-29: each insert is a plain SQL INSERT -- TimescaleDB routes it transparently
        conn.execute(  # => co-29: the hypertable's own chunk-routing is invisible to this INSERT statement
            "INSERT INTO metrics (ts, sensor_id, value) VALUES (%s, %s, %s)",
            (ts, sensor_id, value),  # => binds this one loop iteration's own reading
        )  # => closes this one execute() call -- runs once per reading
    conn.commit()  # => co-29: makes the 4 inserts durable and visible to the range query below


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    conn = psycopg.connect("host=localhost port=5433 dbname=nosqldb user=postgres password=nosqldb")  # => connects to the local TimescaleDB Docker container
    conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")  # => co-29: enables the extension -- TimescaleDB ships AS a PostgreSQL extension
    conn.commit()  # => makes the extension creation durable before the hypertable conversion below

    create_hypertable(conn)  # => co-29: converts metrics from a plain table into a time-partitioned hypertable
    insert_readings(conn)  # => co-29: inserts 4 readings spanning 3 hours

    chunk_count_row = conn.execute(  # => co-29: counts the ACTUAL time-partitioned chunks TimescaleDB created underneath the hypertable
        "SELECT COUNT(*) FROM timescaledb_information.chunks WHERE hypertable_name = 'metrics'"  # => queries TimescaleDB's own catalog view, not the metrics table itself
    ).fetchone()  # => a COUNT(*) query always returns exactly one row -- never genuinely None
    assert chunk_count_row is not None  # => confirms the COUNT(*) row genuinely came back
    chunk_count = chunk_count_row[0]  # => the single aggregate value this COUNT(*) query returns
    assert chunk_count >= 1  # => co-29: at least ONE chunk exists -- the hypertable conversion genuinely took effect

    rows = conn.execute(  # => co-29: a time-range SELECT, the dominant TSDB read pattern
        "SELECT ts, value FROM metrics WHERE ts >= '2026-07-27 00:00:00+00' AND ts < '2026-07-27 04:00:00+00' ORDER BY ts"  # => a bounded time-range filter, ORDER BY ts
    ).fetchall()  # => materializes every row this range query matched
    values_in_order = [row[1] for row in rows]  # => extracts values in the RETURNED (time) order
    assert values_in_order == [21.5, 21.8, 22.1, 22.4]  # => co-29: returned strictly in TIME order, matching insertion order here

    print(f"Hypertable 'metrics' created with {chunk_count} chunk(s)")  # => Output line -- exact chunk count depends on the default chunk_time_interval
    print(f"Time-range query returned {len(rows)} points, ordered by time: {values_in_order}")  # => Output: Time-range query returned 4 points, ordered by time: [21.5, 21.8, 22.1, 22.4]
    print("Plain SQL INSERT/SELECT -- TimescaleDB's chunk routing and time-partitioning are entirely transparent to the client")  # => Output line
    conn.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
