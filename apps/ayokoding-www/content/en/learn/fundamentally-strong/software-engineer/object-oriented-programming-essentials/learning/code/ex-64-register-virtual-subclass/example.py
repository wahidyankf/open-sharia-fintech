"""Example 64: Registering a Virtual Subclass."""

import abc  # => imports the abc module


class Shape(abc.ABC):  # => Shape extends abc.ABC
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def area(self) -> float: ...


class ThirdPartyCircle:  # => a class Shape never declares any relationship to at all
    def __init__(
        self, radius: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.radius = radius  # => stores radius on this instance

    def area(self) -> float:  # => defines the area() method
        return 3.14159 * self.radius**2  # => returns this value to the caller


Shape.register(
    ThirdPartyCircle
)  # => tells the ABC machinery to treat this class as a Shape
print(
    isinstance(ThirdPartyCircle(1.0), Shape)
)  # => True, with ZERO inheritance declared anywhere
# => Output: True
print(
    ThirdPartyCircle in Shape.__subclasses__()
)  # => .register() does NOT appear in the MRO list
# => Output: False
# => `.register()` grants `isinstance`/`issubclass` compatibility without touching the registered class's own definition or its method resolution order at all
