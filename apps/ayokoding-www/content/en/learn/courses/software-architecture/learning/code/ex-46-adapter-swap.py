# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 46: keep policy independent of a storage implementation."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from typing import Protocol


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class Store(Protocol):
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def save(self, order_id: str) -> None: ...


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def place(store: Store, order_id: str) -> None:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    store.save(order_id)


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class MemoryStore:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def save(self, order_id: str) -> None:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        print(order_id)


# => This keeps the modeled rule explicit so its trade-off can be inspected.
place(MemoryStore(), "order-1")
