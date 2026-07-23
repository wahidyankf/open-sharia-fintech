"""Example 16: .order_by() Appends a Trailing ORDER BY Clause."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-06: ORDER BY is a trailing, ascending-by-default clause
class Select:  # => a minimal single-table SELECT with an ordering slot
    table: str  # => FROM target
    order_bys: tuple[str, ...] = ()  # => accumulated column names to sort by, in order

    def order_by(self, column: str) -> "Select":  # => appends one column, ascending
        return dataclasses.replace(self, order_bys=self.order_bys + (column,))  # => new tuple

    def compile(self) -> str:  # => assembles SELECT, FROM, and a trailing ORDER BY
        sql = f"SELECT * FROM {self.table}"  # => base SELECT
        if self.order_bys:  # => only append ORDER BY if at least one column was added
            sql += " ORDER BY " + ", ".join(self.order_bys)  # => comma-joined column list
        return sql  # => the final assembled SQL string


query = Select(table="users").order_by("name")  # => sort ascending by name
sql = query.compile()  # => renders the accumulated state to SQL text
assert sql == "SELECT * FROM users ORDER BY name"  # => "ORDER BY name" trails the SELECT

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name) VALUES (1, 'Carol'), (2, 'Alice')")  # => 2 rows
    conn.commit()  # => makes both seed rows visible
    rows = conn.execute(sql).fetchall()  # => runs the real ordered SELECT
    print(rows)  # => Output: [(2, 'Alice'), (1, 'Carol')]
    # => Alice sorts before Carol -- proves ORDER BY name actually reordered the result
