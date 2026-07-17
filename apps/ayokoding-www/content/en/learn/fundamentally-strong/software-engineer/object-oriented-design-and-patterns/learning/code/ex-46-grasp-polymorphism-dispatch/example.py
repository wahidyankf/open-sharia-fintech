"""Example 46: Replacing a Type-Switch with Polymorphic Dispatch."""  # => module docstring

import abc  # => imports the abc module


class ShapeData:  # => a plain data holder, no behavior -- used only by the BEFORE version
    def __init__(self, kind: str, side: float) -> None:  # => the constructor
        self.kind = kind  # => stores kind on this instance
        self.side = side  # => stores side on this instance


def area_by_type_switch(shape: ShapeData) -> float:  # => the BEFORE version -- a type-switch
    if shape.kind == "square":  # => branch 1 -- must be edited for every NEW shape kind
        return shape.side * shape.side  # => returns this value to the caller
    if shape.kind == "circle":  # => branch 2 -- must be edited for every NEW shape kind
        return 3.14159 * shape.side * shape.side  # => returns this value to the caller
    raise ValueError(f"unknown kind: {shape.kind}")  # => a THIRD kind requires editing this exact function


class Shape(abc.ABC):  # => the AFTER version -- one abstract method, no switch anywhere
    @abc.abstractmethod  # => marks the next method as required for every Shape subclass
    def area(self) -> float:  # => no body -- required by every concrete shape
        ...  # => the ellipsis stub -- concrete shapes below fill this in


class Square(Shape):  # => the type-switch's "square" branch, now its OWN class
    def __init__(self, side: float) -> None:  # => the constructor
        self.side = side  # => stores side on this instance

    def area(self) -> float:  # => defines the area() method
        return self.side * self.side  # => returns this value to the caller


class Circle(Shape):  # => the type-switch's "circle" branch, now its OWN class
    def __init__(self, radius: float) -> None:  # => the constructor
        self.radius = radius  # => stores radius on this instance

    def area(self) -> float:  # => defines the area() method
        return 3.14159 * self.radius * self.radius  # => returns this value to the caller


class Triangle(Shape):  # => a BRAND NEW shape -- adding this edits NOTHING above it
    def __init__(self, base: float, height: float) -> None:  # => the constructor
        self.base = base  # => stores base on this instance
        self.height = height  # => stores height on this instance

    def area(self) -> float:  # => defines the area() method
        return 0.5 * self.base * self.height  # => returns this value to the caller


print(area_by_type_switch(ShapeData("square", 4.0)))  # => the OLD, switch-based version
# => Output: 16.0

shapes: list[Shape] = [  # => a heterogeneous list -- every element satisfies the Shape contract
    Square(4.0),  # => side length 4.0, same abstract type as its siblings below
    Circle(2.0),  # => radius 2.0, same abstract type as its siblings
    Triangle(3.0, 6.0),  # => base 3.0, height 6.0 -- a brand-new shape class
]  # => Triangle added with ZERO edits to any existing dispatch code
areas: list[float] = [s.area() for s in shapes]  # => ONE call-site, dispatches polymorphically for ALL three
print(areas)  # => each shape computed its OWN area, no isinstance() or kind check anywhere
# => Output: [16.0, 12.56636, 9.0]
# => Adding `Triangle` required a new class, but edited zero lines of the polymorphic dispatch loop
