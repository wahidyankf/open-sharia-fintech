"""Example 35: __eq__ Without __hash__ Is Unhashable."""


class Money:  # => begins the Money class body
    def __init__(
        self, amount: int, currency: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.amount = amount  # => stores amount on this instance
        self.currency = currency  # => stores currency on this instance

    def __eq__(self, other: object) -> bool:  # => defining __eq__ ALONE
        if not isinstance(other, Money):
            return NotImplemented  # => returns this value to the caller
        return (
            self.amount == other.amount and self.currency == other.currency
        )  # => returns this value to the caller

    # => Python sets __hash__ = None automatically the moment __eq__ is defined without __hash__


try:  # => the block below is expected to raise
    {Money(500, "USD")}  # type: ignore  # => building a set calls hash() on each element (static checkers correctly flag Money as unhashable)
except TypeError as exc:  # => catches the TypeError raised above
    print(exc)  # => confirms the instance is genuinely unhashable
# => Output: unhashable type: 'Money'
# => Defining `__eq__` without `__hash__` does not silently inherit `object`'s default hash
