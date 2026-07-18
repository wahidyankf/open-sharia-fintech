"""Example 53: Compose a Builder Query, Execute It, Map Every Row to a Typed Object."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the builder's compiled query AND the mapped domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => compile()'s params list holds mixed-type bound values


@dataclasses.dataclass(frozen=True)  # => co-03: immutable, fluent
class Select:  # => a minimal SELECT builder -- just enough to compose with the mapper below
    table: str  # => FROM target
    where_value: int | None = None  # => optional "id > ?" filter value

    def where_id_gt(self, value: int) -> "Select":  # => a fluent WHERE method, returns a NEW instance
        return dataclasses.replace(self, where_value=value)  # => co-03: never mutates self

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: the builder/driver boundary
        sql = f"SELECT id, name FROM {self.table}"  # => base SELECT
        params: list[Any] = []  # => co-08: a fresh params list, every call
        if self.where_value is not None:  # => narrows where_value to int
            sql += " WHERE id > ?"  # => appends the filter fragment
            params.append(self.where_value)  # => appends the bound value
        return sql, params  # => the boundary value the driver consumes directly


@dataclasses.dataclass  # => a loaded domain object
class User:  # => the type every mapped row becomes
    id: int  # => column 0
    name: str  # => column 1


def row_to_user(row: tuple[int, str]) -> User:  # => co-10: tuple in, typed object out
    return User(id=row[0], name=row[1])  # => assignment by column order


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "Alice"), (2, "Bob"), (3, "Carol")])  # => 3 rows
    conn.commit()  # => makes all three seed rows visible
    query = Select(table="users").where_id_gt(1)  # => co-03 + co-04: composed fluently
    sql, params = query.compile()  # => co-08: the ONE crossing from builder to driver
    raw_rows = conn.execute(sql, params).fetchall()  # => the driver runs it, params bound safely (co-02)
    users = [row_to_user(row) for row in raw_rows]  # => co-10: every returned row becomes a typed User
    assert all(isinstance(u, User) for u in users)  # => a list of REAL User objects, not raw tuples
    print([u.name for u in users])  # => Output: ['Bob', 'Carol']
