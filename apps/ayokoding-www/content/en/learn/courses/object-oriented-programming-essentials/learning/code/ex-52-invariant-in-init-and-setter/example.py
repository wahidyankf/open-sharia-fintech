"""Example 52: The Same Invariant Enforced in __init__ and a Setter."""


class Percentage:  # => begins the Percentage class body
    def __init__(
        self, value: float
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.value = (
            value  # => routes through the setter below -- validated on construction too
        )

    @property  # => marks the next method as a computed attribute
    def value(self) -> float:  # => defines the value() method
        return self._value  # => returns this value to the caller

    @value.setter  # => marks the next method as value's validating setter
    def value(
        self, v: float
    ) -> None:  # => the ONE place the 0-100 invariant is actually checked
        if not (
            0 <= v <= 100
        ):  # => guards the invariant on every assignment, not just __init__
            raise ValueError(
                "value must be between 0 and 100"
            )  # => rejects the whole assignment
        self._value = v  # => stores _value on this instance


try:  # => the block below is expected to raise
    Percentage(
        150
    )  # => rejected by __init__, because __init__ assigns through the setter
except ValueError:  # => catches the ValueError raised above
    print(
        "constructor path rejected 150"
    )  # => proves the CONSTRUCTOR path enforces the invariant
# => Output: constructor path rejected 150

p: Percentage = Percentage(50)  # => constructs p
try:  # => the block below is expected to raise
    p.value = 150  # => rejected by the setter path too -- the SAME guard, reused
except ValueError:  # => catches the ValueError raised above
    print(
        "setter path rejected 150"
    )  # => proves the SETTER path enforces the SAME invariant
# => Output: setter path rejected 150
# => Writing the invariant check exactly once, inside the setter, covers both `__init__` and later assignments
