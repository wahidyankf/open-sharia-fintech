"""Example 12: pytest verification for Combine Two Predicates With AND."""

from example import And, col


def test_and_joins_two_predicates_with_and_keyword() -> None:
    pred = And(left=col("a") == 1, right=col("b") == 2)  # => two leaves
    sql, params = pred.compile()  # => splits into text + bound values
    assert sql == "a = ? AND b = ?"  # => exactly one " AND " between the two leaves
    assert params == [1, 2]  # => left's value before right's value


def test_and_params_stay_in_left_to_right_order_even_when_swapped() -> None:
    pred = And(left=col("b") == 2, right=col("a") == 1)  # => swapped left/right this time
    _, params = pred.compile()  # => only params are checked here
    assert params == [2, 1]  # => order tracks left/right position, not column name


# => Run: pytest -- Output: 2 passed
