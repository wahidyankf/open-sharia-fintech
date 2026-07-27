"""Example 85: Time-Series vs. Wide-Column Feed."""  # => co-29,co-22,co-30: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import psycopg  # => co-29: psycopg, the official typed Python driver for PostgreSQL (TimescaleDB is a PG extension)
from cassandra.cluster import Cluster, Session  # => co-22: cassandra-driver, the Apache Software Foundation-maintained Python driver

# The SAME metrics feed, modeled two ways: a TimescaleDB hypertable, and a Cassandra wide-column
# partition (contrast with Example 71's embedded-array-vs-partition and Example 79's own feed shape).


def timescale_feed_query(conn: psycopg.Connection) -> list[float]:  # => co-29: TimescaleDB's own answer to "readings for sensor-1 in this hour"
    """Seed 4 readings for sensor-1 in a hypertable, then read them back time-ordered."""  # => documents the contract
    conn.execute("DROP TABLE IF EXISTS feed_timescale")  # => resets state -- this example is fully self-contained
    conn.execute("CREATE TABLE feed_timescale (sensor_id TEXT NOT NULL, ts TIMESTAMPTZ NOT NULL, value DOUBLE PRECISION NOT NULL)")  # => a plain table
    conn.execute("SELECT create_hypertable('feed_timescale', by_range('ts'))")  # => co-29: converts it to a hypertable, same API Example 81 used
    readings = [
        ("sensor-1", "2026-07-27 09:00:00+00", 20.0),
        ("sensor-1", "2026-07-27 09:15:00+00", 20.5),  # => the first 2 of 4 readings, TimescaleDB timestamptz syntax
        ("sensor-1", "2026-07-27 09:30:00+00", 21.0),
        ("sensor-1", "2026-07-27 09:45:00+00", 21.5),
    ]  # => co-29: 4 readings, one sensor, 45-minute span
    for sensor_id, ts, value in readings:  # => co-29: each insert is a plain SQL INSERT -- chunk routing is transparent
        conn.execute("INSERT INTO feed_timescale (sensor_id, ts, value) VALUES (%s, %s, %s)", (sensor_id, ts, value))  # => binds this loop iteration's own reading
    rows = conn.execute(  # => co-29: the dominant TSDB read pattern -- a time-range scan for one sensor
        "SELECT value FROM feed_timescale WHERE sensor_id = %s AND ts >= %s AND ts < %s ORDER BY ts",  # => a bounded, per-sensor time-range filter
        ("sensor-1", "2026-07-27 09:00:00+00", "2026-07-27 10:00:00+00"),  # => the SAME sensor and time window cassandra_feed_query will use
    ).fetchall()  # => materializes the matched rows in time order
    return [row[0] for row in rows]  # => hand back the values in time order


def cassandra_feed_query(session: Session) -> list[float]:  # => co-22: Cassandra's own answer to the IDENTICAL shaped read
    """Seed the SAME 4 readings for sensor-1 in a Cassandra wide-column partition, then read them back."""  # => documents the contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS feed_wide")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: sensor_id partitions, ts clusters -- the SAME partition+clustering shape Example 79 used
        "CREATE TABLE feed_wide (sensor_id text, ts timestamp, value double, PRIMARY KEY ((sensor_id), ts))"  # => partition key sensor_id, clustering key ts
    )  # => closes the execute() call -- the table now exists with this exact partition + clustering layout
    readings = [
        ("sensor-1", "2026-07-27 09:00:00", 20.0),
        ("sensor-1", "2026-07-27 09:15:00", 20.5),  # => the first 2 of 4 identical readings, Cassandra timestamp syntax
        ("sensor-1", "2026-07-27 09:30:00", 21.0),
        ("sensor-1", "2026-07-27 09:45:00", 21.5),
    ]  # => co-22: the IDENTICAL 4 readings
    for sensor_id, ts, value in readings:  # => co-22: each INSERT is a cheap, sequential append into sensor-1's own partition
        session.execute("INSERT INTO feed_wide (sensor_id, ts, value) VALUES (%s, %s, %s)", (sensor_id, ts, value))  # => binds this loop iteration's own reading
    rows = list(
        session.execute(  # => co-22: a single-partition scan, ordered by the clustering key -- Cassandra's own time-range read
            "SELECT value FROM feed_wide WHERE sensor_id = %s AND ts >= %s AND ts < %s",  # => a bounded time-range filter, scoped to ONE partition
            ("sensor-1", "2026-07-27 09:00:00", "2026-07-27 10:00:00"),  # => the SAME sensor and time window timescale_feed_query used
        )
    )  # => closes the list()/execute() call -- materializes the matched rows
    return [row.value for row in rows]  # => hand back the values in clustering (time) order


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    timescale_conn = psycopg.connect("host=localhost port=5433 dbname=nosqldb user=postgres password=nosqldb")  # => connects to the local TimescaleDB Docker container
    timescale_conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")  # => enables the extension, idempotent if already present
    timescale_conn.commit()  # => makes the extension creation durable before the hypertable conversion below
    cassandra_cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    cassandra_session = cassandra_cluster.connect()  # => opens a session against that cluster

    timescale_values = timescale_feed_query(timescale_conn)  # => co-29: TimescaleDB's own answer to the shared time-range read
    timescale_conn.commit()  # => makes Timescale's 4 inserts durable
    cassandra_values = cassandra_feed_query(cassandra_session)  # => co-22: Cassandra's own answer to the IDENTICAL shaped read

    expected = [20.0, 20.5, 21.0, 21.5]  # => co-29,co-22: the SAME shared expectation for both stores, since they seed identical logical data
    assert timescale_values == cassandra_values == expected  # => co-29,co-22: BOTH stores serve the identical time-range read correctly
    print(f"TimescaleDB time-range read: {timescale_values}")  # => Output: TimescaleDB time-range read: [20.0, 20.5, 21.0, 21.5]
    print(f"Cassandra time-range read:   {cassandra_values}")  # => Output: Cassandra time-range read:   [20.0, 20.5, 21.0, 21.5]
    print("Identical results, same time-range read, from two genuinely different engines")  # => Output line

    print("Retention:    TimescaleDB has a built-in add_retention_policy (Example 83) -- the engine drops old chunks itself")  # => Output line
    print("              Cassandra has NO built-in retention concept -- per-row TTL (Example 48) is the closest hand-rolled equivalent, set at every INSERT")  # => Output line
    print("Downsampling: TimescaleDB has built-in time_bucket() + continuous aggregates (Examples 82, 84) -- the engine maintains rollups for you")  # => Output line
    print("              Cassandra has NO built-in downsampling -- an application must hand-roll its own rollup job, writing summarized rows to a separate table itself")  # => Output line
    # => co-29,co-30: this is the concrete payoff of co-29's own definition -- a TSDB bakes the time
    # => axis, retention, and rollups INTO the engine, while a general wide-column store leaves all
    # => three entirely to the schema and application code, even though BOTH can physically store and
    # => read the same time-ordered, partition-scoped data

    timescale_conn.close()  # => always release what you open
    cassandra_cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
