"""Example 35: Round-Trip an Object Through a Row and Back."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the round-tripped domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass  # => equality compares field values -- exactly what "equals original" needs
class User:  # => the type flowing through object -> row -> object
    id: int  # => column 0
    name: str  # => column 1
    email: str  # => column 2


def user_to_row(user: User) -> tuple[int, str, str]:  # => co-11: object -> row (the forward mapping)
    return (user.id, user.name, user.email)  # => a plain tuple, column order matches the schema


def row_to_user(row: tuple[int, str, str]) -> User:  # => co-10: row -> object (the inverse mapping)
    return User(id=row[0], name=row[1], email=row[2])  # => symmetric with user_to_row's column order


original = User(id=1, name="Alice", email="alice@example.com")  # => the STARTING object

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, email TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (?, ?, ?)", user_to_row(original))  # => object -> row -> INSERT
    conn.commit()  # => makes the round-tripped row visible
    raw_row = conn.execute("SELECT id, name, email FROM users").fetchone()  # => a REAL row from the db
    reloaded = row_to_user(raw_row)  # => row -> object, completing the round trip
    assert reloaded == original  # => co-10 + co-11 together: the loop closes with no data lost
    print(reloaded == original)  # => Output: True
