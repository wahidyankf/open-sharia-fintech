"""Example 70: Type the Injected Field Against an Interface, Not a Concrete Class."""

import abc  # => imports the abc module


class PricingStrategy(
    abc.ABC
):  # => the interface Order depends on -- never a concrete class
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def price(
        self, base: float
    ) -> float: ...  # => no body -- both implementations below supply one


class RegularPricing(PricingStrategy):  # => RegularPricing extends PricingStrategy
    def price(self, base: float) -> float:  # => defines the price() method
        return base  # => returns this value to the caller


class DiscountPricing(
    PricingStrategy
):  # => a SECOND implementation of the same interface
    def price(self, base: float) -> float:  # => defines the price() method
        return base * 0.8  # => returns this value to the caller


class Order:  # => begins the Order class body
    def __init__(
        self, pricing: PricingStrategy
    ) -> None:  # => typed against the ABC, not a class
        self.pricing = pricing  # => stores pricing on this instance

    def total(self, base: float) -> float:  # => defines the total() method
        return self.pricing.price(base)  # => returns this value to the caller


strategies: list[PricingStrategy] = [
    RegularPricing(),
    DiscountPricing(),
]  # => two conforming impls
totals: list[float] = [
    Order(s).total(100.0) for s in strategies
]  # => any conforming impl accepted
print(
    totals
)  # => both implementations plug into the SAME Order class with no special-casing
# => Output: [100.0, 80.0]
# => Typing `pricing` as the `PricingStrategy` ABC, not a concrete class, is what lets both implementations pass static type checking
