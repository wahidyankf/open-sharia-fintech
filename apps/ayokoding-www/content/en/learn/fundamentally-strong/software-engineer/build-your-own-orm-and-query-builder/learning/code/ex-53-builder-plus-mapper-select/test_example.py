"""Example 53: pytest verification for Builder-Plus-Mapper SELECT."""

import contextlib
import sqlite3

from example import Select, User, row_to_user


def test_compiled_builder_query_maps_to_a_list_of_typed_objects() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT)")  # => real table
        conn.executemany("INSERT INTO items VALUES (?, ?)", [(1, "a"), (2, "b")])  # => two rows
        conn.commit()  # => makes both rows visible
        sql, params = Select(table="items").compile()  # => no filter -- both rows should come back
        rows = conn.execute(sql, params).fetchall()  # => runs the compiled query
        items = [row_to_user(row) for row in rows]  # => maps every row
        assert len(items) == 2  # => count matches the seeded rows
        assert all(isinstance(x, User) for x in items)  # => every element is a real typed object


def test_where_filter_narrows_which_rows_get_mapped() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT)")
        conn.executemany("INSERT INTO items VALUES (?, ?)", [(1, "a"), (2, "b"), (3, "c")])
        conn.commit()
        sql, params = Select(table="items").where_id_gt(1).compile()  # => filters to id > 1
        rows = conn.execute(sql, params).fetchall()
        items = [row_to_user(row) for row in rows]
        assert [i.id for i in items] == [2, 3]  # => only the filtered rows were mapped


# => Run: pytest -- Output: 2 passed
