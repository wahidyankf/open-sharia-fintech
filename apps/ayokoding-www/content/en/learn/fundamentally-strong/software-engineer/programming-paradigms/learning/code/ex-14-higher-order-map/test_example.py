"""Example 14: pytest verification for Higher-Order Map."""

from example import apply_all, double, square


def test_apply_all_with_named_functions() -> None:
    numbers = [1, 2, 3, 4]  # => shared sample input
    assert apply_all(double, numbers) == [2, 4, 6, 8]  # => passing double as a value
    assert apply_all(square, numbers) == [1, 4, 9, 16]  # => passing square as a value, same helper


def test_apply_all_with_a_lambda_and_the_identity_function() -> None:
    numbers = [5, 10]  # => small sample input
    assert apply_all(lambda n: n, numbers) == [5, 10]  # => identity: transforms nothing
    assert apply_all(lambda n: -n, numbers) == [-5, -10]  # => a fresh anonymous transform


# => Run: pytest -- Output: 2 passed
