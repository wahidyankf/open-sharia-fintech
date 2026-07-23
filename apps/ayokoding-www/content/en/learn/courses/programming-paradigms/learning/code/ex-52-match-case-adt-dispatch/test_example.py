"""Example 52: pytest verification for Match-Case ADT Dispatch."""

from example import Circle, Rectangle, Triangle, area


def test_every_variant_is_handled_by_its_own_case() -> None:
    assert round(area(Circle(2.0)), 2) == 12.57  # => circle variant
    assert area(Rectangle(3.0, 4.0)) == 12.0  # => rectangle variant
    assert area(Triangle(5.0, 6.0)) == 15.0  # => triangle variant


def test_dispatch_is_purely_structural_not_by_an_explicit_tag_field() -> None:
    shapes: list[Circle | Rectangle | Triangle] = [Rectangle(1.0, 1.0), Circle(1.0)]  # => mixed order
    areas = [round(area(s), 2) for s in shapes]  # => each dispatched to the correct case regardless of order
    assert areas == [1.0, 3.14]


# => Run: pytest -- Output: 2 passed
