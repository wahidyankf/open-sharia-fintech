"""Example 39: each root has a collection-shaped repository."""


class Repository:
    def __init__(self) -> None:
        self.items: dict[str, object] = {}

    def add(self, id: str, item: object) -> None:
        self.items[id] = item


orders, customers = (
    Repository(),
    Repository(),
)  # => separate collections protect separate root lifecycles
orders.add("o-1", object())
customers.add("c-1", object())
assert set(orders.items) == {"o-1"} and set(customers.items) == {"c-1"}
