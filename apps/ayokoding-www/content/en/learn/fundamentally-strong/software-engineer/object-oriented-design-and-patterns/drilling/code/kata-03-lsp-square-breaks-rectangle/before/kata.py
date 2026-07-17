"""Kata 3 (before): LSP violation -- Square overrides set_width in a way that breaks callers of Rectangle."""


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def set_width(self, width: float) -> None:
        self.width = width

    def area(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    def set_width(self, width: float) -> None:
        self.width = width
        self.height = width  # SMELL: also changes height -- breaks the Rectangle contract silently


def double_width_only(shape: Rectangle) -> float:
    original_height = shape.height
    shape.set_width(shape.width * 2)
    return shape.height - original_height  # a caller of Rectangle.set_width expects height UNCHANGED


square = Square(4, 4)
print(double_width_only(square))  # expected 0 (height unchanged) -- LSP violation breaks this
