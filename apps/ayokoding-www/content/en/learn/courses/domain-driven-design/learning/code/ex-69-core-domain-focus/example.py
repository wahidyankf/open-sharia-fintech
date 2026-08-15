# => Keeps this domain step explicit and reviewable.
"""Example 69: concentrate rules where the business competes."""


# => Gives domain rules a single, named home.
class Price:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, cents: int) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.cents = cents

    # => Names policy so callers do not recreate the rule.
    def apply_loyalty_rule(self, tier: str) -> int:
        # => Returns the domain result instead of leaking representation.
        return (
            # => Keeps lifecycle state controlled by the domain object.
            self.cents - 10 if tier == "gold" else self.cents
        )  # => core policy gets explicit modelling


# => Proves the stated business rule is observable.
assert Price(100).apply_loyalty_rule("gold") == 90
