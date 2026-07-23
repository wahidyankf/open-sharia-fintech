"""Example 11: col("age") == 30 Compiles to a Parameterized Equality."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Protocol  # => Protocol types the shared Predicate interface


class Predicate(Protocol):  # => co-05: any node that can compile to (sql, params)
    def compile(self) -> tuple[str, list[Any]]: ...  # => structural contract, no base class needed


@dataclasses.dataclass(frozen=True)  # => a single "column = value" leaf predicate
class Eq:  # => co-02: emits "?", value travels in the params list, never inlined
    column: str  # => the column name, e.g. "age"
    value: Any  # => the bound literal, e.g. 30

    def compile(self) -> tuple[str, list[Any]]:  # => satisfies the Predicate protocol
        return f"{self.column} = ?", [self.value]  # => "age = ?", [30]


@dataclasses.dataclass(frozen=True, eq=False)  # => eq=False: __eq__ below returns a node, not bool
class Col:  # => a lightweight column-name wrapper enabling `col("age") == 30` syntax
    name: str  # => the wrapped column name

    def __eq__(self, other: object) -> Eq:  # type: ignore[override]
        # => deliberately violates object.__eq__'s "-> bool" contract: Col is a query-DSL
        # => node, never used as a dict/set key needing real value-equality semantics
        return Eq(column=self.name, value=other)  # => "age" == 30 becomes Eq("age", 30)

    def __hash__(self) -> int:  # => still hashable even though __eq__ no longer returns bool
        return hash(self.name)


def col(name: str) -> Col:  # => the public entry point: col("age")
    return Col(name=name)  # => wraps the bare name


@dataclasses.dataclass(frozen=True)  # => co-03: immutable, WHERE now stored as a Predicate
class Select:  # => a minimal single-table SELECT with exactly one WHERE slot
    table: str  # => FROM target
    where_pred: Predicate | None = None  # => None means "no filter"

    def where(self, pred: Predicate) -> "Select":  # => attaches a predicate, immutably
        return dataclasses.replace(self, where_pred=pred)  # => new instance, self untouched

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: returns (sql, params) together
        sql = f"SELECT * FROM {self.table}"  # => base SELECT
        params: list[Any] = []  # => the params list this query will bind
        if self.where_pred is not None:  # => only append WHERE if a predicate was attached
            where_sql, where_params = self.where_pred.compile()  # => delegates to the node
            sql += f" WHERE {where_sql}"  # => "SELECT * FROM users WHERE age = ?"
            params = where_params  # => the leaf's params become the query's params
        return sql, params  # => the compiled (sql, params) pair


query = Select(table="users").where(col("age") == 30)  # => WHERE age = 30, via ==
sql, params = query.compile()  # => splits into text + bound values
assert sql == "SELECT * FROM users WHERE age = ?"  # => "?" placeholder, never "30" inline
assert params == [30]  # => the literal 30 travels only in the params list

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, age INTEGER)")  # => real table
    conn.execute("INSERT INTO users(id, age) VALUES (1, 30), (2, 40)")  # => two seed rows
    conn.commit()  # => makes both seed rows visible
    rows = conn.execute(sql, params).fetchall()  # => runs the parameterized SELECT for real
    print(rows)  # => Output: [(1, 30)]
    # => only the age=30 row matched -- proves the "?" bound to 30, not 40
