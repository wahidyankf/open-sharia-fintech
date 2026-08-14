"""Example 38: a dictionary is an adapter for the repository port."""


class MemoryOrders:
    def __init__(self) -> None:
        self._items: dict[str, str] = {}

    def add(self, order_id: str) -> None:
        self._items[order_id] = order_id  # => storage detail stays here

    def get(self, order_id: str) -> str:
        return self._items[order_id]  # => round trip behaviour


repo = MemoryOrders()
repo.add("o-1")
assert repo.get("o-1") == "o-1"
