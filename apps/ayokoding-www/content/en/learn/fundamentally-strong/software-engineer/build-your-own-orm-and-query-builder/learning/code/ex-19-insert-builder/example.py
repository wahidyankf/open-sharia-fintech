"""Example 19: insert("users").values(...) Compiles a Parameterized INSERT."""  # => concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => column values can be any Python type SQLite accepts


@dataclasses.dataclass(frozen=True)  # => co-07: the same clause-as-data approach, INSERT-shaped
class Insert:  # => a minimal single-table INSERT builder
    table: str  # => target table
    column_values: dict[str, Any] = dataclasses.field(default_factory=dict[str, Any])  # => col -> value

    def values(self, **kwargs: Any) -> "Insert":  # => sets every column=value pair at once
        return dataclasses.replace(self, column_values={**self.column_values, **kwargs})

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: returns (sql, params) together
        columns = list(self.column_values.keys())  # => column names, dict-insertion order
        placeholders = ", ".join("?" for _ in columns)  # => one "?" per column
        col_list = ", ".join(columns)  # => comma-joined column names
        sql = f"INSERT INTO {self.table} ({col_list}) VALUES ({placeholders})"  # => full SQL
        params = [self.column_values[c] for c in columns]  # => values, in the SAME column order
        return sql, params  # => the compiled (sql, params) pair


def insert(table: str) -> Insert:  # => the public entry point: insert("users")
    return Insert(table=table)  # => an empty INSERT, no columns chosen yet


query = insert("users").values(id=1, name="Alice")  # => two columns, in call order
sql, params = query.compile()  # => splits into text + bound values
assert sql == "INSERT INTO users (id, name) VALUES (?, ?)"  # => two "?" placeholders
assert params == [1, "Alice"]  # => id's value precedes name's value, matching the column list

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.commit()  # => empty table, ready for the parameterized insert
    conn.execute(sql, params)  # => runs the real compiled INSERT against the real table
    conn.commit()  # => makes the inserted row durable/visible
    row = conn.execute("SELECT id, name FROM users").fetchone()  # => real read-back
    print(row)  # => Output: (1, 'Alice')
    # => proves the compiled INSERT actually wrote a row the SELECT can see
