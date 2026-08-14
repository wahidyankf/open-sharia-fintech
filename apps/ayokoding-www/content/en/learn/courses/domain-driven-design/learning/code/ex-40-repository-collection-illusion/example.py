"""Example 40: a repository hides its storage mechanism."""


class Orders:
    def __init__(self) -> None:
        self._items: dict[str, str] = {}

    def add(self, value: str) -> None:
        self._items[value] = value  # => collection-style write

    def __getitem__(self, key: str) -> str:
        return self._items[key]  # => collection-style read


orders = Orders()
orders.add("o-1")
assert orders["o-1"] == "o-1"
