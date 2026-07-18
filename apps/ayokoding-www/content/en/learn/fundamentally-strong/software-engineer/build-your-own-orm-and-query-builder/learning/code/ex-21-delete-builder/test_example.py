"""Example 21: pytest verification for delete().where()."""

from example import Eq, delete


def test_delete_with_where_scopes_to_one_row() -> None:
    query = delete("orders").where(Eq(column="id", value=5))  # => targets order 5
    sql, params = query.compile()  # => splits into text + bound values
    assert sql == "DELETE FROM orders WHERE id = ?"  # => WHERE present, "?" not the literal
    assert params == [5]  # => the id travels in the params list


def test_delete_without_where_targets_every_row() -> None:
    query = delete("orders")  # => no .where() call at all
    sql, params = query.compile()  # => splits into text + bound values
    assert sql == "DELETE FROM orders"  # => no "WHERE" text -- deletes everything, explicitly
    assert params == []  # => nothing to bind


# => Run: pytest -- Output: 2 passed
