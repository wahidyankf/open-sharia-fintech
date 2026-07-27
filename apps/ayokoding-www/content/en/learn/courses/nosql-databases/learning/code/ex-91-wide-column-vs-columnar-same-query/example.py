"""Example 91: Wide-Column vs. Columnar, Same Query."""  # => co-36,co-22: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import statistics  # => co-36: median-of-N timing, the same discipline earlier timing-sensitive examples used
import time  # => co-36: perf_counter for the supplementary at-scale timing section

import duckdb  # => co-36: duckdb, the official Python API for the in-process, MIT-licensed columnar OLAP engine
from cassandra import InvalidRequest  # => co-22: Cassandra's own driver exception for a query its planner refuses to run
from cassandra.cluster import Cluster, Session  # => co-36: the official Cassandra Python driver -- the wide-column side of this contrast
from cassandra.concurrent import execute_concurrent_with_args  # => co-36: batches the at-scale seed instead of one round trip per row

SAMPLE_ROWS = [  # => co-36: the SAME 5 rows loaded into BOTH engines -- one dataset, two storage layouts
    ("user-1", 1, "click", 10.0),  # => user-1's first event -- lands in user-1's own partition
    ("user-1", 2, "view", 5.0),  # => user-1's second event -- SAME partition, clustered by event_id
    ("user-2", 1, "click", 20.0),  # => user-2's first event -- a DIFFERENT partition
    ("user-2", 2, "purchase", 100.0),  # => user-2's second event -- SAME partition as the row above
    ("user-3", 1, "view", 3.0),  # => user-3's only event -- a THIRD partition
]  # => 5 rows total, spread across 3 distinct partitions -- the shape both point-read and aggregate demos below rely on


def seed_cassandra(session: Session, rows: list[tuple[str, int, str, float]]) -> None:  # => co-22: the wide-column side, partitioned by user_id
    """Create events_91, partitioned by user_id and clustered by event_id, then load rows."""  # => documents the contract
    session.execute("DROP TABLE IF EXISTS events_91")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: PRIMARY KEY ((user_id), event_id) -- user_id is the partition key, event_id clusters WITHIN it
        "CREATE TABLE events_91 (user_id text, event_id int, event_type text, amount double, PRIMARY KEY ((user_id), event_id))"  # => the DDL string itself
    )  # => co-22: closes the CREATE TABLE call -- no other column can route a query the way user_id does
    insert = session.prepare("INSERT INTO events_91 (user_id, event_id, event_type, amount) VALUES (?, ?, ?, ?)")  # => a prepared statement, reused per row
    for row in rows:  # => co-22: each row lands in the partition NAMED by its own user_id -- Cassandra ROUTES it there directly
        session.execute(insert, row)  # => a normal single-row insert -- fine at this small scale


def seed_duckdb(con: duckdb.DuckDBPyConnection, rows: list[tuple[str, int, str, float]]) -> None:  # => co-33: the columnar side, no partition key at all
    """Create events_91_duck, a plain columnar table with no partitioning or index, then load rows."""  # => documents the contract
    con.execute("CREATE TABLE events_91_duck (user_id TEXT, event_id INT, event_type TEXT, amount DOUBLE)")  # => co-33: a flat columnar table -- DuckDB has no partition-key concept
    con.executemany("INSERT INTO events_91_duck VALUES (?, ?, ?, ?)", rows)  # => co-33: the IDENTICAL rows, stored column-by-column instead of partition-by-partition


def demonstrate_partition_point_read(session: Session, con: duckdb.DuckDBPyConnection) -> None:  # => co-22,co-33: the SAME point-read query against both engines
    """Run 'all events for user-1' against both engines and show how each one executes it."""  # => documents the contract
    cass_rows = list(session.execute("SELECT event_id, event_type, amount FROM events_91 WHERE user_id = %s", ("user-1",)))  # => co-22: partition-key-scoped -- ALWAYS allowed, no restriction
    assert len(cass_rows) == 2  # => co-22: exactly user-1's own 2 rows, nothing else read
    print(f"Cassandra point read (user-1):  {[(r.event_id, r.event_type, r.amount) for r in cass_rows]}")  # => Output: Cassandra point read (user-1):  [(1, 'click', 10.0), (2, 'view', 5.0)]

    duck_rows = con.execute("SELECT event_id, event_type, amount FROM events_91_duck WHERE user_id = 'user-1'").fetchall()  # => co-33: the IDENTICAL logical query
    assert duck_rows == [(1, "click", 10.0), (2, "view", 5.0)]  # => co-33: the SAME 2 rows -- both engines agree on the DATA
    print(f"DuckDB point read (user-1):     {duck_rows}")  # => Output: DuckDB point read (user-1):     [(1, 'click', 10.0), (2, 'view', 5.0)]

    plan_text = con.execute("EXPLAIN SELECT event_id, event_type, amount FROM events_91_duck WHERE user_id = 'user-1'").fetchall()[0][1]  # => co-33: EXPLAIN's own plan for the point read
    assert "SEQ_SCAN" in plan_text  # => co-33: DuckDB has NO index on user_id -- it reads EVERY row and filters, even for a single-user lookup
    print("DuckDB's own EXPLAIN plan uses SEQ_SCAN for the point read -- no partition or index lets it skip straight to user-1's rows")  # => Output line
    print("Cassandra ROUTES straight to user-1's own partition -- it never even considers user-2 or user-3's rows")  # => Output line


