"""Capstone Step 3: wide.py -- an order-history feed, partitioned by customer (co-22, co-25).

Builds directly on Example 79's own preview shape: customer_id partitions, order_time
clusters DESC, so "this customer's history, newest first" is a single-partition, already-sorted
scan -- the canonical Cassandra access pattern for any per-entity timeline. This module adds a
SECOND customer to prove partition isolation: cust-2's own history never leaks into cust-1's read.
"""

from __future__ import annotations

from cassandra.cluster import Cluster, Session  # => the Apache Software Foundation-maintained Python driver (Apache-2.0, co-28)

TABLE_NAME = "capstone_orders"


def setup_order_history_table(session: Session) -> None:
    """Create the order-history table: partition by customer, cluster by order time, newest first."""
    session.execute("CREATE KEYSPACE IF NOT EXISTS nosqldb WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}")
    session.set_keyspace("nosqldb")
    session.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")  # => resets state -- this script is fully self-contained
    session.execute(
        f"CREATE TABLE {TABLE_NAME} (customer_id text, order_time timestamp, amount double, PRIMARY KEY ((customer_id), order_time)) WITH CLUSTERING ORDER BY (order_time DESC)"  # => newest order first -- the dominant read this table serves
    )


def insert_order(session: Session, customer_id: str, order_time: str, amount: float) -> None:
    """Append one order -- a cheap, sequential write, exactly the shape an LSM-tree-backed store favors."""
    session.execute(
        f"INSERT INTO {TABLE_NAME} (customer_id, order_time, amount) VALUES (%s, %s, %s)",
        (customer_id, order_time, amount),
    )


def fetch_order_history(session: Session, customer_id: str) -> list[float]:
    """A single-partition scan, already clustering-ordered (newest order_time first)."""
    rows = list(session.execute(f"SELECT order_time, amount FROM {TABLE_NAME} WHERE customer_id = %s", (customer_id,)))
    return [row.amount for row in rows]  # => extracts amounts in RETURN (clustering) order


def main() -> None:
    """Seed two customers' out-of-order orders, then verify each partition reads back correctly isolated."""
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect()
    setup_order_history_table(session)

    cust_1_orders = [  # => deliberately out of time order -- clustering order is enforced by the STORE
        ("cust-1", "2026-07-27 09:00:00", 20.0),
        ("cust-1", "2026-07-27 09:30:00", 35.5),
        ("cust-1", "2026-07-27 09:15:00", 12.0),
        ("cust-1", "2026-07-27 09:45:00", 8.25),
    ]
    cust_2_orders = [  # => a SECOND customer -- a DIFFERENT partition, to prove isolation below
        ("cust-2", "2026-07-27 10:00:00", 50.0),
        ("cust-2", "2026-07-27 10:10:00", 15.0),
    ]
    for customer_id, order_time, amount in cust_1_orders + cust_2_orders:
        insert_order(session, customer_id, order_time, amount)

    cust_1_history = fetch_order_history(session, "cust-1")
    assert cust_1_history == [8.25, 35.5, 12.0, 20.0]  # => clustering-ordered (newest first), NOT insert-ordered
    print(f"cust-1 order history, newest first: {cust_1_history}")

    cust_2_history = fetch_order_history(session, "cust-2")
    assert cust_2_history == [15.0, 50.0]  # => cust-2's OWN partition, newest first
    print(f"cust-2 order history, newest first: {cust_2_history}")

    assert set(cust_1_history).isdisjoint(cust_2_history)  # => partition isolation: no amount leaked across partitions
    print("wide.py: both customer partitions return correctly-ordered, correctly-isolated history -- PASSED")
    cluster.shutdown()


if __name__ == "__main__":
    main()
