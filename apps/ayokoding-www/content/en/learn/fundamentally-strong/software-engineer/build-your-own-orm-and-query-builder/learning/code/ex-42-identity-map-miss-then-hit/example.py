"""Example 42: Identity Map -- a Miss Then a Hit Issues Exactly One Query."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the loaded domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a loaded domain object
class User:  # => cached by pk in the identity map below
    id: int  # => primary key
    name: str  # => an ordinary column


class IdentityMap:  # => co-13, instrumented to COUNT real queries for this example
    def __init__(self) -> None:  # => starts empty, zero queries issued so far
        self._cache: dict[tuple[str, int], User] = {}  # => keyed by (table, pk)
        self.query_count = 0  # => co-13: proves a cache HIT issues no additional query

    def load(self, conn: sqlite3.Connection, pk: int) -> User:  # => cache-aware, counted load
        key = ("users", pk)  # => this pk's identity key
        if key in self._cache:  # => a HIT -- return immediately, query_count untouched
            return self._cache[key]  # => no query below runs on this path
        self.query_count += 1  # => a MISS -- about to issue a real query, count it
        row = conn.execute("SELECT id, name FROM users WHERE id = ?", (pk,)).fetchone()  # => the real query
        user = User(id=row[0], name=row[1])  # => maps the row
        self._cache[key] = user  # => caches it so the NEXT load of this pk is a hit
        return user  # => the newly-loaded, now-counted, now-cached object


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")  # => one seed row
    conn.commit()  # => makes the seed row visible
    identity_map = IdentityMap()  # => a fresh, instrumented map
    identity_map.load(conn, 1)  # => FIRST load -- a miss, issues one real query
    assert identity_map.query_count == 1  # => confirms exactly one query so far
    identity_map.load(conn, 1)  # => SECOND load, same pk -- a hit, issues NO query
    assert identity_map.query_count == 1  # => still exactly one -- the hit added nothing
    print(identity_map.query_count)  # => Output: 1
