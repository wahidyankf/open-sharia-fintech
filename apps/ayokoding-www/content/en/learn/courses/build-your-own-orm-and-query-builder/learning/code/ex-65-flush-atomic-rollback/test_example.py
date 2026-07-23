"""Example 65: pytest verification for Flush Atomic Rollback."""

import contextlib
import sqlite3

import pytest

from example import UnitOfWork, User


def test_a_failing_batch_rolls_back_the_successful_writes_too() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT UNIQUE)")  # => real table
        conn.execute("INSERT INTO users VALUES (1, 'Grace')")  # => a pre-existing row
        conn.commit()  # => makes the seed row visible
        uow = UnitOfWork(conn)
        uow.register_new(User(id=None, name="NewOne"))  # => would succeed alone
        uow.register_new(User(id=None, name="Grace"))  # => collides -- forces the batch to fail
        with pytest.raises(sqlite3.IntegrityError):  # => confirms the failure propagates to the caller
            uow.flush()
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 1  # => only the original seed row survives


def test_a_fully_successful_batch_still_commits_normally() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
        conn.commit()
        uow = UnitOfWork(conn)
        uow.register_new(User(id=None, name="A"))  # => no collisions here
        uow.register_new(User(id=None, name="B"))
        uow.flush()  # => succeeds cleanly
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 2  # => both committed


# => Run: pytest -- Output: 2 passed
