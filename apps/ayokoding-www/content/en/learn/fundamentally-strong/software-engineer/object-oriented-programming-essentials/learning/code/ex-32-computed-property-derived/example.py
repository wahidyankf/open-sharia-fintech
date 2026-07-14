"""Example 32: A Computed Property Derived from Two Fields."""


class Rectangle:  # => begins the Rectangle class body
    def __init__(
        self, width: float, height: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.width = width  # => stores width on this instance
        self.height = height  # => stores height on this instance

    @property  # => marks the next method as a computed attribute
    def perimeter(self) -> float:  # => recomputed from width/height every single access
        return 2 * (self.width + self.height)  # => returns this value to the caller


r: Rectangle = Rectangle(3.0, 4.0)  # => constructs r
print(r.perimeter)  # => baseline perimeter before mutating width below
# => Output: 14.0
r.width = 10.0  # => mutating a plain field the property depends on
print(r.perimeter)  # => perimeter reflects the NEW width -- nothing was cached
# => Output: 28.0
# => A property with no explicit cache always recomputes from its dependencies
