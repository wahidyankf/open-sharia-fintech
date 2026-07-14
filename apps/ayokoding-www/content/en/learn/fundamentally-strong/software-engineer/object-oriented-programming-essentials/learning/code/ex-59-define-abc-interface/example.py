"""Example 59: Define an ABC Interface."""

import abc  # => imports the abc module


class Shape(
    abc.ABC
):  # => abc.ABC marks this class as an INTERFACE, never directly instantiable
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def area(
        self,
    ) -> float:  # => no body implementation -- a REQUIRED contract for subclasses
        ...  # => the ellipsis stub -- Shape() below proves this makes the class uninstantiable


try:  # => the block below is expected to raise
    Shape()  # type: ignore  # => instantiating an ABC with unimplemented methods always fails
except TypeError as exc:  # => catches the TypeError raised above
    print(
        type(exc).__name__
    )  # => confirms it is genuinely a TypeError, not merely any exception
# => Output: TypeError
# => `abc.ABC` plus at least one `@abstractmethod` makes a class impossible to instantiate directly
