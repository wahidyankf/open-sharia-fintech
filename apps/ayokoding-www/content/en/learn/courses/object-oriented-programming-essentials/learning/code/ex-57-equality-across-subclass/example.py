"""Example 57: A Type-Strict __eq__ Across a Subclass."""


class Money:  # => begins the Money class body
    def __init__(
        self, amount: int
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.amount = amount  # => stores amount on this instance

    def __eq__(self, other: object) -> bool:  # => defines the __eq__() method
        if type(other) is not type(
            self
        ):  # => STRICT: exact type match, not isinstance()
            return NotImplemented  # => a subclass instance is deliberately never equal to a Money
        return self.amount == other.amount  # type: ignore


class Cash(Money):  # => a subclass adding no new fields, just a different TYPE
    pass  # => an intentionally empty body


m: Money = Money(500)  # => constructs m
c: Cash = Cash(500)  # => same amount, but a DIFFERENT exact type than Money
print(m == c)  # => the type-strict contract: equal amount is not enough across types
# => Output: False
# => `type(other) is not type(self)` is a stricter equality contract than `isinstance(other, Money)`
