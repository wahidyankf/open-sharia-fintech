"""Example 17: pytest verification for order_by(desc=True)."""

from example import Select


def test_desc_true_appends_desc_keyword() -> None:
    query = Select(table="orders").order_by("total", desc=True)  # => explicit descending
    assert query.compile() == "SELECT * FROM orders ORDER BY total DESC"  # => DESC present


def test_desc_defaults_to_false() -> None:
    query = Select(table="orders").order_by("total")  # => desc argument omitted entirely
    assert query.compile() == "SELECT * FROM orders ORDER BY total"  # => no DESC keyword


# => Run: pytest -- Output: 2 passed
