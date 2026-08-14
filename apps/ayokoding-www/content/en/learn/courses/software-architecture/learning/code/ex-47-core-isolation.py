"""Worked Example 47: a fake adapter captures an observable effect."""


class FakeStore:
    def __init__(self) -> None:
        self.saved: list[str] = []

    def save(self, order_id: str) -> None:
        self.saved.append(order_id)


store = FakeStore()
store.save("order-1")
assert store.saved == ["order-1"]