def demonstrate_cross_partition_aggregate(session: Session, con: duckdb.DuckDBPyConnection) -> None:  # => co-22,co-33,co-36: the SAME analytical query against both engines
    """Run 'total amount by event_type across ALL users' -- a query that does NOT name the partition key."""  # => documents the contract
    try:  # => co-22: event_type is NOT the partition key -- Cassandra's own query planner refuses this shape by default
        session.execute("SELECT event_type, amount FROM events_91 WHERE event_type = %s", ("click",))  # => co-22: a filter on a non-partition-key column
        raise AssertionError("expected InvalidRequest")  # => this line should never run -- Cassandra should reject the query above
    except InvalidRequest as exc:  # => co-22: Cassandra's own driver exception for a query it refuses to run without an explicit opt-in
        print(f"Cassandra rejects the aggregate's filter without ALLOW FILTERING: {exc}")  # => Output line -- the exact server-side rejection message

    filtered_rows = list(session.execute("SELECT event_type, amount FROM events_91 WHERE event_type = %s ALLOW FILTERING", ("click",)))  # => co-22: the SAME query, now with Cassandra's own explicit "yes, scan everything" escape hatch
    assert len(filtered_rows) == 2  # => co-22: both click rows, found only by reading EVERY partition -- ALLOW FILTERING is Cassandra's OWN admission of a full-cluster scan
    print(f"Cassandra WITH ALLOW FILTERING (event_type='click'): {[(r.event_type, r.amount) for r in filtered_rows]}")  # => Output: Cassandra WITH ALLOW FILTERING (event_type='click'): [('click', 10.0), ('click', 20.0)]

    duck_agg = con.execute("SELECT event_type, sum(amount) FROM events_91_duck GROUP BY event_type ORDER BY event_type").fetchall()  # => co-33: the IDENTICAL analytical shape -- GROUP BY a non-partition column
    assert duck_agg == [("click", 30.0), ("purchase", 100.0), ("view", 8.0)]  # => co-33: DuckDB's own aggregate, matching a hand-checkable sum of the 5 sample rows
    print(f"DuckDB GROUP BY event_type (no restriction needed): {duck_agg}")  # => Output: DuckDB GROUP BY event_type (no restriction needed): [('click', 30.0), ('purchase', 100.0), ('view', 8.0)]

    plan_text = con.execute("EXPLAIN SELECT event_type, sum(amount) FROM events_91_duck GROUP BY event_type").fetchall()[0][1]  # => co-33: reuses the Example 86 EXPLAIN-projection technique
    assert "Projections:" in plan_text and "event_type" in plan_text and "amount" in plan_text and "user_id" not in plan_text  # => co-33: the scan projects ONLY the 2 columns the aggregate needs -- user_id is never touched
    print("DuckDB needs NO escape hatch and NO restriction -- its own EXPLAIN plan shows it simply projects event_type and amount and aggregates")  # => Output line
    print("co-36: Cassandra's wide-column layout is BUILT for partition-scoped reads; a cross-partition aggregate needs its own explicit opt-in")  # => Output line
    print("co-36: DuckDB's columnar layout is BUILT for exactly this shape -- a GROUP BY over a subset of columns, no partition concept at all")  # => Output line


