"""Example 38: pytest verification for eq=False Falls Back to Identity Equality."""

from example import Point


def test_eq_false_disables_value_equality() -> None:
    a: Point = Point(1, 2)
    b: Point = Point(1, 2)
    assert a != b  # => no generated __eq__ -- falls back to identity, and a is not b


def test_eq_false_still_allows_self_equality() -> None:
    a: Point = Point(1, 2)
    assert a == a  # => identity comparison: an object always equals itself


# => Run: pytest -- Output: 2 passed
