"""Example 77: A Fully-Typed End-to-End Path -- Builder to Domain Object, No `Any` Leaks."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the builder's compiled query AND the mapped domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Protocol, Self  # => co-25: the generic bound, the ONLY sanctioned Any usage


class FromRow(Protocol):  # => co-25: the structural bound every T in the typed API below must satisfy
    @classmethod  # => a classmethod, not a plain method -- `cls` is what varies per concrete T
    def from_row(cls, row: tuple[Any, ...]) -> Self: ...  # => the ONE place `Any` appears -- the row's raw shape


@dataclasses.dataclass(frozen=True)  # => co-08: immutable, fluent -- fully typed, no Any anywhere here
class Select:  # => the query builder layer, unchanged in shape from Example 53/75
    table: str  # => FROM target
    where_value: int | None = None  # => optional "id > ?" filter value

    def where_id_gt(self, value: int) -> "Select":  # => a fluent WHERE method, returns a NEW instance
        return dataclasses.replace(self, where_value=value)  # => co-03: never mutates self

    def compile(self) -> tuple[str, list[int]]:  # => co-08: narrower than Example 53 -- only int params here
        sql = f"SELECT * FROM {self.table}"  # => SELECT * -- co-25 needs arbitrary row shapes, not fixed columns
        params: list[int] = []  # => co-08: a fresh, PRECISELY-typed params list, every call
        if self.where_value is not None:  # => narrows where_value to int
            sql += " WHERE id > ?"  # => appends the filter fragment
            params.append(self.where_value)  # => appends the bound value, still an int
        return sql, params  # => the boundary value the driver consumes directly


@dataclasses.dataclass  # => a loaded domain object -- satisfies FromRow structurally, no inheritance needed
class User:  # => the concrete type this example's typed API returns
    id: int  # => primary key
    name: str  # => an ordinary column

    @classmethod  # => satisfies FromRow's classmethod requirement structurally
    def from_row(cls, row: tuple[Any, ...]) -> Self:  # => co-10, expressed as the FromRow contract
        return cls(id=row[0], name=row[1])  # => Self here resolves to User at the call site


def select_typed[T: FromRow](conn: sqlite3.Connection, cls: type[T], query: Select) -> list[T]:  # => co-25
    sql, params = query.compile()  # => co-08: builder -> driver boundary, fully typed on both sides
    rows = conn.execute(sql, params).fetchall()  # => co-23: the real query, params: list[int]
    return [cls.from_row(row) for row in rows]  # => co-25: pyright checks this returns list[T], not list[Any]


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "Alice"), (2, "Bob")])  # => two rows
    conn.commit()  # => makes both seed rows visible
    users: list[User] = select_typed(conn, User, Select(table="users").where_id_gt(0))  # => T inferred as User
    assert all(isinstance(u, User) for u in users)  # => the runtime type matches what pyright inferred
    print([u.name for u in users])  # => Output: ['Alice', 'Bob']
