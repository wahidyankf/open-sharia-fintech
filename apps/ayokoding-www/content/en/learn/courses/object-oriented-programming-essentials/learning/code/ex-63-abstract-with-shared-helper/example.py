"""Example 63: An ABC Providing a Concrete Shared Helper."""

import abc  # => imports the abc module


class Shape(abc.ABC):  # => Shape extends abc.ABC
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def area(
        self,
    ) -> float: ...  # => no body -- Square below supplies the required implementation

    def describe(
        self,
    ) -> str:  # => a CONCRETE method -- every subclass inherits this for free
        return f"{type(self).__name__}: area={self.area():.2f}"  # => reuses the abstract method


class Square(Shape):  # => Square extends Shape
    def __init__(
        self, side: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.side = side  # => stores side on this instance

    def area(self) -> float:  # => Square only implements the REQUIRED abstract part
        return self.side**2  # => returns this value to the caller


print(
    Square(3.0).describe()
)  # => describe() was never redefined -- inherited straight from Shape
# => Output: Square: area=9.00
# => An ABC is not "every method abstract"
