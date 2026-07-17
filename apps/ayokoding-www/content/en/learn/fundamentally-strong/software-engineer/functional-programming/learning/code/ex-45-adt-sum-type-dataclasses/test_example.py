"""Example 45: pytest verification for A Shape ADT as a Union of Frozen Dataclasses."""

from example import Circle, Square, area


def test_each_variant_computes_its_own_area() -> None:
    assert round(area(Circle(radius=1.0)), 2) == 3.14
    assert area(Square(side=4.0)) == 16.0


# => Run: pytest -- Output: 1 passed
