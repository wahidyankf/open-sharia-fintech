"""Example 45: A Strategy via typing.Protocol Duck Typing."""

from typing import Protocol  # => imports Protocol from typing


class PricingStrategy(Protocol):  # => a STRUCTURAL type -- "anything callable like this"
    def __call__(self, base: float) -> float:  # => the shape every strategy must match
        ...  # => the ellipsis stub -- no shared base class required anywhere


def regular_pricing(base: float) -> float:  # => a PLAIN FUNCTION -- never declares Protocol
    return base  # => returns this value to the caller


def discount_pricing(base: float) -> float:  # => a DIFFERENT plain function, same shape
    return base * 0.8  # => returns this value to the caller


class Order:  # => begins the Order class body
    def __init__(self, pricing: PricingStrategy) -> None:  # => type-hinted against the PROTOCOL, not a concrete class
        self.pricing = pricing  # => held as a swappable collaborator

    def total(self, base: float) -> float:  # => defines the total() method
        return self.pricing(base)  # => calls the strategy as an ordinary function


regular_order: Order = Order(regular_pricing)  # => a bare FUNCTION satisfies the Protocol
discount_order: Order = Order(discount_pricing)  # => a DIFFERENT bare function, same Protocol
print(regular_order.total(100.0))  # => regular_pricing applied
# => Output: 100.0
print(discount_order.total(100.0))  # => discount_pricing applied -- same Order class
# => Output: 80.0
# => `regular_pricing` never declares `PricingStrategy` anywhere -- structural typing accepts it by shape alone
