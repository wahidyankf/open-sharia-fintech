"""Example 34: A Consistent __hash__ Alongside __eq__."""


class Money:  # => begins the Money class body
    def __init__(
        self, amount: int, currency: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.amount = amount  # => stores amount on this instance
        self.currency = currency  # => stores currency on this instance

    def __eq__(self, other: object) -> bool:  # => defines the __eq__() method
        if not isinstance(
            other, Money
        ):  # => guards against comparing a Money to an unrelated type
            return NotImplemented  # => returns this value to the caller
        return (
            self.amount == other.amount and self.currency == other.currency
        )  # => returns this value to the caller

    def __hash__(self) -> int:  # => MUST hash the SAME fields __eq__ compares
        return hash(
            (self.amount, self.currency)
        )  # => tuple hash -- combines both fields at once


wallet: set[Money] = {Money(500, "USD"), Money(500, "USD"), Money(100, "USD")}
# => two equal Money objects were inserted above; a correct hash/eq pair deduplicates them
print(len(wallet))  # => only 2 distinct (amount, currency) pairs survive
# => Output: 2
# => `hash((self.amount, self.currency))` combines the exact same fields `__eq__` compares into a single hash
