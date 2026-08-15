# => Keeps this domain step explicit and reviewable.
"""Example 49: an application service coordinates without owning policy."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.placed = False

    # => Names policy so callers do not recreate the rule.
    def place(self) -> None:
        self.placed = True  # => business transition belongs in the root


# => Names policy so callers do not recreate the rule.
def place_order(order: Order, saved: list[Order]) -> None:
    # => Keeps this domain step explicit and reviewable.
    order.place()
    saved.append(order)  # => application layer coordinates state and persistence


# => Keeps this domain step explicit and reviewable.
saved: list[Order] = []
# => Keeps this domain step explicit and reviewable.
place_order(Order(), saved)
# => Proves the stated business rule is observable.
assert saved[0].placed
