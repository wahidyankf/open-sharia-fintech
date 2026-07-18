"""Example 3: Bind a Value as a Placeholder, Never Interpolate It."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from dataclasses import dataclass  # => a frozen dataclass models the immutable Param node
from typing import Any  # => a bound value can be any Python type SQLite accepts


@dataclass(frozen=True)  # => a literal value node -- NEVER stringified into SQL text
class Param:  # => the non-negotiable safety primitive of this whole builder (co-02)
    value: Any  # => the raw Python value, kept as data -- never f-string-ed into SQL

    def render(self) -> tuple[str, list[Any]]:  # => returns SQL fragment + params, together
        return "?", [self.value]  # => "?" is the ONLY text; the value travels separately


literal = Param(value="Alice; DROP TABLE users;--")  # => a deliberately hostile string
sql_fragment, bound = literal.render()  # => sql_fragment is "?"; bound is [the hostile string]
assert sql_fragment == "?"  # => the SQL text NEVER contains the value's characters
assert bound == ["Alice; DROP TABLE users;--"]  # => the value lives only in the params list

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.commit()  # => empty table, ready for a parameterized insert
    sql = f"INSERT INTO users(id, name) VALUES (1, {sql_fragment})"  # => "?" plugs in as text
    conn.execute(sql, bound)  # => the driver binds bound[0] into the "?" slot itself
    conn.commit()  # => makes the inserted row durable/visible
    row = conn.execute("SELECT name FROM users WHERE id = 1").fetchone()  # => real read-back
    print(row)  # => Output: ('Alice; DROP TABLE users;--',)
    # => the hostile string landed as ONE column value -- no second statement ever ran
    tables = conn.execute(  # => lists every table still present, proving nothing was dropped
        "SELECT name FROM sqlite_master WHERE type = 'table'"  # => sqlite's own catalog table
    ).fetchall()  # => materializes the catalog rows
    assert ("users",) in tables  # => "users" table survived -- the DROP TABLE never executed
