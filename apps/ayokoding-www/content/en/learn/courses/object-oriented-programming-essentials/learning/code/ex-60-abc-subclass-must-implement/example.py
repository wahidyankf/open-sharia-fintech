"""Example 60: An Incomplete Subclass Also Cannot Be Instantiated."""

import abc  # => imports the abc module


class Shape(abc.ABC):  # => Shape extends abc.ABC
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def area(
        self,
    ) -> float: ...  # => no body -- Triangle below never supplies one either


class Triangle(Shape):  # => subclasses Shape but forgets to implement area()
    pass  # => STILL abstract -- the missing method means Triangle inherits the same restriction


try:  # => the block below is expected to raise
    Triangle()  # type: ignore  # => fails for the same reason Shape() does: area() is unimplemented
except TypeError as exc:  # => catches the TypeError raised above
    print(
        type(exc).__name__
    )  # => confirms it is genuinely a TypeError, same as Example 59
# => Output: TypeError
# => Subclassing an ABC does not automatically satisfy its contract
