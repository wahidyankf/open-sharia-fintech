"""Kata 7 (after): fix -- an explicit wildcard case raises instead of silently falling through."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Circle:
    radius: float


@dataclass(frozen=True)
class Square:
    side: float


@dataclass(frozen=True)
class Triangle:
    base: float
    height: float


Shape = Circle | Square | Triangle


def area(shape: Shape) -> float:
    match shape:
        case Circle(radius=r):
            return 3.14159 * r * r
        case Square(side=s):
            return s * s
        case Triangle(base=b, height=h):  # => the new variant now has its OWN branch
            return 0.5 * b * h
        case _:  # => a manual safety net for any FUTURE variant this evaluator hasn't been taught yet
            raise ValueError(f"unhandled shape variant: {shape!r}")


result = area(Triangle(base=4.0, height=3.0))
print(result)
