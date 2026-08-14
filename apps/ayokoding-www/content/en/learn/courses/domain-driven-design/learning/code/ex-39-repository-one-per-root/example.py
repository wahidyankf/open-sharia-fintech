# => Keeps this domain step explicit and reviewable.
"""Example 39: each root has a collection-shaped repository."""


# => Gives domain rules a single, named home.
class Repository:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.items: dict[str, object] = {}

    # => Names policy so callers do not recreate the rule.
    def add(self, id: str, item: object) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.items[id] = item


# => Keeps this domain step explicit and reviewable.
orders, customers = (
    # => Keeps this domain step explicit and reviewable.
    Repository(),
    # => Keeps this domain step explicit and reviewable.
    Repository(),
)  # => separate collections protect separate root lifecycles
# => Keeps this domain step explicit and reviewable.
orders.add("o-1", object())
# => Keeps this domain step explicit and reviewable.
customers.add("c-1", object())
# => Proves the stated business rule is observable.
assert set(orders.items) == {"o-1"} and set(customers.items) == {"c-1"}
