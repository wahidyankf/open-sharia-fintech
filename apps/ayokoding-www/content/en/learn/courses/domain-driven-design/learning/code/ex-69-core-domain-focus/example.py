"""Example 69: concentrate rules where the business competes."""


class Price:
    def __init__(self, cents: int) -> None:
        self.cents = cents

    def apply_loyalty_rule(self, tier: str) -> int:
        return (
            self.cents - 10 if tier == "gold" else self.cents
        )  # => core policy gets explicit modelling


assert Price(100).apply_loyalty_rule("gold") == 90
