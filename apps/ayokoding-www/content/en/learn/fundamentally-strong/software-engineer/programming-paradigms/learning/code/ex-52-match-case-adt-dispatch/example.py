"""Example 52: Match-Case ADT Dispatch."""

from dataclasses import dataclass  # => @dataclass auto-generates __init__ for each variant below


@dataclass(frozen=True)  # => variant #1 of the sum type
class Circle:  # => frozen=True makes every instance immutable, safe to pattern-match against
    radius: float  # => the one field match/case can destructure below


@dataclass(frozen=True)  # => variant #2 of the sum type
class Rectangle:  # => frozen=True makes every instance immutable, safe to pattern-match against
    width: float  # => one of the two fields match/case can destructure below
    height: float  # => the other field match/case can destructure below


@dataclass(frozen=True)  # => variant #3 of the sum type
class Triangle:  # => frozen=True makes every instance immutable, safe to pattern-match against
    base: float  # => one of the two fields match/case can destructure below
    height: float  # => the other field match/case can destructure below


Shape = Circle | Rectangle | Triangle  # => the SUM TYPE: a value is exactly one of these three variants


def area(shape: Shape) -> float:  # => match/case destructures the ACTIVE variant, no isinstance chain
    match shape:  # => structural pattern matching over a union of dataclasses (PEP 634)
        case Circle(radius=r):  # => matches ONLY if shape is a Circle, binds its field to `r`
            return 3.14159 * r * r  # => classic circle-area formula, using the bound radius
        case Rectangle(width=w, height=h):  # => matches ONLY if shape is a Rectangle
            return w * h  # => classic rectangle-area formula, using the bound width and height
        case Triangle(base=b, height=h):  # => matches ONLY if shape is a Triangle
            return 0.5 * b * h  # => classic triangle-area formula, using the bound base and height
        # => no wildcard case: Shape's three variants are exhaustive, every possibility is handled


shapes: list[Shape] = [Circle(2.0), Rectangle(3.0, 4.0), Triangle(5.0, 6.0)]  # => one of each variant
areas = [round(area(s), 2) for s in shapes]  # => dispatch each shape to its own matching case
print(areas)  # => pi*4, 12, 15
# => Output: [12.57, 12.0, 15.0]
