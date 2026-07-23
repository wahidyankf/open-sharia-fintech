"""Example 26: A Duck-Typed area() Preview."""


class Circle:  # => begins the Circle class body
    def __init__(
        self, radius: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.radius = radius  # => stores radius on this instance

    def area(
        self,
    ) -> float:  # => no shared base class with Square below -- just this one method
        return 3.14159 * self.radius**2  # => returns this value to the caller


class Square:  # => begins the Square class body
    def __init__(
        self, side: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.side = side  # => stores side on this instance

    def area(
        self,
    ) -> float:  # => an UNRELATED class that happens to have the same method name
        return self.side**2  # => returns this value to the caller


def print_area(shape: object) -> None:  # => accepts ANYTHING with an area() method
    print(shape.area())  # type: ignore  # => duck typing: no shared base required (see Example 56)


print_area(Circle(2.0))  # => works because Circle has area()
# => Output: 12.56636
print_area(
    Square(3.0)
)  # => works because Square ALSO has area(), despite no shared ancestor
# => Output: 9.0
# => A function typed to accept `object` and calling `.area()` on it works with any class that happens to define `area()`
