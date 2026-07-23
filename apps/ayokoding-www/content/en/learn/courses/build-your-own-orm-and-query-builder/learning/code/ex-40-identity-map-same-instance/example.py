"""Example 40: Identity Map -- Loading the Same PK Twice Returns the Same Instance."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the loaded domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a loaded domain object, cached by the identity map below
class User:  # => the type the identity map holds one instance of, per pk
    id: int  # => primary key
    name: str  # => an ordinary column


class IdentityMap:  # => co-13: a per-session {(table, pk): object} cache
    def __init__(self) -> None:  # => starts empty -- nothing cached before any load
        self._cache: dict[tuple[str, int], User] = {}  # => keyed by (table, pk), holds the SAME object

    def load(self, conn: sqlite3.Connection, pk: int) -> User:  # => co-13: cache-aware load
        key = ("users", pk)  # => co-13's key shape: table name plus pk
        if key in self._cache:  # => a CACHE HIT -- no query needed, return the SAME object
            return self._cache[key]  # => identical instance as the first load
        row = conn.execute("SELECT id, name FROM users WHERE id = ?", (pk,)).fetchone()  # => real query
        user = User(id=row[0], name=row[1])  # => maps the row (co-10)
        self._cache[key] = user  # => registers it BEFORE returning -- future loads hit this same object
        return user  # => the freshly-loaded, now-cached object


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")  # => one seed row
    conn.commit()  # => makes the seed row visible
    identity_map = IdentityMap()  # => one identity map for this "session"
    a = identity_map.load(conn, 1)  # => FIRST load of pk 1 -- a real query runs
    b = identity_map.load(conn, 1)  # => SECOND load of the SAME pk -- a cache hit, no query
    assert a is b  # => co-13's core guarantee: the identical object, not two equal copies
    print(a is b)  # => Output: True
