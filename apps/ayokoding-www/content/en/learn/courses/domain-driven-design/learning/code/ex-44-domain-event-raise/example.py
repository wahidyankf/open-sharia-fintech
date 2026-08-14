# => Keeps this domain step explicit and reviewable.
"""Example 44: a root records an event after its transition."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.pending_events: list[str] = []

    # => Names policy so callers do not recreate the rule.
    def place(self) -> None:
        self.pending_events.append("OrderPlaced")  # => root records the domain fact


# => Keeps scenario data close to the rule it exercises.
order = Order()
# => Keeps this domain step explicit and reviewable.
order.place()
# => Proves the stated business rule is observable.
assert order.pending_events == ["OrderPlaced"]
