"""Example 22: compile() Always Returns a (sql, params) Tuple."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any, Protocol  # => Protocol types the shared Predicate interface


class Predicate(Protocol):  # => any node that can compile to (sql, params)
    def compile(self) -> tuple[str, list[Any]]: ...  # => structural contract


@dataclasses.dataclass(frozen=True)  # => a single "column = value" leaf predicate
class Eq:  # => reused from earlier WHERE examples -- same shape, same guarantee
    column: str  # => the column name
    value: Any  # => the bound literal

    def compile(self) -> tuple[str, list[Any]]:  # => satisfies the Predicate protocol
        return f"{self.column} = ?", [self.value]  # => "col = ?", [value]


@dataclasses.dataclass(frozen=True)  # => co-03: immutable, every step is a fluent chain link
class Select:  # => a fuller SELECT: columns, WHERE, and LIMIT all feed one compile() call
    table: str  # => FROM target
    where_pred: Predicate | None = None  # => optional WHERE
    limit_val: int | None = None  # => optional LIMIT

    def where(self, pred: Predicate) -> "Select":  # => attaches a predicate, immutably
        return dataclasses.replace(self, where_pred=pred)  # => new instance, self untouched

    def limit(self, n: int) -> "Select":  # => sets the row cap, immutably
        return dataclasses.replace(self, limit_val=n)  # => new instance, self untouched

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: the SINGLE boundary to the driver
        sql = f"SELECT * FROM {self.table}"  # => base SELECT
        params: list[Any] = []  # => accumulates every bound value, in clause order
        if self.where_pred is not None:  # => only append WHERE if a predicate was attached
            where_sql, where_params = self.where_pred.compile()  # => delegates to the node
            sql += f" WHERE {where_sql}"  # => appends the WHERE fragment
            params += where_params  # => WHERE's params join the accumulator
        if self.limit_val is not None:  # => only append LIMIT if one was set
            sql += " LIMIT ?"  # => "?" placeholder, never the literal number
            params.append(self.limit_val)  # => LIMIT's value joins the accumulator LAST
        return sql, params  # => co-08: ALWAYS a 2-tuple, regardless of which clauses were used


result = Select(table="users").where(Eq(column="age", value=30)).limit(5).compile()  # => a full chain
assert isinstance(result, tuple)  # => compile() genuinely returns a tuple, not a custom object
assert len(result) == 2  # => exactly two elements, always -- sql first, params second
sql, params = result  # => unpacking works because it IS a plain 2-tuple
assert isinstance(sql, str)  # => the first element is always a str
assert isinstance(params, list)  # => the second element is always a list
assert sql == "SELECT * FROM users WHERE age = ? LIMIT ?"  # => both clauses present
assert params == [30, 5]  # => WHERE's value first, LIMIT's value second -- clause order

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, age INTEGER)")  # => real table
    for n in range(1, 11):  # => seeds 10 rows, all with age=30
        conn.execute("INSERT INTO users(id, age) VALUES (?, 30)", [n])  # => one row per id
    conn.commit()  # => makes all 10 seed rows visible
    rows = conn.execute(sql, params).fetchall()  # => runs the real compiled tuple directly
    print(len(rows))  # => Output: 5
    # => 10 matching rows exist, but LIMIT 5 capped the real result to exactly 5
