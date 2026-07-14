"""Example 29: A Read-Only Property."""


class Rectangle:  # => begins the Rectangle class body
    def __init__(
        self, width: float, height: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.width = width  # => stores width on this instance
        self.height = height  # => stores height on this instance

    @property  # => marks the next method as a computed attribute
    def area(
        self,
    ) -> float:  # => computed on every access -- never stored as its own field
        return (
            self.width * self.height
        )  # => always reflects the CURRENT width and height


r: Rectangle = Rectangle(3.0, 4.0)  # => constructs r
print(r.area)  # => read like a plain attribute -- no parentheses at the call site
# => Output: 12.0
# => `@property` on a method makes `obj.method_name` (no parentheses) call it
