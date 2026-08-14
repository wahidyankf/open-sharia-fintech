# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 47: a fake adapter captures an observable effect."""


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class FakeStore:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def __init__(self) -> None:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        self.saved: list[str] = []

    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def save(self, order_id: str) -> None:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        self.saved.append(order_id)


# => This keeps the modeled rule explicit so its trade-off can be inspected.
store = FakeStore()
# => This keeps the modeled rule explicit so its trade-off can be inspected.
store.save("order-1")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert store.saved == ["order-1"]
