"""Example 31: Map a Dict Row to a Typed Object by Column Name."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the mapper's target is still a plain dataclass
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => a driver-produced dict row's values are dynamically typed


@dataclasses.dataclass  # => mutable, a loaded domain object
class User:  # => the typed domain object rows get mapped INTO
    id: int  # => must come from the "id" key, not position 0
    name: str  # => must come from the "name" key
    email: str  # => must come from the "email" key


def row_to_user(row: dict[str, Any]) -> User:  # => co-10: dict in, typed object out, BY NAME
    return User(id=row["id"], name=row["name"], email=row["email"])  # => key lookups, not positions


def dict_row_factory(cursor: sqlite3.Cursor, row: tuple[Any, ...]) -> dict[str, Any]:  # => turns tuples to dicts
    columns = [d[0] for d in cursor.description]  # => cursor.description names each column, in order
    return dict(zip(columns, row, strict=True))  # => zips column names to this row's values


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.row_factory = dict_row_factory  # => every fetch below now returns a dict, not a tuple
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, email TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name, email) VALUES (1, 'Alice', 'alice@example.com')")  # => one row
    conn.commit()  # => makes the seed row visible
    dict_row = conn.execute("SELECT email, id, name FROM users").fetchone()  # => columns SELECTED out of order
    assert dict_row == {"email": "alice@example.com", "id": 1, "name": "Alice"}  # => a real dict, not a tuple
    user = row_to_user(dict_row)  # => mapping is BY KEY, so column order in the SELECT never matters
    print(user)  # => Output: User(id=1, name='Alice', email='alice@example.com')
