"""Example 18: Factory Method: ShapeFactory Hides Concrete Types."""  # => docstring

from typing import Protocol  # => Protocol declares the shape every factory product matches


class Shape(Protocol):  # => the abstraction the caller programs against
    def area(self) -> float:  # => the one method every shape must provide
        ...  # => Protocol methods have no body -- a structural contract only


class Circle:  # => a concrete product -- the caller never names this class directly
    def __init__(self, radius: float) -> None:  # => the constructor
        self.radius = radius  # => stores radius on this instance

    def area(self) -> float:  # => satisfies Shape structurally
        return 3.14159 * self.radius**2  # => a real, honest implementation


class Square:  # => a SECOND concrete product, also hidden behind the factory
    def __init__(self, side: float) -> None:  # => the constructor
        self.side = side  # => stores side on this instance

    def area(self) -> float:  # => satisfies Shape structurally
        return self.side**2  # => a real, honest implementation


class ShapeFactory:  # => the FACTORY METHOD -- defers instantiation to one place
    @staticmethod  # => no instance state needed to build a shape
    def create(  # => the FACTORY METHOD, spread across lines to annotate each argument
        kind: str,  # => a plain string selector, never a class reference
        size: float,
        # => the caller passes a STRING, never a concrete class name like Circle
    ) -> Shape:  # => returns the abstraction, not a named concrete type
        if kind == "circle":  # => the ONLY place that knows Circle exists
            return Circle(size)  # => constructs the concrete product internally
        return Square(size)  # => the ONLY place that knows Square exists


shape: Shape = ShapeFactory.create(
    "circle",  # => the selector string, decides Circle vs Square inside create()
    2.0,  # => the size argument, forwarded to whichever constructor is chosen
    # => this file's caller code never writes `from example import Circle`
)  # => the caller obtains a Circle without ever importing Circle itself

print(round(shape.area(), 2))  # => confirms the factory built a working shape
# => the returned object is typed as Shape -- its exact class stays an implementation detail
# => Output: 12.57
# => Adding a Triangle later means editing ShapeFactory.create() ONCE -- callers never change
