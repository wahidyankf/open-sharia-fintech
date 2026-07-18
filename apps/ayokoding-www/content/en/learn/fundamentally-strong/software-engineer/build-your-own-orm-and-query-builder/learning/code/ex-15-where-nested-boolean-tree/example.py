"""Example 15: Nest And Inside Or Inside And -- a Real Boolean Tree."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => models every boolean-tree node as a small frozen value
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Protocol  # => Protocol types the shared Predicate interface


class Predicate(Protocol):  # => any node -- leaf or combinator -- that compiles to (sql, params)
    def compile(self) -> tuple[str, list[Any]]: ...  # => structural contract, recursive by nature


@dataclasses.dataclass(frozen=True)  # => a single "column = value" leaf predicate
class Eq:  # => the tree's leaves are always Eq nodes in this example
    column: str  # => the column name
    value: Any  # => the bound literal

    def compile(self) -> tuple[str, list[Any]]:  # => satisfies the Predicate protocol
        return f"{self.column} = ?", [self.value]  # => "col = ?", [value]


@dataclasses.dataclass(frozen=True)  # => co-05: AND does NOT add its own parens
class And:  # => a top-level AND reads fine without extra parens around it
    left: Predicate  # => left child -- may itself be a leaf OR another combinator
    right: Predicate  # => right child -- same recursive shape

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: recurses into BOTH children
        left_sql, left_params = self.left.compile()  # => left child compiles itself, recursively
        right_sql, right_params = self.right.compile()  # => right child compiles itself, recursively
        return f"{left_sql} AND {right_sql}", left_params + right_params  # => concatenated params


@dataclasses.dataclass(frozen=True)  # => OR ALWAYS parenthesizes -- required under a parent AND
class Or:  # => without these parens, SQL's OR-binds-looser-than-AND would change the meaning
    left: Predicate  # => left child
    right: Predicate  # => right child

    def compile(self) -> tuple[str, list[Any]]:  # => recurses into BOTH children, self-wraps
        left_sql, left_params = self.left.compile()  # => left child compiles itself, recursively
        right_sql, right_params = self.right.compile()  # => right child compiles itself, recursively
        sql = f"({left_sql} OR {right_sql})"  # => the parens are the whole point of this example
        return sql, left_params + right_params  # => concatenated params, left-to-right


def col(name: str) -> "Col":  # => the public entry point
    return Col(name=name)  # => wraps the bare name


@dataclasses.dataclass(frozen=True, eq=False)  # => eq=False: __eq__ returns a node, not bool
class Col:  # => a lightweight column-name wrapper enabling `col("x") == y` syntax
    name: str  # => the wrapped column name

    def __eq__(self, other: object) -> Eq:  # type: ignore[override]
        # => deliberately violates object.__eq__'s "-> bool" contract for this query DSL
        return Eq(column=self.name, value=other)  # => "region" == "west" becomes Eq(...)

    def __hash__(self) -> int:  # => still hashable even though __eq__ no longer returns bool
        return hash(self.name)  # => hashes on the wrapped name, consistent with equality


tree = And(  # => "region = ? AND (status = ? OR status = ?)" -- a AND (b OR c) in tree form
    left=col("region") == "west",  # => leaf a
    right=Or(left=col("status") == "open", right=col("status") == "pending"),  # => (b OR c)
)  # => the whole tree is ONE immutable value, built in one expression
sql, params = tree.compile()  # => a SINGLE recursive walk compiles the whole tree
assert sql == "region = ? AND (status = ? OR status = ?)"  # => AND unwrapped, OR parenthesized
assert params == ["west", "open", "pending"]  # => depth-first, left-to-right param order

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE tickets(id INTEGER PRIMARY KEY, region TEXT, status TEXT)")  # => table
    conn.execute(  # => four seed rows exercising every branch of the tree
        "INSERT INTO tickets(id, region, status) VALUES "  # => column list, VALUES keyword
        "(1, 'west', 'open'), (2, 'west', 'pending'), (3, 'west', 'closed'), (4, 'east', 'open')"
        # => rows 1-2 satisfy the whole tree; row 3 fails the OR; row 4 fails the region AND arm
    )
    conn.commit()  # => makes all four seed rows visible
    rows = conn.execute(f"SELECT id FROM tickets WHERE {sql}", params).fetchall()  # => real filter
    print(rows)  # => Output: [(1,), (2,)]
    # => rows 1-2 matched region=west AND (status IN open/pending); 3 and 4 each fail one arm
