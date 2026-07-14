"""Example 26: pytest verification for A Duck-Typed area() Preview."""

from example import Circle, Square


def test_unrelated_classes_both_expose_area() -> None:
    circle: Circle = Circle(2.0)
    square: Square = Square(3.0)
    assert round(circle.area(), 5) == 12.56636  # => Circle's own area formula
    assert (
        square.area() == 9.0
    )  # => Square's own area formula -- no common base class needed


# => Run: pytest -- Output: 1 passed
