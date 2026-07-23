"""Example 5: Square(Rectangle) Breaks Liskov Substitution."""


class Rectangle:  # => the base type every client below expects to receive
    def __init__(self, width: float, height: float) -> None:  # => the constructor
        self._width = width  # => stored independently from height, by design
        self._height = height  # => stored independently from width, by design

    def set_width(self, width: float) -> None:  # => changes width ONLY
        self._width = width  # => height is left completely untouched

    def set_height(self, height: float) -> None:  # => changes height ONLY
        self._height = height  # => width is left completely untouched

    def area(self) -> float:  # => defines the area() method
        return self._width * self._height  # => the invariant every client relies on


class BrokenSquare(Rectangle):  # => BROKEN: claims to BE a Rectangle, but is not one
    def set_width(self, width: float) -> None:  # => overrides the base contract
        self._width = width  # => sets width...
        self._height = width  # => ...AND silently mutates height too -- the violation

    def set_height(self, height: float) -> None:  # => overrides the base contract
        self._width = height  # => sets width...
        self._height = height  # => ...AND silently mutates width too -- the violation


def resize_to_5_by_4(shape: Rectangle) -> float:  # => a CLIENT written only against Rectangle
    shape.set_width(5.0)  # => the client trusts this changes ONLY width
    shape.set_height(4.0)  # => the client trusts this changes ONLY height
    return shape.area()  # => a well-behaved Rectangle subtype must return 20.0 here


plain: Rectangle = Rectangle(2.0, 2.0)  # => an ordinary, well-behaved Rectangle
broken: BrokenSquare = BrokenSquare(2.0, 2.0)  # => substituted where Rectangle is expected

plain_area: float = resize_to_5_by_4(plain)  # => plain_area is 20.0, as expected
broken_area: float = resize_to_5_by_4(broken)  # => broken_area is 16.0 -- substitution silently broke the client's assumption

print(plain_area, broken_area)  # => the SAME client function, two different outcomes
# => Output: 20.0 16.0
# => Fixing this means Square must NOT inherit from Rectangle -- see the standalone Square below


class Square:  # => the FIX: a standalone type, unrelated to Rectangle entirely
    def __init__(self, side: float) -> None:  # => the constructor
        self._side = side  # => a Square has exactly one dimension, not two

    def set_side(self, side: float) -> None:  # => there is no set_width/set_height at all
        self._side = side  # => nothing here can violate a contract it never inherited

    def area(self) -> float:  # => defines the area() method
        return self._side * self._side  # => Square's own, honest area formula


square: Square = Square(4.0)  # => never passed to resize_to_5_by_4 -- wrong shape for it
print(square.area())  # => Square is verified entirely on its own terms
# => Output: 16.0
# => `Square` and `Rectangle` are siblings, not parent and child -- neither one's contract binds the other
