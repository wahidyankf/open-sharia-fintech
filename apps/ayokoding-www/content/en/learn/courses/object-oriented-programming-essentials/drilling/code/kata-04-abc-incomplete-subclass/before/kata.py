"""Kata 4 (before): a Shape subclass that forgets to implement the abstract method."""

import abc


class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self) -> float: ...


class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    # forgot to implement area()


s = Square(3.0)  # type: ignore
print(s.area())
