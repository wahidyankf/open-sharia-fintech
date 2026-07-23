"""Example 22: pytest verification for A Dataclass's Auto-Generated __eq__."""

from example import Point


def test_equal_field_values_compare_equal() -> None:
    a: Point = Point(1, 2)
    b: Point = Point(1, 2)
    assert a == b  # => value equality, generated automatically from the field list
    assert a is not b  # => still two separate objects


# => Run: pytest -- Output: 1 passed
