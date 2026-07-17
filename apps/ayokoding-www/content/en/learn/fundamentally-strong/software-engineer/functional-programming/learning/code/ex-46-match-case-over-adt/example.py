"""Example 46: match/case Dispatches Over the Shape ADT."""

from __future__ import (
    annotations,
)  # => enables the quoted forward references used below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds each immutable variant


@dataclass(frozen=True)  # => marks Circle immutable, matching the FP style
class Circle:  # => the Circle variant's body
    radius: float  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Square immutable, matching the FP style
class Square:  # => the Square variant's body
    side: float  # => the single field this variant carries


Shape = Circle | Square  # => the ADT itself: a Shape is EITHER variant


def describe(
    shape: Shape,
) -> str:  # => match/case, the structural-pattern-matching alternative to isinstance
    match shape:  # => picks the FIRST case whose pattern matches shape's shape
        case Circle(radius=r):  # => destructures a Circle, binding its radius to r
            return f"circle with radius {r}"  # => the Circle branch's result
        case Square(side=s):  # => destructures a Square, binding its side to s
            return f"square with side {s}"  # => the Square branch's result
        case _:  # => NOTE: match/case has NO compile-time exhaustiveness check -- a manual safety net
            raise ValueError(
                "unreachable for a Circle | Square"
            )  # => defends against a THIRD variant appearing later


# => match/case reads like the ADT's own shape, not a chain of isinstance checks
print(describe(Circle(radius=2.0)))  # => Output: circle with radius 2.0
print(describe(Square(side=5.0)))  # => Output: square with side 5.0
