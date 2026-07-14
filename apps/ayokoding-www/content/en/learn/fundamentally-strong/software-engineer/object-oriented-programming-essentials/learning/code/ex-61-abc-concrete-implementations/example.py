"""Example 61: Two Concrete Implementations of the Same ABC."""

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

    def area(
        self,
    ) -> float:  # => implements the required abstract method -- now instantiable
        return math.pi * self.radius**2  # => returns this value to the caller


class Square(Shape):  # => Square extends Shape
    def __init__(
        self, side: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.side = side  # => stores side on this instance

    def area(
        self,
    ) -> float:  # => a SECOND, independent implementation of the same contract
        return self.side**2  # => returns this value to the caller


print(
    round(Circle(2.0).area(), 2), Square(3.0).area()
)  # => both classes instantiate AND compute
# => Output: 12.57 9.0
# => Implementing every abstract method a base class declares is the entire requirement for instantiability
