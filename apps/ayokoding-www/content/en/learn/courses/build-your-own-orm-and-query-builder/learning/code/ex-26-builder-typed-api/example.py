"""Example 26: A Fully Type-Annotated Builder Chain, pyright --strict Clean."""  # => concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => bound values can be any Python type SQLite accepts


@dataclasses.dataclass(frozen=True)  # => co-25: EVERY field and method below is explicitly typed
class Select:  # => a small SELECT builder used purely to demonstrate a typed fluent chain
    table: str  # => FROM target -- typed str, never Any
    columns: tuple[str, ...] = ()  # => typed tuple[str, ...], never a bare list
    where_value: int | None = None  # => typed int | None -- the exact union pyright checks

    def select(self, *cols: str) -> "Select":  # => co-25: explicit *cols: str, explicit -> "Select"
        return dataclasses.replace(self, columns=cols)  # => return type matches the annotation

    def where_id(self, value: int) -> "Select":  # => explicit int parameter, explicit -> "Select"
        return dataclasses.replace(self, where_value=value)  # => pyright checks this call site too

    def compile(self) -> tuple[str, list[Any]]:  # => explicit -> tuple[str, list[Any]], not "Any"
        col_list = ", ".join(self.columns) if self.columns else "*"  # => str, inferred correctly
        sql = f"SELECT {col_list} FROM {self.table}"  # => sql: str, inferred from f-string
        params: list[Any] = []  # => explicit list[Any] -- the ONE deliberately loose type here
        if self.where_value is not None:  # => narrows where_value from int | None to int
            sql += " WHERE id = ?"  # => appends the filter fragment
            params.append(self.where_value)  # => appends the NARROWED int, not int | None
        return sql, params  # => matches the declared return type exactly


# => a real fluent chain -- pyright must resolve EVERY intermediate type correctly, in order
chain: Select = (
    Select(table="users")  # => Select
    .select("id", "name")  # => still Select -- pyright checks .select()'s return type here
    .where_id(7)  # => still Select -- pyright checks .where_id()'s param AND return type here
)
sql, params = chain.compile()  # => pyright checks compile()'s declared tuple[str, list[Any]]
assert sql == "SELECT id, name FROM users WHERE id = ?"  # => the chain compiled correctly
assert params == [7]  # => the narrowed int made it into the params list, still typed list[Any]

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name) VALUES (7, 'Grace')")  # => one seed row
    conn.commit()  # => makes the seed row visible
    row = conn.execute(sql, params).fetchone()  # => runs the fully-typed chain's real output
    print(row)  # => Output: (7, 'Grace')
    # => the typed chain compiled to real, correct, executable SQL -- types never lied
