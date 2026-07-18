"""Example 7: pytest verification for select() Lists Explicit Columns."""

from example import select


def test_select_lists_columns_in_call_order() -> None:
    query = select("name", "id").from_("users")  # => name given BEFORE id this time
    assert query.compile() == "SELECT name, id FROM users"  # => order matches the call


def test_select_with_single_column() -> None:
    query = select("id").from_("users")  # => just one column requested
    assert query.compile() == "SELECT id FROM users"  # => no comma, one bare column


# => Run: pytest -- Output: 2 passed
