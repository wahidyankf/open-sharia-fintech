"""Example 8: pytest verification for .from_() Attaches the FROM Target."""

from example import select


def test_from_sets_table_without_mutating_original() -> None:
    base = select("id")  # => no table yet
    branched = base.from_("users")  # => branch with a table attached
    assert base.table is None  # => base is unaffected by the branch
    assert branched.table == "users"  # => only the branch carries "users"


def test_from_can_target_different_tables_independently() -> None:
    base = select("id")  # => shared trunk, no table yet
    users = base.from_("users")  # => one branch targets "users"
    orders = base.from_("orders")  # => a second, independent branch targets "orders"
    assert users.compile() == "SELECT id FROM users"  # => first branch's own SQL
    assert orders.compile() == "SELECT id FROM orders"  # => second branch's own SQL


# => Run: pytest -- Output: 2 passed
