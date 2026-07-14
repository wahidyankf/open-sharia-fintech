"""Example 30: A Property Setter That Validates."""


class Rectangle:  # => begins the Rectangle class body
    def __init__(
        self, width: float, height: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.width = width  # => routes through the setter below, even during __init__
        self.height = height  # => stores height on this instance

    @property  # => marks the next method as a computed attribute
    def width(self) -> float:  # => defines the width() method
        return self._width  # => returns this value to the caller

    @width.setter  # => marks the next method as width's validating setter
    def width(
        self, value: float
    ) -> None:  # => every assignment to .width passes through here
        if value <= 0:  # => guards the invariant: a rectangle's width must be positive
            raise ValueError(
                "width must be positive"
            )  # => rejects the assignment entirely
        self._width = value  # => only reached when the value passed validation


r: Rectangle = Rectangle(3.0, 4.0)  # => constructs r
try:  # => the block below is expected to raise
    r.width = -1  # => triggers the guard above, ordinary attribute-assignment syntax
except ValueError as exc:  # => catches the ValueError raised above
    print(exc)  # => prints the exact rejection message
# => Output: width must be positive
# => `@width.setter` intercepts every `obj.width = value` assignment, including the one `__init__` performs
