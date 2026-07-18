"""Example 23: compile() Is Pure -- Calling It Twice Changes Nothing."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from typing import Any  # => the params list holds whatever the WHERE clause bound


@dataclasses.dataclass(frozen=True)  # => co-03: immutable state, co-08: a pure compile step
class Select:  # => a minimal SELECT -- this example is about compile()'s purity, not features
    table: str  # => FROM target
    where_value: int | None = None  # => optional "id = ?" filter value

    def where_id(self, value: int) -> "Select":  # => attaches an id filter, immutably
        return dataclasses.replace(self, where_value=value)  # => new instance, self untouched

    def compile(self) -> tuple[str, list[Any]]:  # => NO side effects: reads self, returns a value
        sql = f"SELECT * FROM {self.table}"  # => base SELECT, read from self.table only
        params: list[Any] = []  # => a FRESH list every call -- never reused, never mutated in place
        if self.where_value is not None:  # => reads self.where_value only, never writes it
            sql += " WHERE id = ?"  # => appends the filter fragment
            params.append(self.where_value)  # => appends to the FRESH local list, not shared state
        return sql, params  # => returns a brand-new (sql, params) pair every single call


query = Select(table="users").where_id(7)  # => built once
first_sql, first_params = query.compile()  # => FIRST call
second_sql, second_params = query.compile()  # => SECOND call, same object, called again
assert first_sql == second_sql  # => identical SQL text both times
assert first_params == second_params  # => identical params both times
assert first_params is not second_params  # => but NOT the same list object -- a fresh one each call
first_params.append("mutated locally")  # => mutating the FIRST call's returned list...
assert second_params == [7]  # => ...never touches the SECOND call's list -- no shared state
assert query.where_value == 7  # => query itself is STILL untouched after two compile() calls

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name) VALUES (7, 'Grace')")  # => one seed row
    conn.commit()  # => makes the seed row visible
    row_a = conn.execute(second_sql, second_params).fetchone()  # => runs the SECOND compile's output
    row_b = conn.execute(*query.compile()).fetchone()  # => compiles a THIRD time, runs that too
    print(row_a, row_b)  # => Output: (7, 'Grace') (7, 'Grace')
    # => three separate compile() calls, three identical real results -- no hidden state drifted
