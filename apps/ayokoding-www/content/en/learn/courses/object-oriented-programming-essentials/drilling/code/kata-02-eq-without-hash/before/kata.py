"""Kata 2 (before): __eq__ defined alone -- silently makes the class unhashable."""


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y


points = {Point(1, 2), Point(1, 2)}  # type: ignore
print(points)
