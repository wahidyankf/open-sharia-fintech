"""Example 24: pytest verification for Executing a Compiled Tuple Over a Cursor."""

import contextlib
import sqlite3

from example import Select


def test_compiled_tuple_runs_correctly_over_a_real_cursor() -> None:
    sql, params = Select(table="orders").where_status("closed").compile()  # => co-08 output
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => isolated real db
        conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY, status TEXT)")  # => table
        conn.execute("INSERT INTO orders(id, status) VALUES (1, 'closed'), (2, 'open')")
        conn.commit()  # => makes both seed rows visible
        cur = conn.cursor()  # => explicit cursor, same as the example
        cur.execute(sql, params)  # => feeds the compiled tuple straight into the cursor
        rows = cur.fetchall()  # => materializes matching rows
        cur.close()  # => releases the cursor
        assert rows == [(1, "closed")]  # => only the closed order matched


# => Run: pytest -- Output: 1 passed
