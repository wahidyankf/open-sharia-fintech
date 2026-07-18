"""Example 32: Map a fetchall() Result to a List of Objects."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the mapper's target is a plain dataclass
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => a loaded domain object, one per row
class User:  # => the typed object every row gets mapped into
    id: int  # => column 0
    name: str  # => column 1


def row_to_user(row: tuple[int, str]) -> User:  # => co-10: maps ONE row, reused per row below
    return User(id=row[0], name=row[1])  # => assignment by column order


def rows_to_users(rows: list[tuple[int, str]]) -> list[User]:  # => co-10: maps a WHOLE result set
    return [row_to_user(row) for row in rows]  # => reuses the single-row mapper for every row


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.executemany(  # => seeds THREE rows in one call
        "INSERT INTO users(id, name) VALUES (?, ?)",  # => co-02: still parameterized, per row
        [(1, "Alice"), (2, "Bob"), (3, "Carol")],  # => three seed rows, in this exact order
    )  # => executemany() applies the same parameterized statement to each tuple in the list
    conn.commit()  # => makes all three seed rows visible
    raw_rows = conn.execute("SELECT id, name FROM users ORDER BY id").fetchall()  # => list[tuple] from the driver
    users = rows_to_users(raw_rows)  # => THIS is the mapping step -- 3 tuples become 3 Users
    assert len(users) == 3  # => count preserved -- no row silently dropped
    print([u.name for u in users])  # => Output: ['Alice', 'Bob', 'Carol']
