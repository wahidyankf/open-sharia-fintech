"""Example 33: A Money Value Object with __eq__."""


class Money:  # => begins the Money class body
    def __init__(
        self, amount: int, currency: str
    ) -> None:  # => amount in integer cents
        self.amount = amount  # => stores amount on this instance
        self.currency = currency  # => stores currency on this instance

    def __eq__(self, other: object) -> bool:  # => defines the __eq__() method
        if not isinstance(other, Money):
            return NotImplemented  # => returns this value to the caller
        return (
            self.amount == other.amount and self.currency == other.currency
        )  # => returns this value to the caller
        # => equal ONLY when BOTH fields match -- a partial match is not equality


a: Money = Money(500, "USD")  # => constructs a
b: Money = Money(500, "USD")  # => same amount and currency, different object
c: Money = Money(500, "EUR")  # => same amount, DIFFERENT currency
print(a == b, a == c)  # => value equality on both fields together
# => Output: True False
# => A multi-field value object's `__eq__` must compare every field that participates in its value
