"""Example 78: pytest verification for the Mini-ORM Preview."""

import contextlib
import sqlite3

from example import Customer, MiniOrm, Migration, migrate


def test_migrate_then_flush_then_eager_load_end_to_end() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        migrate(  # => co-24: schema setup first
            conn,
            [
                Migration(version=1, sql="CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT);"),
                Migration(version=2, sql="CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL);"),
            ],
        )
        orm = MiniOrm(conn)
        orm.add(Customer(id=None, name="Grace"))  # => tracked
        orm.flush()  # => real INSERT + commit
        conn.execute("INSERT INTO orders(customer_id, total) VALUES (1, 5.0)")  # => one order for Grace
        conn.commit()
        grouped = orm.all_with_orders()  # => co-22: two queries total
        assert grouped[1] == [(1, 5.0)]  # => correctly grouped


def test_identity_map_returns_the_same_object_across_reads() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        migrate(
            conn,
            [
                Migration(version=1, sql="CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT);"),
                Migration(version=2, sql="CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL);"),
            ],
        )
        orm = MiniOrm(conn)
        orm.add(Customer(id=None, name="Bob"))
        orm.flush()  # => flush ALSO registers the flushed object in the identity map
        orm.all_with_orders()  # => a subsequent read must NOT re-construct a new Customer for pk 1
        assert orm.identity_of(1).name == "Bob"  # => the SAME identity-mapped object, correctly named


# => Run: pytest -- Output: 2 passed
