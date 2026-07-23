"""Example 31: A Property Backed by a Private Field."""


class Rectangle:  # => begins the Rectangle class body
    def __init__(
        self, width: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.width = (
            width  # => external code always uses THIS name, never _width directly
        )

    @property  # => marks the next method as a computed attribute
    def width(self) -> float:  # => defines the width() method
        return (
            self._width
        )  # => internally-named storage field, hidden behind the property

    @width.setter  # => marks the next method as width's validating setter
    def width(self, value: float) -> None:  # => defines the width() method
        self._width = value  # => the ONLY place _width is ever assigned


r: Rectangle = Rectangle(5.0)  # => constructs r
print(r.width)  # => external code never spells out ._width anywhere
# => Output: 5.0
print(
    hasattr(r, "_width")
)  # => the storage field exists, but is not the public interface
# => Output: True
# => A property's public name (`width`) and its private storage name (`_width`) can differ
