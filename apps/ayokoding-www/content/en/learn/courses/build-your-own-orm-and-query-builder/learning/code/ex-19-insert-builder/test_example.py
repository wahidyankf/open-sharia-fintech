"""Example 19: pytest verification for insert().values()."""

from example import insert


def test_insert_lists_columns_and_placeholders_in_order() -> None:
    query = insert("orders").values(id=7, total=42.5)  # => two columns, id then total
    sql, params = query.compile()  # => splits into text + bound values
    assert sql == "INSERT INTO orders (id, total) VALUES (?, ?)"  # => matching column order
    assert params == [7, 42.5]  # => id's value precedes total's value


def test_single_column_insert() -> None:
    query = insert("tags").values(name="urgent")  # => just one column
    sql, params = query.compile()  # => splits into text + bound values
    assert sql == "INSERT INTO tags (name) VALUES (?)"  # => one column, one placeholder
    assert params == ["urgent"]  # => exactly one bound value


# => Run: pytest -- Output: 2 passed
