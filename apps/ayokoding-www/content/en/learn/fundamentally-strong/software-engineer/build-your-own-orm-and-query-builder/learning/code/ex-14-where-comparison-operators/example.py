"""Example 14: Lt, Gt, Ne, and In -- Every Comparison Compiles the Same Way."""  # => concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => models every comparison node as a small frozen value
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Protocol  # => Protocol types the shared Predicate interface


class Predicate(Protocol):  # => any node that can compile to (sql, params)
    def compile(self) -> tuple[str, list[Any]]: ...  # => structural contract


@dataclasses.dataclass(frozen=True)  # => "column < value"
class Lt:  # => strictly-less-than leaf predicate
    column: str  # => the column name
    value: Any  # => the bound literal

    def compile(self) -> tuple[str, list[Any]]:  # => satisfies the Predicate protocol
        return f"{self.column} < ?", [self.value]  # => "col < ?", [value]


@dataclasses.dataclass(frozen=True)  # => "column > value"
class Gt:  # => strictly-greater-than leaf predicate
    column: str  # => the column name
    value: Any  # => the bound literal

    def compile(self) -> tuple[str, list[Any]]:  # => satisfies the Predicate protocol
        return f"{self.column} > ?", [self.value]  # => "col > ?", [value]


@dataclasses.dataclass(frozen=True)  # => "column != value"
class Ne:  # => not-equal leaf predicate
    column: str  # => the column name
    value: Any  # => the bound literal

    def compile(self) -> tuple[str, list[Any]]:  # => satisfies the Predicate protocol
        return f"{self.column} != ?", [self.value]  # => "col != ?", [value]


@dataclasses.dataclass(frozen=True)  # => "column IN (?, ?, ...)"
class In:  # => membership leaf predicate over a fixed set of values
    column: str  # => the column name
    values: tuple[Any, ...]  # => every candidate value, in call order

    def compile(self) -> tuple[str, list[Any]]:  # => one "?" per value, comma-joined
        placeholders = ", ".join("?" for _ in self.values)  # => "?, ?, ?" for 3 values
        return f"{self.column} IN ({placeholders})", list(self.values)  # => params = all values


@dataclasses.dataclass(frozen=True)  # => normal auto-generated __eq__/__hash__, untouched here
class Col:  # => one wrapper exposing every comparison as an operator or a method
    name: str  # => the wrapped column name

    def __lt__(self, other: object) -> Lt:  # => co-05: enables `col("age") < 18`
        # => object has no typed __lt__, so this is a fresh method, not an incompatible override
        return Lt(column=self.name, value=other)  # => "age" < 18 becomes Lt("age", 18)

    def __gt__(self, other: object) -> Gt:  # => enables `col("age") > 65`, same non-override case
        return Gt(column=self.name, value=other)  # => "age" > 65 becomes Gt("age", 65)

    def __ne__(self, other: object) -> Ne:  # type: ignore[override]
        # => deliberately violates object.__ne__'s "-> bool" contract: Col is a query-DSL
        # => node, never used as a dict/set key needing real value-equality semantics
        return Ne(column=self.name, value=other)  # => "status" != "closed" becomes Ne(...)

    def in_(self, *values: Any) -> In:  # => `IN` has no Python operator, so this is a method
        return In(column=self.name, values=values)  # => co-05 comparison family, method form


def col(name: str) -> Col:  # => the public entry point
    return Col(name=name)  # => wraps the bare name


checks: list[tuple[Predicate, str, list[Any]]] = [  # => (predicate, expected sql, expected params)
    (col("age") < 18, "age < ?", [18]),  # => Lt
    (col("age") > 65, "age > ?", [65]),  # => Gt
    (  # => Ne -- pyright's default-eq heuristic misreads the custom __ne__ node as
        col("status") != "closed",  # pyright: ignore[reportUnnecessaryComparison]
        "status != ?",  # => "always True", which is wrong here -- suppressed, not a real bug
        ["closed"],  # => the expected single-element params list for this Ne leaf
    ),  # => closes the (predicate, expected_sql, expected_params) tuple for Ne
    (col("id").in_(1, 2, 3), "id IN (?, ?, ?)", [1, 2, 3]),  # => In
]  # => four (predicate, expected_sql, expected_params) tuples, one per comparison kind
for pred, expected_sql, expected_params in checks:  # => walks every comparison once
    sql, params = pred.compile()  # => renders this one predicate
    assert sql == expected_sql  # => the exact SQL fragment matches
    assert params == expected_params  # => the exact params list matches

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, age INTEGER)")  # => real table
    conn.execute("INSERT INTO users(id, age) VALUES (1, 10), (2, 70), (3, 40)")  # => 3 rows
    conn.commit()  # => makes all three seed rows visible
    lt_sql, lt_params = (col("age") < 18).compile()  # => renders the Lt predicate again
    rows = conn.execute(f"SELECT id FROM users WHERE {lt_sql}", lt_params).fetchall()  # => real run
    print(rows)  # => Output: [(1,)]
    # => only row 1 (age=10) is under 18 -- proves Lt bound the real "?" correctly