def demonstrate_at_scale_timing(session: Session, con: duckdb.DuckDBPyConnection) -> None:  # => co-36: a SUPPLEMENTARY, honestly-caveated timing data point -- not the primary proof above
    """Seed a larger dataset and time the SAME partition point read against both engines, median of several runs."""  # => documents the contract
    users, events_per_user = 2000, 50  # => co-36: enough rows that a full DuckDB scan touches real work, not a handful of in-cache rows
    scale_rows = [(f"scaleuser-{u}", e, "click" if e % 2 == 0 else "view", float(e)) for u in range(users) for e in range(events_per_user)]  # => co-36: 100,000 rows, same 4-column shape as SAMPLE_ROWS

    session.execute("DROP TABLE IF EXISTS events_91_scale")  # => resets state for this section's own table
    session.execute("CREATE TABLE events_91_scale (user_id text, event_id int, event_type text, amount double, PRIMARY KEY ((user_id), event_id))")  # => co-22: the SAME partitioned shape, at scale
    insert = session.prepare("INSERT INTO events_91_scale (user_id, event_id, event_type, amount) VALUES (?, ?, ?, ?)")  # => a prepared statement, reused across ALL 100,000 rows
    execute_concurrent_with_args(session, insert, scale_rows, concurrency=100)  # => co-36: concurrent batched inserts -- one row per network round trip would be impractically slow at this size

    con.execute("CREATE TABLE events_91_scale_duck (user_id TEXT, event_id INT, event_type TEXT, amount DOUBLE)")  # => co-33: the IDENTICAL 100,000 rows, columnar
    con.executemany("INSERT INTO events_91_scale_duck VALUES (?, ?, ?, ?)", scale_rows)  # => co-33: bulk-loads all 100,000 rows in one call

    def time_cassandra_read() -> float:  # => co-36: one timed partition-scoped point read
        start = time.perf_counter()  # => marks the start of JUST the query, not connection setup
        list(session.execute("SELECT event_type, amount FROM events_91_scale WHERE user_id = %s", ("scaleuser-1000",)))  # => co-22: routed straight to ONE partition among 2000
        return time.perf_counter() - start  # => elapsed seconds for this single query

    def time_duckdb_read() -> float:  # => co-36: the IDENTICAL logical query, timed the same way
        start = time.perf_counter()  # => marks the start of JUST the query
        con.execute("SELECT event_type, amount FROM events_91_scale_duck WHERE user_id = ?", ["scaleuser-1000"]).fetchall()  # => co-33: a full SEQ_SCAN over all 100,000 rows, filtered in-flight
        return time.perf_counter() - start  # => elapsed seconds for this single query

    time_cassandra_read()  # => a warmup call each -- excludes one-time connection/JIT overhead from the timed samples below
    time_duckdb_read()  # => a warmup call each
    cassandra_median_ms = statistics.median(time_cassandra_read() for _ in range(9)) * 1000  # => co-36: median of 9 runs, damping single-sample noise
    duckdb_median_ms = statistics.median(time_duckdb_read() for _ in range(9)) * 1000  # => co-36: median of 9 runs, the SAME discipline

    print(f"At 100,000 rows / 2000 partitions -- Cassandra partition read: {cassandra_median_ms:.3f} ms (median of 9)")  # => Output line -- exact ms machine-dependent
    print(f"At 100,000 rows / 2000 partitions -- DuckDB full-table scan:   {duckdb_median_ms:.3f} ms (median of 9)")  # => Output line -- exact ms machine-dependent
    print("HONEST CAVEAT: on this single local machine, DuckDB's in-process vectorized scan of 100,000 in-memory rows can")  # => Output line -- see co-36 discussion below for why this does not undercut the architectural claim
    print("still beat Cassandra's own network round trip -- Cassandra's win is architectural: its point-read cost stays FLAT")  # => Output line
    print("as TOTAL cluster data grows (it only ever touches one partition), while DuckDB's SEQ_SCAN cost grows with EVERY")  # => Output line
    print("row in the table -- at distributed, multi-node, larger-than-one-machine's-memory scale, that flat-vs-growing curve is what wins")  # => Output line


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => co-22: connects to the local Cassandra Docker container
    session = cluster.connect()  # => a live CQL session
    session.execute("CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}")  # => idempotent -- reuses the keyspace earlier Cassandra examples created
    session.set_keyspace("nosqldb")  # => all statements below target this keyspace

    con = duckdb.connect()  # => co-33: an IN-PROCESS DuckDB connection, no server to manage

    seed_cassandra(session, SAMPLE_ROWS)  # => co-22: loads the 5-row sample into Cassandra's wide-column table
    seed_duckdb(con, SAMPLE_ROWS)  # => co-33: loads the IDENTICAL 5 rows into DuckDB's columnar table

    demonstrate_partition_point_read(session, con)  # => co-22,co-33: proves the point-read distinction structurally, via EXPLAIN and partition routing
    demonstrate_cross_partition_aggregate(session, con)  # => co-22,co-33,co-36: proves the analytical-aggregate distinction structurally, via ALLOW FILTERING and EXPLAIN
    demonstrate_at_scale_timing(session, con)  # => co-36: a supplementary, honestly-caveated real timing data point at 100,000 rows

    con.close()  # => always release what you open
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
