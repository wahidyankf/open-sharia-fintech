"""Example 16: pytest verification for .order_by() Appends ORDER BY."""

from example import Select


def test_order_by_appends_trailing_clause() -> None:
    query = Select(table="users").order_by("name")  # => one sort column
    assert query.compile() == "SELECT * FROM users ORDER BY name"  # => trails the SELECT


def test_multiple_order_by_columns_stay_in_call_order() -> None:
    query = Select(table="users").order_by("name").order_by("id")  # => two sort columns
    assert query.compile() == "SELECT * FROM users ORDER BY name, id"  # => "name" listed first


# => Run: pytest -- Output: 2 passed
