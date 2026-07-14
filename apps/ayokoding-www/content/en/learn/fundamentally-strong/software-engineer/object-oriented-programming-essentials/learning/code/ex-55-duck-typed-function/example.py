"""Example 55: A Duck-Typed Function Over Mixed Types."""

from typing import Iterable  # => imports Iterable from typing


class Circle:  # => begins the Circle class body
    def __init__(
        self, radius: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.radius = radius  # => stores radius on this instance

    def area(self) -> float:  # => defines the area() method
        return 3.14159 * self.radius**2  # => returns this value to the caller


class Square:  # => begins the Square class body
    def __init__(
        self, side: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.side = side  # => stores side on this instance

    def area(self) -> float:  # => defines the area() method
        return self.side**2  # => returns this value to the caller


def total_area(
    shapes: Iterable[object],
) -> float:  # => accepts ANY iterable of area()-having objects
    return sum(shape.area() for shape in shapes)  # type: ignore
    # => duck typing: only .area() is required, not a shared base class


shapes: list[object] = [
    Circle(1.0),
    Square(2.0),
    Circle(2.0),
]  # => two unrelated types, mixed
print(
    round(total_area(shapes), 5)
)  # => sums every shape's own area formula in one pass
# => Output: 19.70795
# => `total_area` never imports or checks `Circle`/`Square` at all
