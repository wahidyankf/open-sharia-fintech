"""Example 59: Cassandra Secondary Index Cost."""  # => co-17,co-22: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => co-17: a new secondary index builds ASYNCHRONOUSLY -- a short wait avoids racing its own build

from cassandra.cluster import Cluster, Session  # => co-17: cassandra-driver, the Apache Software Foundation-maintained Python driver
from cassandra.protocol import InvalidRequest  # => co-17: the exception a non-partition-key filter raises WITHOUT a secondary index


def setup_orders_table(session: Session) -> None:  # => co-22: partitioned by customer_id -- status is NOT part of the primary key
    """Create a table partitioned by customer_id, with a status column that is NOT part of the key."""  # => documents the contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS orders_by_status")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: customer_id is the ONLY partition key -- status is a plain, non-key column
        "CREATE TABLE orders_by_status (customer_id int, order_id int, status text, PRIMARY KEY ((customer_id), order_id))"
    )
    for i in range(100):  # => co-17: 100 rows across 10 customers, a mix of statuses
        session.execute(  # => co-22: every row lands in the partition matching (i % 10)
            "INSERT INTO orders_by_status (customer_id, order_id, status) VALUES (%s, %s, %s)",  # => positional CQL placeholders
            (i % 10, i, "shipped" if i % 5 == 0 else "pending"),  # => customer_id cycles 0-9; every 5th row is "shipped"
        )


def query_by_status_without_index(session: Session) -> bool:  # => co-17: attempts to filter on status, a NON-partition-key column
    """Attempt to filter on status alone -- expect rejection, since status is not the partition key."""  # => documents contract
    try:  # => catches ONLY the specific rejection Cassandra's planner raises for this un-indexed filter
        list(session.execute("SELECT * FROM orders_by_status WHERE status = %s", ("shipped",)))  # => co-17: status is not indexed yet
        return True  # => unreachable in this example -- Cassandra rejects this without an index
    except InvalidRequest:  # => co-17: Cassandra refuses to filter on a non-indexed, non-partition-key column
        return False  # => co-17: correctly rejected, exactly like Example 47's missing-partition-key case


def query_by_status_with_index(session: Session) -> int:  # => co-17: the SAME filter, now served by a secondary index
    """Create a secondary index on status, then re-run the same filter -- now it succeeds."""  # => documents the contract
    session.execute("CREATE INDEX IF NOT EXISTS ON orders_by_status (status)")  # => co-17: a SECONDARY index -- cross-node fan-out, unlike a partition-key lookup
    time.sleep(3)  # => co-17: gives the new index a moment to finish its asynchronous build before querying it
    rows = list(session.execute("SELECT * FROM orders_by_status WHERE status = %s", ("shipped",)))  # => co-17: NOW permitted, served by the secondary index
    return len(rows)  # => hand back the row count now that the index serves the query


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    session = cluster.connect()  # => opens a session against that cluster
    setup_orders_table(session)  # => sets up the 100-row, 10-partition, mixed-status fixture

    rejected = not query_by_status_without_index(session)  # => co-17: confirms the un-indexed filter query was rejected
    assert rejected is True  # => co-17: Cassandra refused it -- status is not the partition key, and no index exists yet
    print(f"Query on status BEFORE a secondary index: rejected = {rejected}")  # => Output: Query on status BEFORE a secondary index: rejected = True

    row_count = query_by_status_with_index(session)  # => co-17: the SAME filter, now index-served
    assert row_count == 20  # => co-17: 20 of the 100 rows (i % 5 == 0) have status="shipped"
    print(f"Query on status AFTER a secondary index:  {row_count} rows returned")  # => Output: Query on status AFTER a secondary index:  20 rows returned
    # => co-17,co-22: a Cassandra secondary index works, but it is NOT free -- unlike a partition-key
    # => query (Example 46), which routes to exactly the node owning that partition, a secondary-index
    # => query must FAN OUT to EVERY node in the cluster (each node checks its own local index shard),
    # => because the index does not change WHERE data physically lives, only how it is looked up locally
    # => on each node -- this cross-node coordination cost is the qualitative tradeoff this example verifies
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
