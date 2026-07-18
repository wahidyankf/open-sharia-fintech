"""Example 13: Combine Two Predicates With OR, Parenthesized."""  # => this concept

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


@dataclasses.dataclass(frozen=True)  # => co-05: an OR node -- ALWAYS self-parenthesizing
class Or:  # => combines left and right, wrapped in parens so precedence is unambiguous
    left: Predicate  # => the first child predicate
    right: Predicate  # => the second child predicate

    def compile(self) -> tuple[str, list[Any]]:  # => params from BOTH children, in order
        left_sql, left_params = self.left.compile()  # => renders the left child first
        right_sql, right_params = self.right.compile()  # => renders the right child second
        sql = f"({left_sql} OR {right_sql})"  # => parens make this safe to nest under AND
        return sql, left_params + right_params  # => left's params THEN right's params


@dataclasses.dataclass(frozen=True, eq=False)  # => eq=False: __eq__ returns a node, not bool
class Col:  # => a lightweight column-name wrapper enabling `col("x") == y` syntax
    name: str  # => the wrapped column name

    def __eq__(self, other: object) -> Eq:  # type: ignore[override]
        # => deliberately violates object.__eq__'s "-> bool" contract: Col is a query-DSL
        # => node, never used as a dict/set key needing real value-equality semantics
        return Eq(column=self.name, value=other)  # => "status" == "open" becomes Eq(...)

    def __hash__(self) -> int:  # => still hashable even though __eq__ no longer returns bool
        return hash(self.name)  # => hashes on the wrapped name, consistent with equality


def col(name: str) -> Col:  # => the public entry point
    return Col(name=name)  # => wraps the bare name


pred = Or(left=col("status") == "open", right=col("status") == "pending")  # => two Eq leaves
sql, params = pred.compile()  # => splits into text + bound values
assert sql == "(status = ? OR status = ?)"  # => parens, exactly one " OR " between leaves
assert params == ["open", "pending"]  # => left's value precedes right's value

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE tickets(id INTEGER PRIMARY KEY, status TEXT)")  # => real table
    conn.execute(  # => three seed rows, two of which match either OR branch
        "INSERT INTO tickets(id, status) VALUES (1, 'open'), (2, 'pending'), (3, 'closed')"
        # => row 3 ('closed') matches neither 'open' nor 'pending'
    )  # => insert executed against the real in-memory database
    conn.commit()  # => makes all three seed rows visible
    sql_full = f"SELECT id FROM tickets WHERE {sql}"  # => embeds the parenthesized OR
    rows = conn.execute(sql_full, params).fetchall()  # => runs the real parameterized SELECT
    print(rows)  # => Output: [(1,), (2,)]
    # => rows 1 and 2 matched EITHER branch; row 3 ('closed') matched neither
