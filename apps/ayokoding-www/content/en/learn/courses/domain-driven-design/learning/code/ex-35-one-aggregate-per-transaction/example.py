# => Keeps this domain step explicit and reviewable.
"""Example 35: queue work for the other aggregate."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.placed = False

    # => Names policy so callers do not recreate the rule.
    def place(self) -> str:
        self.placed = True  # => this transaction changes only the order root
        # => Returns the domain result instead of leaking representation.
        return (
            "inventory-reservation-requested"  # => the second update becomes a message
            # => Keeps this domain step explicit and reviewable.
        )


# => Proves the stated business rule is observable.
assert Order().place() == "inventory-reservation-requested"
