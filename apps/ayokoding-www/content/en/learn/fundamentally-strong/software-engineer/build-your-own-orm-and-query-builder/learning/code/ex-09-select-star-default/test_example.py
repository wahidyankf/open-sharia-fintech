"""Example 9: pytest verification for select() Defaults to SELECT *."""

from example import select


def test_no_columns_compiles_to_star() -> None:
    query = select().from_("orders")  # => zero column names given
    assert query.compile() == "SELECT * FROM orders"  # => defaults to a bare "*"


def test_explicit_columns_override_the_star_default() -> None:
    query = select("id").from_("orders")  # => one column IS given this time
    assert query.compile() == "SELECT id FROM orders"  # => "*" default never applies here


# => Run: pytest -- Output: 2 passed
