"""Example 47: Cassandra Query Without a Partition Key."""  # => co-22: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from cassandra.cluster import Cluster, Session  # => co-22: cassandra-driver, the Apache Software Foundation-maintained Python driver
from cassandra.protocol import InvalidRequest  # => co-22: the exact exception Cassandra raises for a rejected filter query


def setup_orders_table(session: Session) -> None:  # => co-22: reuses the SAME shape as Example 46 -- partitioned by customer_id
    """Create the same customer_id-partitioned table Example 46 used, with a handful of rows."""  # => documents the contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS customer_orders_2")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: the SAME partition-key + no-secondary-index shape as Example 46
        "CREATE TABLE customer_orders_2 (customer_id int, order_id int, amount double, PRIMARY KEY ((customer_id), order_id))"
    )  # => closes the execute() call -- the table now exists with this exact partition layout
    for i in range(20):  # => a small, sufficient fixture -- this example is about REJECTION, not row count
        session.execute("INSERT INTO customer_orders_2 (customer_id, order_id, amount) VALUES (%s, %s, %s)", (i % 4, i, float(i)))


def try_query_without_partition_key(session: Session) -> bool:  # => co-22: attempts a filter query that OMITS the partition key entirely
    """Attempt to filter on amount alone, with NO partition key in the WHERE clause -- expect rejection."""  # => documents contract
    try:  # => catches ONLY the specific rejection Cassandra's planner raises for this unsafe shape
        list(session.execute("SELECT * FROM customer_orders_2 WHERE amount > %s", (10.0,)))  # => co-22: no customer_id in the WHERE clause at all
        return True  # => unreachable in this example -- Cassandra rejects this shape by design
    except InvalidRequest:  # => co-22: Cassandra's query planner REFUSES a filter that would require scanning every partition
        return False  # => co-22: correctly rejected -- this is Cassandra protecting the cluster from an accidental full scan


def try_query_with_allow_filtering(session: Session) -> int:  # => co-22: the SAME query, but with the explicit escape hatch
    """Re-run the same filter with ALLOW FILTERING -- Cassandra now permits it, but the caller opted in explicitly."""  # => documents contract
    rows = list(session.execute("SELECT * FROM customer_orders_2 WHERE amount > %s ALLOW FILTERING", (10.0,)))  # => co-22: ALLOW FILTERING is an explicit, deliberate opt-in
    return len(rows)  # => hand back the row count now that the scan was explicitly permitted


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    session = cluster.connect()  # => opens a session against that cluster
    setup_orders_table(session)  # => sets up the 20-row, partition-keyed fixture

    rejected = not try_query_without_partition_key(session)  # => co-22: confirms the plain filter query was rejected
    assert rejected is True  # => co-22: Cassandra refused the query -- it would have required scanning EVERY partition
    print(f"Query without partition key: rejected = {rejected} (InvalidRequest raised)")  # => Output: Query without partition key: rejected = True (InvalidRequest raised)

    row_count = try_query_with_allow_filtering(session)  # => co-22: the SAME filter, now with the explicit opt-in
    assert row_count == 9  # => co-22: 9 of the 20 rows (order_id 11-19) have amount > 10.0
    print(f"Same query WITH ALLOW FILTERING: {row_count} rows returned (explicit opt-in to a full scan)")  # => Output: Same query WITH ALLOW FILTERING: 9 rows returned (explicit opt-in to a full scan)
    # => co-22: ALLOW FILTERING does not make the underlying full-cluster scan cheap -- it only removes
    # => the SAFETY RAIL that stops a query from accidentally doing one; production code should treat
    # => needing it as a signal the schema's partition key does not fit this access pattern
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
