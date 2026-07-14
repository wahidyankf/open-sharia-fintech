"""Example 69: A Swappable Pricing Strategy via Composition."""


class RegularPricing:  # => begins the RegularPricing class body
    def price(self, base: float) -> float:  # => no discount at all
        return base  # => returns this value to the caller


class DiscountPricing:  # => unrelated to RegularPricing -- no shared base class
    def price(self, base: float) -> float:  # => same method NAME, different formula
        return base * 0.8  # => a flat 20% discount


class Order:  # => begins the Order class body
    def __init__(
        self, pricing: RegularPricing
    ) -> None:  # => too NARROW a type -- Example 70 fixes this
        self.pricing = (
            pricing  # => held, not inherited -- swappable at construction time
        )

    def total(self, base: float) -> float:  # => defines the total() method
        return self.pricing.price(
            base
        )  # => delegates the pricing DECISION to the collaborator


regular: Order = Order(RegularPricing())  # => constructs regular
discounted: Order = Order(DiscountPricing())  # type: ignore  # => works at runtime despite the narrow hint
print(
    regular.total(100.0), discounted.total(100.0)
)  # => same Order class, two different totals
# => Output: 100.0 80.0
# => Swapping the collaborator `Order` holds changes `total()`'s result with no subclass of `Order` anywhere
