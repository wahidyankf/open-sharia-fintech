"""Example 45: Cassandra Table with Partition + Clustering Key."""  # => co-22: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from cassandra.cluster import Cluster, Session  # => co-22: cassandra-driver, the Apache Software Foundation-maintained Python driver


def setup_feed_table(session: Session) -> None:  # => co-22: a partition-key + clustering-column table for a time-series feed
    """Create a keyspace and table modeling a per-sensor feed, ordered by reading time within a partition."""  # => documents contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS sensor_feed")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: PRIMARY KEY ((sensor_id), reading_time) -- sensor_id PARTITIONS, reading_time CLUSTERS within it
        "CREATE TABLE sensor_feed ("  # => opens the DDL's column-definition list
        "sensor_id text, "  # => the PARTITION key column -- decides which node holds a given sensor's rows
        "reading_time timestamp, "  # => the CLUSTERING key column -- orders rows WITHIN a partition
        "temperature double, "  # => a plain, non-key value column
        "PRIMARY KEY ((sensor_id), reading_time)"  # => co-22: partition key groups rows, clustering key ORDERS them within a partition
        ") WITH CLUSTERING ORDER BY (reading_time DESC)"  # => co-22: newest reading first within each partition -- the common feed read
    )  # => closes the execute() call -- the table now exists with this exact partition + clustering layout


def insert_readings(session: Session) -> None:  # => co-22: 3 readings for ONE sensor -- all land in the SAME partition
    """Insert 3 out-of-order readings for one sensor -- Cassandra stores them clustering-key-sorted regardless."""  # => documents contract
    readings = [  # => co-22: deliberately inserted OUT of time order -- clustering order is enforced by the STORE, not insert order
        ("sensor-1", "2026-07-27 10:00:00", 21.5),  # => reading 1, chronologically FIRST, inserted FIRST
        ("sensor-1", "2026-07-27 10:02:00", 22.1),  # => reading 3, chronologically LAST, inserted SECOND
        ("sensor-1", "2026-07-27 10:01:00", 21.8),  # => inserted LAST but clusters BETWEEN the two readings above
    ]  # => 3 readings, deliberately out of chronological insert order -- clustering must re-sort them
    for sensor_id, reading_time, temperature in readings:  # => co-22: each INSERT targets the SAME partition key, sensor-1
        session.execute(  # => co-22: every row here lands in ONE partition -- Cassandra's clustering column sorts them on write
            "INSERT INTO sensor_feed (sensor_id, reading_time, temperature) VALUES (%s, %s, %s)",  # => positional CQL placeholders
            (sensor_id, reading_time, temperature),  # => bound in insert order, but STORED in clustering-key order
        )  # => closes this one execute() call -- runs once per reading, in the deliberately-scrambled loop order above


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    session = cluster.connect()  # => opens a session against that cluster
    setup_feed_table(session)  # => sets up the dedicated keyspace/table fixture
    insert_readings(session)  # => co-22: inserts 3 out-of-time-order readings, all in the sensor-1 partition

    rows = list(session.execute("SELECT reading_time, temperature FROM sensor_feed WHERE sensor_id = %s", ("sensor-1",)))  # => co-22: a single-partition scan
    times = [str(row.reading_time) for row in rows]  # => extracts the ordered reading times for inspection
    print(f"Readings for sensor-1, newest first: {times}")  # => Output line -- CLUSTERING ORDER BY DESC enforced regardless of insert order
    assert times == sorted(times, reverse=True)  # => co-22: rows come back CLUSTERING-KEY-ordered (newest first), NOT insert-ordered
    assert len(rows) == 3  # => co-22: all 3 readings landed in the SAME partition, exactly as the schema intended
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
