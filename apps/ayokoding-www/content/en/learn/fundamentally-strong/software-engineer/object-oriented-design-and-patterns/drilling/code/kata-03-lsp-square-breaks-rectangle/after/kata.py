"""Kata 3 (after): LSP -- Square no longer subclasses Rectangle; each honors its own, distinct contract."""


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def set_width(self, width: float) -> None:
        self.width = width

    def area(self) -> float:
        return self.width * self.height


class Square:  # => no longer a Rectangle subclass -- avoids inheriting a contract it cannot honor
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side


def double_width_only(shape: Rectangle) -> float:  # => genuinely only accepts Rectangle-shaped things now
    original_height = shape.height
    shape.set_width(shape.width * 2)
    return shape.height - original_height


rectangle = Rectangle(4, 4)
print(double_width_only(rectangle))  # 0 -- Rectangle actually honors ITS OWN contract
