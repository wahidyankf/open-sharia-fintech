"""Example 47: Session begin/write/commit -- the Row Persists After Commit."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


class Session:  # => co-15: owns the connection, demarcates the transaction
    def __init__(self, conn: sqlite3.Connection) -> None:  # => handed one connection, kept for its lifetime
        self._conn = conn  # => the ONE connection this session ever uses

    def execute(self, sql: str, params: tuple[object, ...] = ()) -> sqlite3.Cursor:  # => routes every query
        return self._conn.execute(sql, params)  # => an INSERT/UPDATE/DELETE here implicitly opens a transaction

    def commit(self) -> None:  # => co-15: the session is the ONLY thing that ever calls commit
        self._conn.commit()  # => makes everything since the implicit "begin" durable, together


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => schema setup, outside the session
    conn.commit()  # => the schema itself is committed before the session's own transaction starts
    session = Session(conn)  # => co-15: one session, one transaction boundary
    session.execute("INSERT INTO users VALUES (1, 'Alice')")  # => "begin": the write is pending, not yet durable
    session.commit()  # => "commit": the pending write becomes durable
    row = session.execute("SELECT name FROM users WHERE id = 1").fetchone()  # => reads it back
    assert row is not None and row[0] == "Alice"  # => the row persisted PAST the commit boundary
    print(row[0])  # => Output: Alice
