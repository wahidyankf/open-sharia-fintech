"""Example 62: One Call-Site Handles Every Shape Implementation."""

import abc  # => imports the abc module
import math  # => imports the math module


class Shape(abc.ABC):  # => Shape extends abc.ABC
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def area(
        self,
    ) -> float: ...  # => no body -- Circle and Square below each supply their own


class Circle(Shape):  # => Circle extends Shape
    def __init__(
        self, radius: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.radius = radius  # => stores radius on this instance

    def area(self) -> float:  # => defines the area() method
        return math.pi * self.radius**2  # => returns this value to the caller


class Square(Shape):  # => Square extends Shape
    def __init__(
        self, side: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.side = side  # => stores side on this instance

    def area(self) -> float:  # => defines the area() method
        return self.side**2  # => returns this value to the caller


def describe(
    shape: Shape,
) -> str:  # => typed against the ABC -- accepts ANY Shape subclass
    return f"{type(shape).__name__} area is {shape.area():.2f}"  # => returns this value to the caller


shapes: list[Shape] = [
    Circle(2.0),
    Square(3.0),
]  # => mixed concrete types, one shared base
print(
    [describe(s) for s in shapes]
)  # => the SAME function handles both, no branching by type
# => Output: ['Circle area is 12.57', 'Square area is 9.00']
# => `describe(shape: Shape)` contains no `if isinstance(shape, Circle)` branch anywhere
