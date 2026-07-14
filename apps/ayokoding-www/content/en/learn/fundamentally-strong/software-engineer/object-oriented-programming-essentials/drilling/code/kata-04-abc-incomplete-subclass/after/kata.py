"""Kata 4 (after): Square implements the required area() method."""

import abc


class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self) -> float: ...


class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side**2


s = Square(3.0)
print(s.area())
