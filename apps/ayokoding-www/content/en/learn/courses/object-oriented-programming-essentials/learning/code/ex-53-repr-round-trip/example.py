"""Example 53: A __repr__ That Round-Trips Through eval()."""


class Point:  # => begins the Point class body
    def __init__(
        self, x: int, y: int
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.x = x  # => stores x on this instance
        self.y = y  # => stores y on this instance

    def __repr__(
        self,
    ) -> str:  # => shows the EXACT constructor call needed to rebuild this object
        return f"Point({self.x!r}, {self.y!r})"  # => returns this value to the caller

    def __eq__(
        self, other: object
    ) -> bool:  # => needed so eval(repr(obj)) == obj can be checked
        if not isinstance(
            other, Point
        ):  # => guards against comparing a Point to an unrelated type
            return NotImplemented  # => returns this value to the caller
        return (
            self.x == other.x and self.y == other.y
        )  # => returns this value to the caller


p: Point = Point(3, 4)  # => constructs p
rebuilt: Point = eval(
    repr(p)
)  # => literally re-executes the repr string as Python source
print(rebuilt == p)  # => the round-tripped object is equal to the original
# => Output: True
# => A repr shaped exactly like the constructor call (`Point(3, 4)`) is not just readable
