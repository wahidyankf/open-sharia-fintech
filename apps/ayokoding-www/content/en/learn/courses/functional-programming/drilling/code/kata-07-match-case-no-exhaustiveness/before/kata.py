"""Kata 7 (before): a new ADT variant falls through match/case silently -- no compile-time warning."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Circle:
    radius: float


@dataclass(frozen=True)
class Square:
    side: float


@dataclass(frozen=True)
class Triangle:  # => a NEW variant added to the shape family after the evaluator below was written
    base: float
    height: float


Shape = Circle | Square | Triangle  # => the ADT now has THREE variants


def area(shape: Shape) -> float:  # type: ignore[misc]  # pyright statically flags what CPython won't
    match shape:  # type: ignore[misc]  # SMELL: no Triangle case, no wildcard -- pyright catches it, CPython doesn't
        case Circle(radius=r):
            return 3.14159 * r * r
        case Square(side=s):
            return s * s
    # BUG: falls through here for Triangle -- Python raises NOTHING, the function returns None


result = area(
    Triangle(base=4.0, height=3.0)
)  # a legitimate Shape value the evaluator never handles
print(result)  # BUG: prints None instead of raising or computing an area
