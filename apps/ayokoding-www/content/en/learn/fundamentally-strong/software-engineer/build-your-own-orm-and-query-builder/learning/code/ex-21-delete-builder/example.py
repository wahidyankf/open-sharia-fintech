"""Example 21: delete().where() Compiles a Parameterized DELETE."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Protocol  # => Protocol types the shared Predicate interface


class Predicate(Protocol):  # => any node that can compile to (sql, params)
    def compile(self) -> tuple[str, list[Any]]: ...  # => structural contract


@dataclasses.dataclass(frozen=True)  # => a single "column = value" leaf predicate
class Eq:  # => reused verbatim from the WHERE examples -- same shape, same guarantee
    column: str  # => the column name
    value: Any  # => the bound literal

    def compile(self) -> tuple[str, list[Any]]:  # => satisfies the Predicate protocol
        return f"{self.column} = ?", [self.value]  # => "col = ?", [value]


@dataclasses.dataclass(frozen=True)  # => co-07: DELETE reuses the exact same WHERE machinery
class Delete:  # => a minimal single-table DELETE builder
    table: str  # => target table
    where_pred: Predicate | None = None  # => None means "delete every row" -- explicit, not implicit

    def where(self, pred: Predicate) -> "Delete":  # => attaches a WHERE predicate
        return dataclasses.replace(self, where_pred=pred)  # => new instance, self untouched

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: returns (sql, params) together
        sql = f"DELETE FROM {self.table}"  # => base DELETE FROM
        params: list[Any] = []  # => the params list this query will bind
        if self.where_pred is not None:  # => only append WHERE if a predicate was attached
            where_sql, where_params = self.where_pred.compile()  # => delegates to the node
            sql += f" WHERE {where_sql}"  # => "DELETE FROM users WHERE id = ?"
            params = where_params  # => the leaf's params become the query's params
        return sql, params  # => the compiled (sql, params) pair


def delete(table: str) -> Delete:  # => the public entry point: delete("users")
    return Delete(table=table)  # => an empty DELETE, no filter chosen yet


query = delete("users").where(Eq(column="id", value=2))  # => targets exactly user 2
sql, params = query.compile()  # => splits into text + bound values
assert sql == "DELETE FROM users WHERE id = ?"  # => "?" placeholder, never the literal 2
assert params == [2]  # => the id to delete travels only in the params list

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name) VALUES (1, 'Alice'), (2, 'Bob')")  # => 2 rows
    conn.commit()  # => makes both seed rows visible
    conn.execute(sql, params)  # => runs the real compiled DELETE against the real table
    conn.commit()  # => makes the deletion durable/visible
    rows = conn.execute("SELECT id, name FROM users").fetchall()  # => real read-back
    print(rows)  # => Output: [(1, 'Alice')]
    # => only Bob (id=2) was deleted -- proves WHERE scoped the DELETE to exactly that row
