"""Example 30: Map a Result Tuple to a Typed Object."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the mapper's TARGET is a plain dataclass, not a dict
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => mutable is fine here -- a loaded domain object, not a builder node
class User:  # => the typed domain object rows get mapped INTO
    id: int  # => column 0 of the row tuple
    name: str  # => column 1 of the row tuple
    email: str  # => column 2 of the row tuple


def row_to_user(row: tuple[int, str, str]) -> User:  # => co-10: tuple in, typed object out
    return User(id=row[0], name=row[1], email=row[2])  # => assignment BY COLUMN ORDER, explicitly


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, email TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name, email) VALUES (1, 'Alice', 'alice@example.com')")  # => one row
    conn.commit()  # => makes the seed row visible
    raw_row = conn.execute("SELECT id, name, email FROM users").fetchone()  # => a plain tuple from the driver
    assert raw_row == (1, "Alice", "alice@example.com")  # => confirms the driver's raw shape
    user = row_to_user(raw_row)  # => THIS is the mapping step -- tuple becomes a User
    assert isinstance(user, User)  # => a real typed object now, not a tuple
    print(user)  # => Output: User(id=1, name='Alice', email='alice@example.com')
