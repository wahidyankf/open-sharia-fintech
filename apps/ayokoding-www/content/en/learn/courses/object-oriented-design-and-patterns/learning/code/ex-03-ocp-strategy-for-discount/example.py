"""Example 3: Replace an If/Elif Chain with Strategy Objects."""  # => module docstring

from typing import Protocol  # => Protocol declares a structural interface, no ABC needed


class DiscountStrategy(Protocol):  # => the ONE shape every discount must match
    # => any class with a matching apply() method satisfies this, no inheritance needed
    def apply(self, price: float) -> float:  # => every strategy exposes apply()
        ...  # => Protocol methods have no body -- this is a structural contract only


class NoDiscount:  # => one interchangeable strategy -- knows nothing about Checkout
    def apply(self, price: float) -> float:  # => matches DiscountStrategy structurally
        return price  # => no discount at all


class LoyaltyDiscount:  # => a second strategy, same method name, different math
    def apply(self, price: float) -> float:  # => matches DiscountStrategy structurally
        return price * 0.9  # => a flat 10% off for loyalty members


class HolidayDiscount:  # => a third strategy, added without touching the other two
    def apply(self, price: float) -> float:  # => matches DiscountStrategy structurally
        return price * 0.75  # => a flat 25% off during holidays


class Checkout:  # => CLOSED for modification: never edited to add a new discount
    def __init__(  # => the constructor, spread across lines to annotate each parameter
        self,
        strategy: DiscountStrategy,
        # => depends on the PROTOCOL, not on any one concrete discount class
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.strategy = strategy  # => held as a collaborator, not hard-coded

    def total(self, price: float) -> float:  # => defines the total() method
        return self.strategy.apply(
            price
            # => no if/elif chain anywhere -- the strategy object IS the branch
        )  # => delegates the discount DECISION entirely to the strategy object


regular: Checkout = Checkout(NoDiscount())  # => open for extension via composition
loyal: Checkout = Checkout(LoyaltyDiscount())  # => a new behavior, zero edits above
holiday: Checkout = Checkout(HolidayDiscount())  # => same Checkout class, third behavior
# => three Checkout instances, three behaviors, ONE unedited Checkout class body

print(
    regular.total(100.0),  # => 100.0, NoDiscount applies no reduction
    loyal.total(100.0),  # => 90.0, LoyaltyDiscount applies 10% off
    holiday.total(100.0),  # => 75.0, HolidayDiscount applies 25% off
    # => each call routes through the same total() method, different collaborator
)  # => three totals, one unmodified Checkout class
# => an if/elif chain would have needed a new branch for every new discount
# => Output: 100.0 90.0 75.0
# => Adding a fourth discount means writing a fourth class with an `apply()` method -- `Checkout` itself never changes again
