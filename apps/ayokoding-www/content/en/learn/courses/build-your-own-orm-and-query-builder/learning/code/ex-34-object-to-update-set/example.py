"""Example 34: Build an UPDATE SET Dict From an Object, Excluding the PK."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain object being mapped back into row shape
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => a column-to-value dict holds mixed value types


@dataclasses.dataclass  # => a loaded domain object with a changed non-pk field
class User:  # => the typed object whose non-pk attrs become UPDATE SET values
    id: int  # => the PRIMARY KEY -- never belongs in a SET clause
    name: str  # => an ordinary, updatable column
    email: str  # => an ordinary, updatable column


def user_to_update_set(user: User, primary_key: str = "id") -> dict[str, Any]:  # => co-11, PK-aware
    all_values = dataclasses.asdict(user)  # => every field, pk included
    return {col: val for col, val in all_values.items() if col != primary_key}  # => drop ONLY the pk


user = User(id=7, name="Grace", email="grace-new@example.com")  # => an object with a changed email
set_values = user_to_update_set(user)  # => co-11: the SET dict for an UPDATE ... WHERE id = 7
assert set_values == {"name": "Grace", "email": "grace-new@example.com"}  # => "id" is NOT present
assert "id" not in set_values  # => explicit: the pk never appears on the SET side of an UPDATE

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, email TEXT)")  # => real table
    conn.execute("INSERT INTO users VALUES (7, 'Grace', 'grace@example.com')")  # => the row BEFORE update
    conn.commit()  # => makes the seed row visible
    set_clause = ", ".join(f"{col} = ?" for col in set_values)  # => "name = ?, email = ?"
    sql = f"UPDATE users SET {set_clause} WHERE id = ?"  # => WHERE targets the pk directly, by value
    conn.execute(sql, [*set_values.values(), user.id])  # => co-02: params, never interpolated
    conn.commit()  # => makes the update visible
    row = conn.execute("SELECT id, name, email FROM users WHERE id = 7").fetchone()  # => reads it back
    print(row)  # => Output: (7, 'Grace', 'grace-new@example.com')
