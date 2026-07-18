"""Example 77: pytest verification for the Fully-Typed End-to-End Path."""

import contextlib
import sqlite3

from example import Select, User, select_typed


def test_select_typed_returns_a_list_of_the_requested_type() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.execute("INSERT INTO users VALUES (9, 'Grace')")  # => one seed row
        conn.commit()  # => makes the seed row visible
        results = select_typed(conn, User, Select(table="users"))  # => T inferred as User
        assert results == [User(id=9, name="Grace")]  # => correctly mapped through from_row


def test_select_typed_works_for_a_second_distinct_type() -> None:
    import dataclasses
    from typing import Any, Self

    @dataclasses.dataclass
    class Tag:  # => a SECOND type satisfying FromRow, proving select_typed is genuinely generic
        id: int
        label: str

        @classmethod
        def from_row(cls, row: tuple[Any, ...]) -> Self:
            return cls(id=row[0], label=row[1])

    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE tags(id INTEGER PRIMARY KEY, label TEXT)")  # => a different table
        conn.execute("INSERT INTO tags VALUES (1, 'urgent')")
        conn.commit()
        results = select_typed(conn, Tag, Select(table="tags"))  # => T inferred as Tag this time
        assert results == [Tag(id=1, label="urgent")]  # => the SAME function, a DIFFERENT inferred T


# => Run: pytest -- Output: 2 passed
