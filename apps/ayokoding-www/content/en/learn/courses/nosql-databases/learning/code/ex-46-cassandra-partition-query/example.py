"""Example 46: Cassandra Partition-Scoped Query."""  # => co-22: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => co-22: measures wall-clock latency for a single-partition read, honestly, on this local cluster

from cassandra.cluster import Cluster, Session  # => co-22: cassandra-driver, the Apache Software Foundation-maintained Python driver


def setup_orders_table(session: Session) -> None:  # => co-22: a partition-key-per-customer table, many rows per partition
    """Create a table partitioned by customer_id, with 500 rows spread across 20 customers."""  # => documents the contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS customer_orders")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: PRIMARY KEY ((customer_id), order_id) -- customer_id PARTITIONS the 500 rows into 20 groups
        "CREATE TABLE customer_orders (customer_id int, order_id int, amount double, PRIMARY KEY ((customer_id), order_id))"
    )  # => closes the execute() call -- the table now exists with this exact partition layout
    for i in range(500):  # => co-22: 500 rows, 20 distinct partitions -- 25 rows per customer partition
        session.execute(  # => each row lands in the partition matching (i % 20)
            "INSERT INTO customer_orders (customer_id, order_id, amount) VALUES (%s, %s, %s)",  # => positional CQL placeholders
            (i % 20, i, float(i)),  # => customer_id cycles 0-19, spreading rows evenly across all 20 partitions
        )  # => closes this one execute() call -- runs 500 times, once per generated row


def query_one_partition(session: Session, customer_id: int) -> tuple[int, float]:  # => co-22: returns (row count, elapsed seconds)
    """Query rows scoped to exactly one partition key -- a fast, single-partition read."""  # => documents the contract
    start = time.perf_counter()  # => marks the start of the timed, partition-scoped read
    rows = list(
        session.execute(  # => co-22: the partition key (customer_id) is provided -- Cassandra routes DIRECTLY to that partition
            "SELECT order_id, amount FROM customer_orders WHERE customer_id = %s",
            (customer_id,),  # => a single positional placeholder, bound to customer_id
        )
    )  # => materializes the cursor -- exactly this ONE partition's rows, nothing else scanned
    elapsed = time.perf_counter() - start  # => elapsed wall-clock seconds for this single-partition scan
    return len(rows), elapsed  # => hand back both the row count and how long the scan took


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    session = cluster.connect()  # => opens a session against that cluster
    setup_orders_table(session)  # => sets up the 500-row, 20-partition fixture

    row_count, elapsed = query_one_partition(session, customer_id=7)  # => co-22: scoped to EXACTLY one of the 20 partitions
    assert row_count == 25  # => co-22: 500 rows / 20 customers == 25 rows in customer 7's own partition, no more, no less
    print(f"Partition-scoped query for customer_id=7: {row_count} rows in {elapsed * 1000:.2f}ms")  # => Output line -- exact ms machine-dependent
    # => co-22: because customer_id IS the partition key, Cassandra routes this query directly to the
    # => single node/partition owning it -- it never has to fan out and scan every partition, which is
    # => exactly the cost Example 47's missing-partition-key query pays instead
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
