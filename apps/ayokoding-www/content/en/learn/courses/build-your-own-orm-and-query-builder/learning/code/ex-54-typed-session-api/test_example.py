"""Example 54: pytest verification for a Generic Typed Session API."""

import contextlib
import sqlite3

from example import Session, User


def test_get_returns_a_correctly_typed_instance() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.execute("INSERT INTO users VALUES (9, 'Grace')")  # => one seed row
        conn.commit()  # => makes the seed row visible
        session = Session(conn)
        user = session.get(User, "users", 9)  # => T inferred as User
        assert isinstance(user, User)  # => runtime confirms the static inference
        assert (user.id, user.name) == (9, "Grace")  # => correct row mapped through from_row


def test_get_works_for_a_second_distinct_type() -> None:
    import dataclasses
    from typing import Any, Self

    @dataclasses.dataclass
    class Tag:  # => a SECOND type satisfying FromRow, proving `get` is genuinely generic
        id: int
        label: str

        @classmethod
        def from_row(cls, row: tuple[Any, ...]) -> Self:
            return cls(id=row[0], label=row[1])

    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE tags(id INTEGER PRIMARY KEY, label TEXT)")  # => a different table
        conn.execute("INSERT INTO tags VALUES (1, 'urgent')")
        conn.commit()
        session = Session(conn)
        tag = session.get(Tag, "tags", 1)  # => T inferred as Tag this time, same `get` method
        assert isinstance(tag, Tag)  # => the SAME generic method, a DIFFERENT inferred T


# => Run: pytest -- Output: 2 passed
