"""Example 17: order_by(desc=True) Appends the DESC Keyword."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-06: DESC is a per-column direction flag
class Select:  # => a minimal single-table SELECT with directional ordering
    table: str  # => FROM target
    order_bys: tuple[str, ...] = ()  # => accumulated "column" or "column DESC" fragments

    def order_by(self, column: str, desc: bool = False) -> "Select":  # => desc defaults to False
        fragment = f"{column} DESC" if desc else column  # => appends " DESC" only when asked
        return dataclasses.replace(self, order_bys=self.order_bys + (fragment,))  # => new tuple

    def compile(self) -> str:  # => assembles SELECT, FROM, and the ORDER BY fragments
        sql = f"SELECT * FROM {self.table}"  # => base SELECT
        if self.order_bys:  # => only append ORDER BY if at least one fragment was added
            sql += " ORDER BY " + ", ".join(self.order_bys)  # => comma-joined fragment list
        return sql  # => the final assembled SQL string


ascending = Select(table="users").order_by("name")  # => no desc argument -- defaults False
descending = Select(table="users").order_by("name", desc=True)  # => explicit descending sort
assert ascending.compile() == "SELECT * FROM users ORDER BY name"  # => no DESC keyword
assert descending.compile() == "SELECT * FROM users ORDER BY name DESC"  # => DESC appended

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name) VALUES (1, 'Alice'), (2, 'Bob')")  # => 2 rows
    conn.commit()  # => makes both seed rows visible
    rows = conn.execute(descending.compile()).fetchall()  # => runs the real descending SELECT
    print(rows)  # => Output: [(2, 'Bob'), (1, 'Alice')]
    # => Bob sorts before Alice under DESC -- proves the DESC keyword actually reversed order
