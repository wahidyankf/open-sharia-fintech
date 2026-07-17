"""Example 18: pytest verification for Factory Method: ShapeFactory Hides Concrete Types."""

# => this test deliberately imports ONLY Shape and ShapeFactory -- never Circle
from example import Shape, ShapeFactory


def test_caller_obtains_a_circle_without_importing_circle() -> None:
    shape: Shape = ShapeFactory.create("circle", 2.0)  # => the caller never wrote Circle(...)
    assert round(shape.area(), 2) == 12.57  # => a genuine, correctly-built Circle


def test_caller_obtains_a_square_without_importing_square() -> None:
    shape: Shape = ShapeFactory.create("square", 3.0)
    assert shape.area() == 9.0  # => a genuine, correctly-built Square


# => Run: pytest -- Output: 2 passed
