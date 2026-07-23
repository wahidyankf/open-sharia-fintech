"""Example 20: update().set().where() Compiles a Parameterized UPDATE."""  # => this concept

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


@dataclasses.dataclass(frozen=True)  # => co-07: SET and WHERE are both parameterized
class Update:  # => a minimal single-table UPDATE builder
    table: str  # => target table
    set_values: dict[str, Any] = dataclasses.field(default_factory=dict[str, Any])  # => col -> new value
    where_pred: Predicate | None = None  # => None means "update every row" -- dangerous, explicit

    def set(self, **kwargs: Any) -> "Update":  # => merges new column=value pairs
        return dataclasses.replace(self, set_values={**self.set_values, **kwargs})

    def where(self, pred: Predicate) -> "Update":  # => attaches a WHERE predicate
        return dataclasses.replace(self, where_pred=pred)  # => new instance, self untouched

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: SET params THEN WHERE params
        columns = list(self.set_values.keys())  # => columns being updated, in call order
        assignments = ", ".join(f"{c} = ?" for c in columns)  # => "name = ?, age = ?"
        sql = f"UPDATE {self.table} SET {assignments}"  # => base UPDATE ... SET ...
        params = [self.set_values[c] for c in columns]  # => SET values, matching column order
        if self.where_pred is not None:  # => only append WHERE if a predicate was attached
            where_sql, where_params = self.where_pred.compile()  # => delegates to the node
            sql += f" WHERE {where_sql}"  # => "UPDATE ... SET ... WHERE id = ?"
            params = params + where_params  # => SET params FIRST, then WHERE params
        return sql, params  # => the compiled (sql, params) pair


def update(table: str) -> Update:  # => the public entry point: update("users")
    return Update(table=table)  # => an empty UPDATE, no assignments chosen yet


query = update("users").set(name="Alicia").where(Eq(column="id", value=1))  # => rename user 1
sql, params = query.compile()  # => splits into text + bound values
assert sql == "UPDATE users SET name = ? WHERE id = ?"  # => SET clause, then WHERE clause
assert params == ["Alicia", 1]  # => SET's value FIRST, WHERE's value SECOND -- matches SQL order

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name) VALUES (1, 'Alice'), (2, 'Bob')")  # => 2 rows
    conn.commit()  # => makes both seed rows visible
    conn.execute(sql, params)  # => runs the real compiled UPDATE against the real table
    conn.commit()  # => makes the update durable/visible
    rows = conn.execute("SELECT id, name FROM users ORDER BY id").fetchall()  # => real read-back
    print(rows)  # => Output: [(1, 'Alicia'), (2, 'Bob')]
    # => only row 1 was renamed -- proves WHERE scoped the UPDATE to exactly that row
