"""Example 48: Session begin/write/rollback -- the Row Is Absent After Rollback."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


class Session:  # => co-15: owns the connection, demarcates the transaction
    def __init__(self, conn: sqlite3.Connection) -> None:  # => handed one connection
        self._conn = conn  # => the ONE connection this session ever uses

    def execute(self, sql: str, params: tuple[object, ...] = ()) -> sqlite3.Cursor:  # => routes every query
        return self._conn.execute(sql, params)  # => an INSERT here implicitly opens a transaction

    def rollback(self) -> None:  # => co-15: undoes everything since the implicit "begin"
        self._conn.rollback()  # => the pending write never becomes durable


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => schema setup
    conn.commit()  # => schema committed before the session's own transaction starts
    session = Session(conn)  # => co-15: one session, one transaction boundary
    session.execute("INSERT INTO users VALUES (1, 'Alice')")  # => "begin": pending, visible only in-session
    pending_count = session.execute("SELECT COUNT(*) FROM users").fetchone()[0]  # => visible BEFORE rollback
    assert pending_count == 1  # => the same connection sees its own uncommitted write
    session.rollback()  # => "rollback": undoes the pending write entirely
    row = session.execute("SELECT * FROM users WHERE id = 1").fetchone()  # => reads again, AFTER rollback
    assert row is None  # => the row never became durable -- it is genuinely absent now
    print(row)  # => Output: None
