"""Example 41: Identity Map -- Different Primary Keys Yield Distinct Instances."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the loaded domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a loaded domain object, cached by the identity map below
class User:  # => the type the identity map holds one instance of, per pk
    id: int  # => primary key
    name: str  # => an ordinary column


class IdentityMap:  # => co-13: a per-session {(table, pk): object} cache
    def __init__(self) -> None:  # => starts empty
        self._cache: dict[tuple[str, int], User] = {}  # => keyed by (table, pk)

    def load(self, conn: sqlite3.Connection, pk: int) -> User:  # => cache-aware load
        key = ("users", pk)  # => the identity key for THIS pk
        if key in self._cache:  # => hit -- same object as before
            return self._cache[key]  # => never re-queries for an already-cached key
        row = conn.execute("SELECT id, name FROM users WHERE id = ?", (pk,)).fetchone()  # => real query
        user = User(id=row[0], name=row[1])  # => maps the row
        self._cache[key] = user  # => caches under THIS pk's own key
        return user  # => a fresh object, distinct from every other pk's cached object


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob')")  # => two distinct rows
    conn.commit()  # => makes both seed rows visible
    identity_map = IdentityMap()  # => one identity map for this "session"
    user1 = identity_map.load(conn, 1)  # => loads pk 1
    user2 = identity_map.load(conn, 2)  # => loads pk 2 -- a DIFFERENT key
    assert user1 is not user2  # => two different pks NEVER share a cache slot
    assert user1.name == "Alice" and user2.name == "Bob"  # => each object holds its OWN row's data
    print(user1 is not user2)  # => Output: True
