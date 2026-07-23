"""Example 75: Wiring the Full Read Stack -- Builder, Driver, Identity Map, Mapper."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the builder's compiled query AND the mapped, identity-mapped domain object
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => compile()'s params list holds mixed-type bound values


@dataclasses.dataclass(frozen=True)  # => co-08: immutable, fluent -- the SAME Select shape as Example 53
class Select:  # => the query builder layer -- knows NOTHING about connections or domain objects
    table: str  # => FROM target
    where_value: int | None = None  # => optional "id > ?" filter value

    def where_id_gt(self, value: int) -> "Select":  # => a fluent WHERE method, returns a NEW instance
        return dataclasses.replace(self, where_value=value)  # => co-03: never mutates self

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: the ONLY crossing from builder to driver
        sql = f"SELECT id, name FROM {self.table}"  # => base SELECT
        params: list[Any] = []  # => a fresh params list, every call
        if self.where_value is not None:  # => narrows where_value to int
            sql += " WHERE id > ?"  # => appends the filter fragment
            params.append(self.where_value)  # => appends the bound value
        return sql, params  # => the boundary value the driver consumes directly


@dataclasses.dataclass  # => the domain object -- what the caller actually works with, mutable once loaded
class User:  # => the type this whole stack ultimately produces
    id: int  # => primary key
    name: str  # => an ordinary column


class IdentityMap:  # => co-13: sits BETWEEN the driver and the caller -- one object per pk, forever
    def __init__(self, conn: sqlite3.Connection) -> None:  # => co-23: owns the connection this stack shares
        self._conn = conn  # => co-15: the ONE connection every layer below routes through
        self._cache: dict[int, User] = {}  # => co-13: keyed by pk -- caches the FINAL, mapped object

    def select(self, query: Select) -> list[User]:  # => co-08 + co-10 + co-13, composed into ONE call
        sql, params = query.compile()  # => co-08: builder -> driver boundary crossed HERE
        rows = self._conn.execute(sql, params).fetchall()  # => co-23: the actual query, over the shared connection
        results: list[User] = []  # => co-13: accumulates identity-mapped objects, not raw mapped copies
        for row in rows:  # => co-10: maps EVERY returned row, but co-13 gates whether a NEW object is built
            pk = row[0]  # => this row's primary key -- the identity map's cache key
            if pk not in self._cache:  # => co-13: only construct a NEW object on a genuine cache MISS
                self._cache[pk] = User(id=row[0], name=row[1])  # => co-10: mapped ONCE, cached FOREVER after
            results.append(self._cache[pk])  # => co-13: always the SAME object for the SAME pk, every call
        return results  # => a list of identity-mapped, fully-typed domain objects


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => co-23: real local SQLite db, opened once
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "Alice"), (2, "Bob"), (3, "Carol")])  # => 3 rows
    conn.commit()  # => makes all three seed rows visible
    stack = IdentityMap(conn)  # => co-13 + co-15 + co-23: the whole read stack, wired around ONE connection
    first_call = stack.select(Select(table="users").where_id_gt(1))  # => co-08 -> co-23 -> co-10 -> co-13
    second_call = stack.select(Select(table="users"))  # => a DIFFERENT query, but OVERLAPPING pks (2, 3)
    bob_from_first = next(u for u in first_call if u.id == 2)  # => Bob, mapped by the FIRST query
    bob_from_second = next(u for u in second_call if u.id == 2)  # => Bob, mapped by the SECOND, different query
    assert bob_from_first is bob_from_second  # => co-13: the IDENTICAL object -- two queries, one identity
    print(bob_from_first is bob_from_second)  # => Output: True
