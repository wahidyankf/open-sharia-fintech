# => Keeps this domain step explicit and reviewable.
"""Example 38: a dictionary is an adapter for the repository port."""


# => Gives domain rules a single, named home.
class MemoryOrders:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self._items: dict[str, str] = {}

    # => Names policy so callers do not recreate the rule.
    def add(self, order_id: str) -> None:
        self._items[order_id] = order_id  # => storage detail stays here

    # => Names policy so callers do not recreate the rule.
    def get(self, order_id: str) -> str:
        return self._items[order_id]  # => round trip behaviour


# => Keeps scenario data close to the rule it exercises.
repo = MemoryOrders()
# => Keeps this domain step explicit and reviewable.
repo.add("o-1")
# => Proves the stated business rule is observable.
assert repo.get("o-1") == "o-1"
