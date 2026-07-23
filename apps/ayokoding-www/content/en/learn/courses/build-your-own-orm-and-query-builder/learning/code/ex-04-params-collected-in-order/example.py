"""Example 4: Compile Two Bound Values, Params Stay Left-to-Right."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from dataclasses import dataclass  # => a frozen dataclass models the immutable Param node
from typing import Any  # => a bound value can be any Python type SQLite accepts


@dataclass(frozen=True)  # => same Param node as Example 3 -- one bound literal
class Param:  # => wraps exactly one literal value, deferred to render() time
    value: Any  # => raw value, kept as data

    def render(self) -> tuple[str, list[Any]]:  # => splits into SQL text + a params list
        return "?", [self.value]  # => "?" text, value in its own single-item list


def compile_two(first: Param, second: Param) -> tuple[str, list[Any]]:  # => co-08: compile()
    first_sql, first_params = first.render()  # => renders the FIRST param in isolation
    second_sql, second_params = second.render()  # => renders the SECOND param in isolation
    sql = f"{first_sql}, {second_sql}"  # => "?, ?" -- two placeholders, comma-joined
    params = first_params + second_params  # => concatenation PRESERVES left-to-right order
    return sql, params  # => a single (sql, params) pair, the compile() boundary (co-08)


sql, params = compile_two(Param(value="Bob"), Param(value=42))  # => name first, age second
assert sql == "?, ?"  # => exactly two placeholders, in source order
assert params == ["Bob", 42]  # => "Bob" is params[0] because it was the FIRST argument

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(name TEXT, age INTEGER)")  # => two-column real table
    conn.commit()  # => empty table ready for a two-column insert
    insert_sql = f"INSERT INTO users(name, age) VALUES ({sql})"  # => "?, ?" plugs into VALUES
    conn.execute(insert_sql, params)  # => params[0] binds to name, params[1] binds to age
    conn.commit()  # => makes the inserted row durable/visible
    row = conn.execute("SELECT name, age FROM users").fetchone()  # => real read-back
    print(row)  # => Output: ('Bob', 42)
    # => proves the driver bound params[0]->name and params[1]->age, in that exact order
