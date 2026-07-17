"""Example 46: pytest verification for Replacing a Type-Switch with Polymorphism."""

from example import Circle, Square, Triangle, area_by_type_switch, ShapeData


def test_type_switch_still_computes_the_correct_area() -> None:
    assert area_by_type_switch(ShapeData("square", 4.0)) == 16.0


def test_polymorphic_dispatch_computes_every_shapes_own_area() -> None:
    shapes = [Square(4.0), Circle(2.0), Triangle(3.0, 6.0)]
    areas: list[float] = [s.area() for s in shapes]  # => one shared call-site
    assert areas == [16.0, 12.56636, 9.0]


def test_adding_a_new_shape_requires_no_dispatch_code_changes() -> None:
    # => Triangle is used here exactly like Square/Circle -- proof the dispatch loop above
    # => never needed editing when this class was added to the module
    assert Triangle(2.0, 5.0).area() == 5.0


# => Run: pytest -- Output: 3 passed
