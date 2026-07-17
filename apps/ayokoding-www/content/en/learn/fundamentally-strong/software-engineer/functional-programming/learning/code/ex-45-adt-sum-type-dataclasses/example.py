"""Example 45: A Shape ADT as a Union of Frozen Dataclasses."""

from __future__ import (
    annotations,
)  # => enables the quoted forward references used below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds each immutable variant


@dataclass(
    frozen=True
)  # => one VARIANT of the Shape ADT -- only the field a circle needs
class Circle:  # => the Circle variant's body
    radius: float  # => the single field this variant carries


@dataclass(frozen=True)  # => a SECOND variant -- only the field a square needs
class Square:  # => the Square variant's body
    side: float  # => the single field this variant carries


Shape = (
    Circle | Square
)  # => PEP 604 union syntax (3.10+): a Shape IS EITHER a Circle OR a Square


def area(
    shape: Shape,
) -> float:  # => accepts EITHER variant -- illegal combinations don't type-check
    if isinstance(shape, Circle):  # => narrows shape to Circle inside this branch
        return 3.14159 * shape.radius**2  # => the actual circle-area formula
    return (
        shape.side**2
    )  # => shape is narrowed to Square here (the only remaining case)


circle_shape: Shape = Circle(radius=2.0)  # => constructs the Circle variant
square_shape: Shape = Square(side=3.0)  # => constructs the Square variant

# => a sum type restricts callers to EXACTLY the variants the ADT defines
print(round(area(circle_shape), 2))  # => Output: 12.57
print(area(square_shape))  # => Output: 9.0
print(
    isinstance(circle_shape, Square)
)  # => Output: False -- a Circle can never ALSO be a Square
