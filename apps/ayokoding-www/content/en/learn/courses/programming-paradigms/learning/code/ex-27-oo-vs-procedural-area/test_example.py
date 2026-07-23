"""Example 27: pytest verification for OO vs Procedural Area."""

from example import Circle, Square, area_via_tag


def test_oo_and_procedural_agree_on_circle_area() -> None:
    circle = Circle(5.0)  # => OO object
    tagged = {"kind": 0, "radius": 5.0}  # => procedural equivalent, same radius
    assert round(circle.area(), 6) == round(area_via_tag(tagged), 6)  # => must be equal areas


def test_oo_and_procedural_agree_on_square_area() -> None:
    square = Square(4.0)  # => OO object
    tagged = {"kind": 1, "side": 4.0}  # => procedural equivalent, same side
    assert square.area() == area_via_tag(tagged) == 16.0  # => 4 squared, both styles agree exactly


# => Run: pytest -- Output: 2 passed
