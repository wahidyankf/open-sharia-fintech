"""Kata 3 (before): assigning a frozen dataclass field as if it were a plain mutable object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def move_right(p: Point) -> None:
    p.x = p.x + 1  # type: ignore  # looks like a normal mutation -- but Point is frozen


p = Point(1, 2)
move_right(p)
print(p)
