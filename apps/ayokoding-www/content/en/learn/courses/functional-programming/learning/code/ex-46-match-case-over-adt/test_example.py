"""Example 46: pytest verification for match/case Dispatches Over the Shape ADT."""

from example import Circle, Square, describe


def test_each_branch_fires_for_its_own_variant() -> None:
    assert describe(Circle(radius=1.0)) == "circle with radius 1.0"
    assert describe(Square(side=2.0)) == "square with side 2.0"


# => Run: pytest -- Output: 1 passed
