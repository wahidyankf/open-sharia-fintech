"""Example 9: pytest verification for Functions Stored in a List."""

from example import double, negate, square


def test_stored_functions_are_called_correctly() -> None:
    operations = [double, square, negate]
    results = [op(5) for op in operations]
    assert results == [10, 25, -5]


# => Run: pytest -- Output: 1 passed
