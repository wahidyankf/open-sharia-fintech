"""Example 59: pytest verification for Clean-Object Flush Issuing Zero Writes."""

import contextlib
import sqlite3

from example import UnitOfWork, User


def test_clean_object_produces_zero_updates() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.execute("INSERT INTO users VALUES (1, 'Grace')")  # => one seed row
        conn.commit()  # => makes the seed row visible
        uow = UnitOfWork(conn)
        user = User(id=1, name="Grace")  # => matches the seed row exactly
        uow.track_clean(user)
        uow.flush()
        assert uow.update_count == 0  # => never dirty, never written


def test_dirtying_after_track_clean_does_produce_an_update() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'Bob')")
        conn.commit()
        uow = UnitOfWork(conn)
        user = User(id=1, name="Bob")
        uow.track_clean(user)
        user.name = "Bobby"  # => mutate AFTER tracking -- now dirty
        uow.flush()
        assert uow.update_count == 1  # => exactly one write, for the one dirty object


# => Run: pytest -- Output: 2 passed
