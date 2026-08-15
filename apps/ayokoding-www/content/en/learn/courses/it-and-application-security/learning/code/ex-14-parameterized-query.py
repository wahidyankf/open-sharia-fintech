"""Example 14: binding a value keeps input separate from SQLite syntax."""

from __future__ import (
    annotations,
)  # => Stable annotations on supported Python versions.

import sqlite3  # => Local in-memory database; no service or real records are contacted.


def find_account(
    candidate: str,
) -> list[str]:  # => Candidate is untrusted data, never query text.
    connection = sqlite3.connect(
        ":memory:"
    )  # => Fresh disposable database for each run.
    connection.execute(
        "create table accounts (name text)"
    )  # => Fixed schema is trusted program text.
    connection.execute(
        "insert into accounts values (?)", ("ada",)
    )  # => Bound value remains data.
    rows = connection.execute(
        "select name from accounts where name = ?", (candidate,)
    )  # => `?` binds candidate.
    return [
        row[0] for row in rows
    ]  # => Returns only exact data matches, including for punctuation.


if (
    __name__ == "__main__"
):  # => Lets the example run directly without import side effects.
    print(find_account("ada"))  # => Expected: ['ada'] for an existing account.
    print(
        find_account("' OR '1'='1")
    )  # => Expected: [] because punctuation stays data.
