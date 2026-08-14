# => Keeps this domain step explicit and reviewable.
"""Example 40: a repository hides its storage mechanism."""


# => Gives domain rules a single, named home.
class Orders:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self._items: dict[str, str] = {}

    # => Names policy so callers do not recreate the rule.
    def add(self, value: str) -> None:
        self._items[value] = value  # => collection-style write

    # => Names policy so callers do not recreate the rule.
    def __getitem__(self, key: str) -> str:
        return self._items[key]  # => collection-style read


# => Keeps scenario data close to the rule it exercises.
orders = Orders()
# => Keeps this domain step explicit and reviewable.
orders.add("o-1")
# => Proves the stated business rule is observable.
assert orders["o-1"] == "o-1"
