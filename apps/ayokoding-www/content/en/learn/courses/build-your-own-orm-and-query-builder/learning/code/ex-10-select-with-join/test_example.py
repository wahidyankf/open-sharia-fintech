"""Example 10: pytest verification for .join() Adds a JOIN Fragment."""

from example import select


def test_join_fragment_appears_after_from() -> None:
    query = select("id").from_("users").join("orders", on="users.id = orders.user_id")
    sql = query.compile()  # => renders the full SELECT ... FROM ... JOIN string
    assert sql == "SELECT id FROM users JOIN orders ON users.id = orders.user_id"


def test_multiple_joins_accumulate_in_call_order() -> None:
    query = (
        select("id")  # => builder start
        .from_("users")  # => driving table
        .join("orders", on="a")  # => first join, predicate "a"
        .join("payments", on="b")  # => second join, predicate "b"
    )
    assert "JOIN orders ON a" in query.compile()  # => first join present
    assert query.compile().index("orders") < query.compile().index("payments")
    # => "orders" appears BEFORE "payments" -- call order is preserved in the SQL


# => Run: pytest -- Output: 2 passed
