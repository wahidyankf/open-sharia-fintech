"""Example 46: The Session Owns One Connection -- Every Query Shares It."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


class Session:  # => co-15: owns exactly ONE connection, for its entire lifetime
    def __init__(self, conn: sqlite3.Connection) -> None:  # => the connection is handed in ONCE
        self._conn = conn  # => the ONE connection this session will ever use

    @property  # => read-only on purpose -- no setter, so this connection can never be swapped after init
    def connection(self) -> sqlite3.Connection:  # => exposes it for observation, never for reassignment
        return self._conn  # => always the SAME object, every time this property is read

    def execute(self, sql: str, params: tuple[object, ...] = ()) -> sqlite3.Cursor:  # => every query goes through here
        return self._conn.execute(sql, params)  # => routes through self._conn -- never opens a second one


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    session = Session(conn)  # => co-15: one session, wrapping this one connection
    session.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => query 1, through the session
    session.execute("INSERT INTO users VALUES (1, 'Alice')")  # => query 2, through the SAME session
    conn.commit()  # => makes the seed row visible
    conn_before = session.connection  # => observed BEFORE the third query
    row = session.execute("SELECT name FROM users WHERE id = 1").fetchone()  # => query 3
    conn_after = session.connection  # => observed AFTER the third query
    assert conn_before is conn_after is conn  # => co-15: the SAME connection, every single query
    print(row[0])  # => Output: Alice
