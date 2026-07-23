"""Example 2: Render a Qualified Column Node."""  # => docstring names this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from dataclasses import dataclass  # => a frozen dataclass models the immutable node


@dataclass(frozen=True)  # => still a plain immutable value, one step richer than Example 1
class ColumnRef:  # => a column node that can OPTIONALLY carry its owning table
    name: str  # => the column's own name, e.g. "id"
    table: str | None = None  # => None means "unqualified" -- no owner announced yet

    def render(self) -> str:  # => the ONE place table-qualification logic lives
        if self.table is None:  # => unqualified case: just the bare column name
            return self.name  # => e.g. "id"
        return f"{self.table}.{self.name}"  # => qualified case: "table.column"
        # => e.g. "users.id" -- exactly the fragment a real SELECT/JOIN needs


bare = ColumnRef(name="id")  # => no table given -- stays unqualified
qualified = ColumnRef(name="id", table="users")  # => explicitly owned by "users"
assert bare.render() == "id"  # => unqualified render is just the column name
assert qualified.render() == "users.id"  # => qualified render is "table.column"

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => a real table
    conn.execute("INSERT INTO users(id, name) VALUES (1, 'Alice')")  # => one seed row
    conn.commit()  # => commits the seed row before the SELECT reads it
    fragment = qualified.render()  # => renders "users.id" -- lazily, right before use
    sql = f"SELECT {fragment} FROM users AS users"  # => the qualified fragment plugs straight in
    row = conn.execute(sql).fetchone()  # => runs the qualified fragment as real SQL
    print(row)  # => Output: (1,)
    # => proves "users.id" is not just a string -- it is valid, executable SQL
