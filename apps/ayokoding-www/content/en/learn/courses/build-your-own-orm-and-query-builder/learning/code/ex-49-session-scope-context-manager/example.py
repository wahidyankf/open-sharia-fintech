"""Example 49: `with Session() as s:` -- Commit on Clean Exit, Rollback on Exception."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from types import TracebackType  # => the exact type __exit__'s traceback parameter needs


class Session:  # => co-15: the transaction boundary, now expressed as a context manager
    def __init__(self, conn: sqlite3.Connection) -> None:  # => handed one connection
        self._conn = conn  # => the ONE connection this session ever uses

    def execute(self, sql: str, params: tuple[object, ...] = ()) -> sqlite3.Cursor:  # => routes every query
        return self._conn.execute(sql, params)  # => runs against self._conn only

    def __enter__(self) -> "Session":  # => `with Session(conn) as s:` -- s is this same session
        return self  # => no separate setup needed -- the connection was already handed in

    def __exit__(  # => decides commit vs rollback based on HOW the block exited
        self,  # => this session instance
        exc_type: type[BaseException] | None,  # => None on a clean exit, an exception TYPE otherwise
        exc: BaseException | None,  # => the actual exception INSTANCE, or None
        tb: TracebackType | None,  # => its traceback, or None -- unused here, but part of the protocol
    ) -> bool:  # => False means "never swallow the exception"
        if exc_type is None:  # => the block exited CLEANLY -- no exception propagated out of it
            self._conn.commit()  # => co-15: a clean exit commits the pending transaction
        else:  # => the block raised SOMETHING
            self._conn.rollback()  # => co-15: any exception rolls back the pending transaction
        return False  # => re-raise the original exception (if any) -- never hide it


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => schema
    conn.commit()  # => schema committed before any session-scoped transaction

    with Session(conn) as clean_session:  # => a CLEAN block -- expects a commit on exit
        clean_session.execute("INSERT INTO users VALUES (1, 'Alice')")  # => pending write
    row = conn.execute("SELECT name FROM users WHERE id = 1").fetchone()  # => checked AFTER the `with` exits
    assert row is not None and row[0] == "Alice"  # => committed -- the row survived

    try:  # => catches the exception the block below deliberately raises
        with Session(conn) as failing_session:  # => a block that WILL raise -- expects a rollback on exit
            failing_session.execute("INSERT INTO users VALUES (2, 'Bob')")  # => pending write
            raise ValueError("simulated failure")  # => triggers __exit__'s exception branch
    except ValueError:  # => the exception propagates OUT, exactly as __exit__ returning False intends
        pass  # => expected here -- catching it proves __exit__ never silently swallowed it itself
    row = conn.execute("SELECT * FROM users WHERE id = 2").fetchone()  # => checked AFTER the `with` exits
    assert row is None  # => rolled back -- the row never became durable
    print("committed on success, rolled back on exception")  # => Output: committed on success, rolled back on exception
