"""Example 27: OO vs Procedural Area."""

from abc import ABC, abstractmethod  # => ABC/abstractmethod force every subclass to define area()
from math import pi  # => needed by Circle's own formula below


class Shape(ABC):  # => OO version: each shape KNOWS how to compute its own area
    @abstractmethod  # => marks area() as required -- Shape itself can never be instantiated directly
    def area(self) -> float:  # => every subclass must supply its own formula
        ...  # => no body here -- only concrete subclasses provide the real implementation


class Circle(Shape):  # => one concrete shape
    def __init__(self, radius: float) -> None:  # => constructor takes the one measurement a circle needs
        self.radius = radius  # => the only piece of state a circle needs

    def area(self) -> float:  # => circle's own formula, no other shape's code is aware of it
        return pi * self.radius**2  # => classic circle-area formula, using this instance's own radius


class Square(Shape):  # => a second, unrelated concrete shape
    def __init__(self, side: float) -> None:  # => constructor takes the one measurement a square needs
        self.side = side  # => the only piece of state a square needs

    def area(self) -> float:  # => square's own formula
        return self.side**2  # => classic square-area formula, using this instance's own side


def area_via_tag(shape: dict[str, float]) -> float:  # => PROCEDURAL version: one function, a tag dict
    kind = shape["kind"]  # => reads a "tag" field to decide which formula to use
    if kind == 0:  # => 0 means circle -- the tag encoding is implicit, external knowledge
        return pi * shape["radius"] ** 2  # => same circle formula, but the caller must pass the right keys
    elif kind == 1:  # => 1 means square
        return shape["side"] ** 2  # => same square formula, gated behind the same external tag convention
    raise ValueError(f"unknown shape kind: {kind}")  # => any other tag is a bug


oo_shapes: list[Shape] = [Circle(2.0), Square(3.0)]  # => OO objects, dispatch via area()
oo_areas = [round(s.area(), 4) for s in oo_shapes]  # => polymorphic calls, no tag anywhere

tagged_shapes: list[dict[str, float]] = [  # => PROCEDURAL objects: plain dicts, no shape-specific class
    {"kind": 0, "radius": 2.0},  # => must match area_via_tag's kind==0 branch's expected keys exactly
    {"kind": 1, "side": 3.0},  # => must match area_via_tag's kind==1 branch's expected keys exactly
]  # => closes the list of tagged dicts driving the procedural version through both shapes
procedural_areas = [round(area_via_tag(s), 4) for s in tagged_shapes]  # => one function, external tag

print(oo_areas)  # => circle area then square area
# => Output: [12.5664, 9.0]
print(oo_areas == procedural_areas)  # => both styles must compute the identical areas
# => Output: True
