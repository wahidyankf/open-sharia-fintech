# => Keeps this domain step explicit and reviewable.
"""Example 16: a lifecycle permits named legal transitions."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        self.status = "draft"  # => new orders begin in one known state

    # => Names policy so callers do not recreate the rule.
    def place(self) -> None:
        # => Checks policy before a state change is allowed.
        if self.status != "draft":
            raise ValueError("not draft")  # => transition precondition
        self.status = "placed"  # => state becomes explicit

    # => Names policy so callers do not recreate the rule.
    def ship(self) -> None:
        # => Checks policy before a state change is allowed.
        if self.status != "placed":
            raise ValueError("not placed")  # => draft orders cannot ship
        # => Keeps lifecycle state controlled by the domain object.
        self.status = "shipped"


# => Keeps scenario data close to the rule it exercises.
order = Order()
# => Keeps this domain step explicit and reviewable.
order.place()
order.ship()  # => follows the legal path
# => Proves the stated business rule is observable.
assert order.status == "shipped"
