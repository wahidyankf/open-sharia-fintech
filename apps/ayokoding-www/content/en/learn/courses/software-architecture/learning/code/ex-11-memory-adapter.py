# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 11: implement the storage port with local memory."""


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class MemoryOrderStore:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def __init__(self) -> None:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        self.ids: list[str] = []

    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def save(self, order_id: str) -> None:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        self.ids.append(order_id)


# => This keeps the modeled rule explicit so its trade-off can be inspected.
store = MemoryOrderStore()
# => This keeps the modeled rule explicit so its trade-off can be inspected.
store.save("order-1")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(store.ids)
