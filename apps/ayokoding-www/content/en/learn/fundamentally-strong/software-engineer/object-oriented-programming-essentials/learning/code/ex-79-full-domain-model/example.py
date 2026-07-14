"""Example 79: A Full Domain Model in One Package."""

import abc  # => imports the abc module
from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(frozen=True)  # => co-06: a dataclass value object
class Money:  # => begins the Money class body
    amount: int  # => a required dataclass field, part of the generated __init__


class PricingStrategy(abc.ABC):  # => co-11: an ABC interface
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def price(
        self, base: Money
    ) -> Money: ...  # => no body -- FlatPricing below supplies one


class FlatPricing(PricingStrategy):  # => FlatPricing extends PricingStrategy
    def price(self, base: Money) -> Money:  # => defines the price() method
        return base  # => no adjustment -- the simplest possible strategy


class Invoice:  # => co-02: an encapsulated entity with an invariant
    def __init__(
        self, pricing: PricingStrategy
    ) -> None:  # => co-13: pricing is COMPOSED, not inherited
        self._pricing: PricingStrategy = pricing  # => stores _pricing on this instance
        self._total: Money = Money(
            0
        )  # => private state, only ever changed through add_item

    def add_item(self, base: Money) -> None:  # => defines the add_item() method
        if base.amount < 0:  # => the invariant: no negative line item is ever accepted
            raise ValueError(
                "item amount must be non-negative"
            )  # => co-17: rejects it entirely
        priced: Money = self._pricing.price(base)  # => delegates the pricing decision
        self._total = Money(
            self._total.amount + priced.amount
        )  # => accumulates the running total

    @property  # => marks the next method as a computed attribute
    def total(self) -> Money:  # => defines the total() method
        return self._total  # => returns this value to the caller


invoice: Invoice = Invoice(FlatPricing())  # => constructs invoice
invoice.add_item(Money(500))  # => adds the first, valid line item
invoice.add_item(Money(300))  # => adds a second, valid line item
print(
    invoice.total.amount
)  # => every piece (value object, ABC, composition, invariant) working together
# => Output: 800
# => `Invoice` composes a `PricingStrategy` (co-13, co-11), accumulates `Money` value objects (co-06), and enforces its own invariant (co-02, co-17)
