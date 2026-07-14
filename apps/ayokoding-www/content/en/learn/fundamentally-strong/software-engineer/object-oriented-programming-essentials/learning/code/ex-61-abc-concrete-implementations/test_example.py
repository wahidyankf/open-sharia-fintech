"""Example 61: pytest verification for Two Concrete Implementations of the Same ABC."""

from example import Circle, Square


def test_both_concrete_implementations_instantiate_and_compute() -> None:
    assert round(Circle(2.0).area(), 2) == 12.57
    assert Square(3.0).area() == 9.0


# => Run: pytest -- Output: 1 passed
