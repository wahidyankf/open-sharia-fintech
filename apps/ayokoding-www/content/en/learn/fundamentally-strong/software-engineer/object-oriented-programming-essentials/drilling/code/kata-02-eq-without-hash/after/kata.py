"""Kata 2 (after): a __hash__ consistent with __eq__, restoring hashability."""


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


points = {Point(1, 2), Point(1, 2)}
print(len(points))
