"""Example 39: Cassandra Quorum Tuning."""  # => co-07: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => co-07: measures wall-clock latency at each consistency level, honestly, on a single-node cluster

from cassandra.cluster import Cluster, Session  # => co-07: cassandra-driver, the Apache Software Foundation-maintained Python driver
from cassandra.query import ConsistencyLevel, SimpleStatement  # => co-07: per-query consistency-level knobs


def setup_keyspace_and_table(session: Session) -> None:  # => co-07: creates a keyspace/table this example owns exclusively
    """Create a dedicated keyspace and table for this quorum-tuning demonstration."""  # => documents the contract
    session.execute(  # => co-07: replication_factor 1 -- this is a SINGLE-NODE local cluster, not a production topology
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS quorum_demo")  # => resets state -- this example is fully self-contained
    session.execute("CREATE TABLE quorum_demo (id int PRIMARY KEY, value text)")  # => a minimal table for this demonstration


def write_at_quorum(session: Session, row_id: int, value: str) -> float:  # => co-07: writes at QUORUM, returns elapsed seconds
    """Insert a row with consistency level QUORUM, returning wall-clock latency."""  # => documents the contract
    statement = SimpleStatement(  # => co-07: wraps the query so a per-statement consistency level can be attached
        "INSERT INTO quorum_demo (id, value) VALUES (%s, %s)",  # => positional CQL placeholders, bound below
        consistency_level=ConsistencyLevel.QUORUM,  # => co-07: WRITE at QUORUM -- must be acked by a majority of replicas
    )  # => closes the SimpleStatement -- query text and consistency level bundled together
    start = time.perf_counter()  # => marks the start of the timed write
    session.execute(statement, (row_id, value))  # => co-07: the actual timed QUORUM write
    return time.perf_counter() - start  # => elapsed wall-clock seconds for this one write


def read_at_level(session: Session, row_id: int, level: int) -> tuple[str | None, float]:  # => co-07: reads at a GIVEN level, returns (value, elapsed)
    """Read a row at the given consistency level, returning (value, elapsed_seconds)."""  # => documents the contract
    statement = SimpleStatement(  # => co-07: wraps the query so a per-statement consistency level can be attached
        "SELECT value FROM quorum_demo WHERE id = %s",  # => a single positional placeholder, bound below
        consistency_level=level,  # => co-07: READ at the level the caller specifies -- ONE or QUORUM, contrasted below
    )  # => closes the SimpleStatement -- query text and consistency level bundled together
    start = time.perf_counter()  # => marks the start of the timed read
    row = session.execute(statement, (row_id,)).one()  # => co-07: the actual timed read at this consistency level
    elapsed = time.perf_counter() - start  # => elapsed wall-clock seconds for this one read
    return (row.value if row else None), elapsed  # => hand back both the value read and how long it took


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    session = cluster.connect()  # => opens a session against that cluster
    setup_keyspace_and_table(session)  # => sets up the dedicated keyspace/table fixture

    write_latency = write_at_quorum(session, 1, "quorum-committed-value")  # => co-07: writes at QUORUM, timed
    value_at_one, latency_one = read_at_level(session, 1, ConsistencyLevel.ONE)  # => co-07: reads at ONE -- consults just 1 replica
    value_at_quorum, latency_quorum = read_at_level(session, 1, ConsistencyLevel.QUORUM)  # => co-07: reads at QUORUM -- consults a majority

    assert value_at_one == "quorum-committed-value"  # => co-07: on THIS single-node cluster, ONE and QUORUM read the same single replica
    assert value_at_quorum == "quorum-committed-value"  # => co-07: both levels agree here -- the contrast is in LATENCY, not correctness, on 1 node
    print(f"Write at QUORUM: {write_latency * 1000:.2f}ms")  # => Output line -- exact ms value machine-dependent
    print(f"Read at ONE:     {latency_one * 1000:.2f}ms, value={value_at_one}")  # => Output line
    print(f"Read at QUORUM:  {latency_quorum * 1000:.2f}ms, value={value_at_quorum}")  # => Output line
    # => co-07: on a REAL multi-node cluster, QUORUM reads/writes coordinate across multiple replicas
    # => and cost measurably more latency than ONE -- this single-node cluster demonstrates the API
    # => and correctness contract; Example 75 (Advanced tier) measures the latency GAP itself, simulated
    # => across a genuinely multi-replica model
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
