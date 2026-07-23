"""Example 18: LIMIT and OFFSET Are Parameterized Trailing Clauses."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => the params list holds LIMIT/OFFSET's bound integer values


@dataclasses.dataclass(frozen=True)  # => co-06: LIMIT/OFFSET are themselves bound, not inlined
class Select:  # => a minimal single-table SELECT with pagination
    table: str  # => FROM target
    limit_val: int | None = None  # => None means "no LIMIT clause at all"
    offset_val: int | None = None  # => None means "no OFFSET clause at all"

    def limit(self, n: int) -> "Select":  # => sets the row cap, immutably
        return dataclasses.replace(self, limit_val=n)  # => new instance, self untouched

    def offset(self, n: int) -> "Select":  # => sets the row skip, immutably
        return dataclasses.replace(self, offset_val=n)  # => new instance, self untouched

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: LIMIT/OFFSET bind as "?", not literals
        sql = f"SELECT * FROM {self.table}"  # => base SELECT
        params: list[Any] = []  # => the params list this query will bind
        if self.limit_val is not None:  # => only append LIMIT if one was set
            sql += " LIMIT ?"  # => "?" placeholder, never the literal number
            params.append(self.limit_val)  # => the row cap travels as a bound param
        if self.offset_val is not None:  # => only append OFFSET if one was set
            sql += " OFFSET ?"  # => "?" placeholder, never the literal number
            params.append(self.offset_val)  # => the row skip travels as a bound param
        return sql, params  # => the compiled (sql, params) pair


query = Select(table="items").limit(10).offset(20)  # => page 3 of a 10-row page size
sql, params = query.compile()  # => splits into text + bound values
assert sql == "SELECT * FROM items LIMIT ? OFFSET ?"  # => two "?" placeholders, in order
assert params == [10, 20]  # => limit's value (10) precedes offset's value (20)

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY)")  # => real table
    for n in range(1, 31):  # => seeds 30 rows, ids 1 through 30
        conn.execute("INSERT INTO items(id) VALUES (?)", [n])  # => one parameterized insert
    conn.commit()  # => makes all 30 seed rows visible
    rows = conn.execute(sql, params).fetchall()  # => runs the real paginated SELECT
    print(rows[0], rows[-1], len(rows))  # => Output: (21,) (30,) 10
    # => offset 20 skips ids 1-20; limit 10 keeps exactly ids 21-30
