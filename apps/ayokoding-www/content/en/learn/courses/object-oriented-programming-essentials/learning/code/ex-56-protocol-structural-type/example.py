"""Example 56: typing.Protocol Formalizes Duck Typing."""

from typing import (
    Protocol,
    runtime_checkable,
)  # => imports Protocol, runtime_checkable from typing


@runtime_checkable  # => opts this Protocol into isinstance() checks at runtime, not just static
class HasArea(
    Protocol
):  # => a STRUCTURAL type: "anything with an area() -> float method"
    def area(
        self,
    ) -> float: ...  # => no implementation -- just the shape of the contract


class Circle:  # => NEVER declares `class Circle(HasArea)` -- no inheritance link at all
    def __init__(
        self, radius: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.radius = radius  # => stores radius on this instance

    def area(
        self,
    ) -> float:  # => satisfies HasArea purely by having this exact method shape
        return 3.14159 * self.radius**2  # => returns this value to the caller


def describe(
    shape: HasArea,
) -> str:  # => type-hinted against the PROTOCOL, not a concrete class
    return f"area is {shape.area()}"  # => returns this value to the caller


print(
    describe(Circle(2.0))
)  # => a static checker accepts this with zero inheritance declared
# => Output: area is 12.56636
print(
    isinstance(Circle(2.0), HasArea)
)  # => @runtime_checkable makes THIS check work too
# => Output: True
# => `Protocol` gives duck typing a name a static checker can verify ahead of time
