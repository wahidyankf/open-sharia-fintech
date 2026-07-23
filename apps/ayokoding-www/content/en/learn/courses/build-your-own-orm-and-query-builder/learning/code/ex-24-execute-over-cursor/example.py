"""Example 24: A Compiled (sql, params) Tuple Feeds a Real DB-API Cursor."""  # => concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => dataclasses.replace() is the immutable "update" primitive
import sqlite3  # => the stdlib DB-API driver -- co-23's connect/cursor/execute/fetch contract
from typing import Any  # => the params list holds whatever the WHERE clause bound


@dataclasses.dataclass(frozen=True)  # => co-03/co-08: immutable builder, pure compile()
class Select:  # => a minimal SELECT -- this example is about the CURSOR boundary, not features
    table: str  # => FROM target
    where_value: str | None = None  # => optional "status = ?" filter value

    def where_status(self, value: str) -> "Select":  # => attaches a status filter, immutably
        return dataclasses.replace(self, where_value=value)  # => new instance, self untouched

    def compile(self) -> tuple[str, list[Any]]:  # => co-08: the builder's ONLY output
        sql = f"SELECT * FROM {self.table}"  # => base SELECT
        params: list[Any] = []  # => fresh list, every call
        if self.where_value is not None:  # => only append WHERE if a filter was attached
            sql += " WHERE status = ?"  # => "?" placeholder, never the literal string
            params.append(self.where_value)  # => the filter value travels as a bound param
        return sql, params  # => exactly what cursor.execute(sql, params) expects


sql, params = Select(table="orders").where_status("open").compile()  # => co-08 boundary crossed

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, status TEXT)")  # => real table
    conn.execute(  # => three seed rows, two of which are 'open'
        "INSERT INTO orders(id, status) VALUES (1, 'open'), (2, 'closed'), (3, 'open')"
        # => row 2 ('closed') should NOT appear in the "open" cursor result below
    )  # => insert executed against the real in-memory database
    conn.commit()  # => makes all three seed rows visible
    cur = conn.cursor()  # => co-23: an explicit cursor -- the object the builder's output feeds
    cur.execute(sql, params)  # => cursor.execute(sql, params) IS the (sql, params) consumer
    rows = cur.fetchall()  # => materializes every matching row from the cursor
    cur.close()  # => releases the cursor once its rows are consumed
    print(rows)  # => Output: [(1, 'open'), (3, 'open')]
    # => the builder never touched the database -- only the real cursor did, and it found 2 rows
