# pyright: strict
"""Capstone: session.py -- co-15: the session owns exactly ONE connection and demarcates
ONE transaction; unit_of_work.py's flush() is the only thing that ever calls commit() or
rollback() on that connection, and only through this session.
"""

import sqlite3
import types

from identity_map import IdentityMap


class Session:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn  # => co-15: the ONE connection this session (and everything below it) shares
        self.identity_map = IdentityMap()  # => co-13: one identity map, lives exactly as long as this session

    def __enter__(self) -> "Session":  # => co-15: `with Session(conn) as s:` -- commit/rollback on exit
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: types.TracebackType | None,
    ) -> None:
        if exc_type is None:  # => co-15: clean exit -- no exception propagated through the `with` block
            self.conn.commit()
        else:  # => co-15: an exception propagated -- roll back instead of leaving a half-applied transaction
            self.conn.rollback()


if __name__ == "__main__":  # => guards against running the demo on `import session`
    import contextlib

    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        with Session(conn) as clean_session:  # => co-15: clean exit below -- COMMITs
            clean_session.conn.execute("INSERT INTO customer(name) VALUES ('Ada')")
        row = conn.execute("SELECT name FROM customer").fetchone()
        print(row)  # => Output: ('Ada',)
        assert row is not None and row[0] == "Ada"  # => co-15: the clean-exit commit made this durable

        try:
            with Session(conn) as failing_session:  # => co-15: an exception below -- ROLLS BACK instead
                failing_session.conn.execute("INSERT INTO customer(name) VALUES ('Bob')")
                raise RuntimeError("simulated failure mid-transaction")
        except RuntimeError:
            pass  # => expected -- the point is to observe what __exit__ did to the connection
        count = conn.execute("SELECT COUNT(*) FROM customer").fetchone()[0]
        print(count)  # => Output: 1
        assert count == 1  # => co-15: still just Ada -- Bob's insert rolled back with the failed session
