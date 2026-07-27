"""Example 79: Capstone Preview - Wide-Column Feed."""  # => co-22,co-25: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from cassandra.cluster import Cluster, Session  # => co-22: cassandra-driver -- the capstone's own wide.py will build on exactly this


def setup_order_history_table(session: Session) -> None:  # => co-22: the capstone's own time-series/feed access pattern, previewed
    """Create the capstone's own order-history table shape: partition by customer, cluster by order time."""  # => documents the contract
    session.execute(  # => a dedicated keyspace, replication_factor 1 on this single-node local cluster
        "CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = "  # => the keyspace-level replication strategy clause
        "{'class': 'SimpleStrategy', 'replication_factor': 1}"  # => concatenated onto the line above -- ONE CQL statement string
    )  # => closes the execute() call -- the keyspace now exists, idempotently
    session.set_keyspace("nosqldb")  # => selects the keyspace for the statements below
    session.execute("DROP TABLE IF EXISTS capstone_preview_orders")  # => resets state -- this example is fully self-contained
    session.execute(  # => co-22: customer_id partitions, order_time clusters -- exactly the capstone's own feed shape
        "CREATE TABLE capstone_preview_orders ("  # => opens the column-list clause
        "customer_id text, "  # => the partition key column
        "order_time timestamp, "  # => the clustering key column -- orders every row WITHIN a partition
        "amount double, "  # => a plain, non-key column
        "PRIMARY KEY ((customer_id), order_time)"  # => co-22: partition key customer_id, clustering key order_time
        ") WITH CLUSTERING ORDER BY (order_time DESC)"  # => co-22: newest order first -- the capstone's own dominant read
    )  # => closes the execute() call -- the table now exists with this exact partition + clustering + ordering


def insert_orders(session: Session) -> None:  # => co-25: appends -- exactly the write shape an LSM-tree-backed store favors
    """Insert 4 out-of-order orders for one customer -- Cassandra stores them clustering-key-sorted regardless."""  # => documents contract
    orders = [  # => co-22: deliberately out of time order -- clustering order is enforced by the STORE, not insert order
        ("cust-1", "2026-07-27 09:00:00", 20.0),  # => the EARLIEST order chronologically, but inserted FIRST anyway
        ("cust-1", "2026-07-27 09:30:00", 35.5),  # => a LATER order, inserted SECOND -- already out of insert order
        ("cust-1", "2026-07-27 09:15:00", 12.0),  # => an order BETWEEN the two above, inserted THIRD
        ("cust-1", "2026-07-27 09:45:00", 8.25),  # => the LATEST order chronologically, inserted LAST
    ]  # => closes the orders list -- 4 tuples, deliberately scrambled relative to their own order_time
    for customer_id, order_time, amount in orders:  # => co-25: each INSERT is a cheap, sequential append -- an LSM-tree-backed write path
        session.execute(  # => co-22: every row here lands in the SAME partition, cust-1
            "INSERT INTO capstone_preview_orders (customer_id, order_time, amount) VALUES (%s, %s, %s)",  # => positional CQL placeholders
            (customer_id, order_time, amount),  # => binds this one loop iteration's own scrambled-order tuple
        )  # => closes this one execute() call -- runs once per order, in whatever order this loop iterates them


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = Cluster(["127.0.0.1"], port=9042)  # => connects to the local single-node Cassandra 5.0 cluster
    session = cluster.connect()  # => opens a session against that cluster
    setup_order_history_table(session)  # => sets up the capstone's own preview table shape
    insert_orders(session)  # => co-25: inserts 4 out-of-time-order orders, all in the cust-1 partition

    rows = list(session.execute("SELECT order_time, amount FROM capstone_preview_orders WHERE customer_id = %s", ("cust-1",)))  # => co-22: a single-partition scan
    amounts_newest_first = [row.amount for row in rows]  # => extracts amounts in RETURN (clustering) order
    print(f"Order history for cust-1, newest first: {amounts_newest_first}")  # => Output: Order history for cust-1, newest first: [8.25, 35.5, 12.0, 20.0]
    assert amounts_newest_first == [8.25, 35.5, 12.0, 20.0]  # => co-22: clustering-key-ordered (newest order_time first), NOT insert-ordered
    assert len(rows) == 4  # => co-22: all 4 orders landed in the SAME partition, exactly as the schema intended
    print("This partition-scoped, clustering-ordered feed IS the shape the capstone's wide.py will build on")  # => Output line
    cluster.shutdown()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
