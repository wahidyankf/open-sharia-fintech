"""Kata 3 (after): construct a NEW Point instead of mutating the frozen one."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def move_right(p: Point) -> Point:
    return Point(p.x + 1, p.y)  # returns a NEW, still-frozen Point


p = Point(1, 2)
p = move_right(p)
print(p)
