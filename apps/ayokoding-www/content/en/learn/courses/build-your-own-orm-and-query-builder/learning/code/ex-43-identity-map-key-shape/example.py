"""Example 43: Identity Map -- Keyed by (table, pk), Never Conflated Across Tables."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the two loaded domain object types
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => the cache holds objects of more than one type


@dataclasses.dataclass  # => one domain type
class User:  # => rows from "users"
    id: int  # => primary key, same VALUE space as Order.id below
    name: str  # => an ordinary column


@dataclasses.dataclass  # => a second, unrelated domain type
class Order:  # => rows from "orders" -- a DIFFERENT table, same pk VALUE
    id: int  # => primary key -- deliberately the SAME integer as a User's pk
    total: float  # => an ordinary column


class IdentityMap:  # => co-13: keyed by (table, pk), not by pk alone
    def __init__(self) -> None:  # => starts empty
        self._cache: dict[tuple[str, int], Any] = {}  # => the TABLE NAME is part of the key

    def load_user(self, conn: sqlite3.Connection, pk: int) -> User:  # => loads from "users"
        key = ("users", pk)  # => "users" is part of the key, not just the bare pk
        if key in self._cache:  # => hit
            return self._cache[key]  # => same object as any earlier load_user(pk) call
        row = conn.execute("SELECT id, name FROM users WHERE id = ?", (pk,)).fetchone()  # => real query
        user = User(id=row[0], name=row[1])  # => maps the row
        self._cache[key] = user  # => cached under ("users", pk)
        return user  # => a User, never confused with an Order at the same pk

    def load_order(self, conn: sqlite3.Connection, pk: int) -> Order:  # => loads from "orders"
        key = ("orders", pk)  # => "orders" is part of the key -- a DIFFERENT slot even if pk matches
        if key in self._cache:  # => hit
            return self._cache[key]  # => same object as any earlier load_order(pk) call
        row = conn.execute("SELECT id, total FROM orders WHERE id = ?", (pk,)).fetchone()  # => real query
        order = Order(id=row[0], total=row[1])  # => maps the row
        self._cache[key] = order  # => cached under ("orders", pk) -- NOT the same slot as ("users", pk)
        return order  # => an Order, never confused with a User at the same pk


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => first table
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, total REAL)")  # => second table
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")  # => user pk=1
    conn.execute("INSERT INTO orders VALUES (1, 99.5)")  # => order pk=1 -- the SAME integer, on purpose
    conn.commit()  # => makes both seed rows visible
    identity_map = IdentityMap()  # => one shared map across BOTH tables
    user = identity_map.load_user(conn, 1)  # => loads users pk=1
    order = identity_map.load_order(conn, 1)  # => loads orders pk=1 -- same pk value, different table
    assert user is not order  # => co-13: (table, pk) keeps them from being conflated
    print(type(user).__name__, type(order).__name__)  # => Output: User Order
