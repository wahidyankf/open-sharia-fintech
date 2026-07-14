"""Example 62: pytest verification for One Call-Site Handles Every Shape Implementation."""

from example import Circle, Square, describe


def test_one_function_handles_every_shape_subclass() -> None:
    assert describe(Circle(2.0)) == "Circle area is 12.57"
    assert (
        describe(Square(3.0)) == "Square area is 9.00"
    )  # => same describe(), no type branching


# => Run: pytest -- Output: 1 passed
