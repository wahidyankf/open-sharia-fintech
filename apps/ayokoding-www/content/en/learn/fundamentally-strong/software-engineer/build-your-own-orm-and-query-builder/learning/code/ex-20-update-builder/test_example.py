"""Example 20: pytest verification for update().set().where()."""

from example import Eq, update


def test_update_orders_set_params_before_where_params() -> None:
    query = update("orders").set(status="shipped").where(Eq(column="id", value=9))
    sql, params = query.compile()  # => splits into text + bound values
    assert sql == "UPDATE orders SET status = ? WHERE id = ?"  # => SET clause, then WHERE
    assert params == ["shipped", 9]  # => SET's value first, WHERE's value second


def test_update_without_where_targets_every_row() -> None:
    query = update("orders").set(status="archived")  # => no .where() call at all
    sql, params = query.compile()  # => splits into text + bound values
    assert sql == "UPDATE orders SET status = ?"  # => no "WHERE" text at all -- every row
    assert params == ["archived"]  # => exactly one bound value


# => Run: pytest -- Output: 2 passed
