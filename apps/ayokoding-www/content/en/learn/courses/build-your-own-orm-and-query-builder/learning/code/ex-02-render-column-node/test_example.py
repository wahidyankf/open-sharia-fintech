"""Example 2: pytest verification for Render a Qualified Column Node."""

from example import ColumnRef


def test_unqualified_column_renders_bare_name() -> None:
    node = ColumnRef(name="email")  # => no table supplied
    assert node.render() == "email"  # => bare name, no dot


def test_qualified_column_renders_table_dot_name() -> None:
    node = ColumnRef(name="email", table="users")  # => table supplied
    assert node.render() == "users.email"  # => exactly one dot, table first


# => Run: pytest -- Output: 2 passed
