"""Example 12: Combine Two Predicates With AND."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Protocol  # => Protocol types the shared Predicate interface


class Predicate(Protocol):  # => any node that can compile to (sql, params)
    def compile(self) -> tuple[str, list[Any]]: ...  # => structural contract


@dataclasses.dataclass(frozen=True)  # => a single "column = value" leaf predicate
class Eq:  # => emits "?", value travels in the params list, never inlined
    column: str  # => the column name
    value: Any  # => the bound literal

    def compile(self) -> tuple[str, list[Any]]:  # => satisfies the Predicate protocol
        return f"{self.column} = ?", [self.value]  # => "col = ?", [value]


@dataclasses.dataclass(frozen=True)  # => co-05: an AND node joining two child predicates
class And:  # => combines left and right into one boolean-tree node
    left: Predicate  # => the first child predicate
    right: Predicate  # => the second child predicate

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: params from BOTH children, in order
        left_sql, left_params = self.left.compile()  # => renders the left child first
        right_sql, right_params = self.right.compile()  # => renders the right child second
        sql = f"{left_sql} AND {right_sql}"  # => "a = ? AND b = ?"
        return sql, left_params + right_params  # => left's params THEN right's params


@dataclasses.dataclass(frozen=True, eq=False)  # => eq=False: __eq__ returns a node, not bool
class Col:  # => a lightweight column-name wrapper enabling `col("x") == y` syntax
    name: str  # => the wrapped column name

    def __eq__(self, other: object) -> Eq:  # type: ignore[override]
        # => deliberately violates object.__eq__'s "-> bool" contract: Col is a query-DSL
        # => node, never used as a dict/set key needing real value-equality semantics
        return Eq(column=self.name, value=other)  # => "age" == 30 becomes Eq("age", 30)

    def __hash__(self) -> int:  # => still hashable even though __eq__ no longer returns bool
        return hash(self.name)  # => hashes on the wrapped name, consistent with equality


def col(name: str) -> Col:  # => the public entry point
    return Col(name=name)  # => wraps the bare name


pred = And(left=col("age") == 30, right=col("status") == "open")  # => two Eq leaves, ANDed
sql, params = pred.compile()  # => splits into text + bound values
assert sql == "age = ? AND status = ?"  # => two placeholders, joined by " AND "
assert params == [30, "open"]  # => left's value (30) precedes right's value ("open")

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, age INTEGER, status TEXT)")  # => table
    conn.execute(  # => three seed rows, only one matches BOTH conditions
        "INSERT INTO users(id, age, status) VALUES (1, 30, 'open'), (2, 30, 'closed'), (3, 20, 'open')"
        # => row 1: age=30/open matches; row 2: age=30 but closed; row 3: open but age=20
    )  # => insert executed against the real in-memory database
    conn.commit()  # => makes all three seed rows visible
    rows = conn.execute(f"SELECT id FROM users WHERE {sql}", params).fetchall()  # => real filter
    print(rows)  # => Output: [(1,)]
    # => only row 1 satisfied BOTH age=30 AND status='open' -- AND requires both to hold
