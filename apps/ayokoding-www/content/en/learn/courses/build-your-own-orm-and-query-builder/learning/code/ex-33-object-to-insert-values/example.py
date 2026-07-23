"""Example 33: Read an Object's Attributes Into an INSERT-Ready Dict."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain object being mapped back into row shape
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => a column-to-value dict holds mixed value types


@dataclasses.dataclass  # => a loaded (or freshly-built) domain object
class User:  # => the typed object whose attrs become INSERT values
    id: int  # => maps to the "id" column
    name: str  # => maps to the "name" column
    email: str  # => maps to the "email" column


def user_to_insert_values(user: User) -> dict[str, Any]:  # => co-11: object in, row-shaped dict out
    return dataclasses.asdict(user)  # => reads EVERY field back into a column-name-keyed dict


user = User(id=1, name="Alice", email="alice@example.com")  # => a fresh object, not yet in the db
values = user_to_insert_values(user)  # => the inverse of Example 30's tuple-to-object mapping
assert values == {"id": 1, "name": "Alice", "email": "alice@example.com"}  # => matches every column

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, email TEXT)")  # => real table
    cols = ", ".join(values.keys())  # => "id, name, email" -- built from the dict's own keys
    placeholders = ", ".join("?" for _ in values)  # => one "?" per value -- co-02: never interpolated
    conn.execute(f"INSERT INTO users({cols}) VALUES ({placeholders})", list(values.values()))  # => runs it
    conn.commit()  # => makes the inserted row visible
    row = conn.execute("SELECT id, name, email FROM users").fetchone()  # => reads it back to prove it landed
    print(row)  # => Output: (1, 'Alice', 'alice@example.com')
