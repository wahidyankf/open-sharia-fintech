"""Worked Example 46: keep policy independent of a storage implementation."""

from typing import Protocol


class Store(Protocol):
    def save(self, order_id: str) -> None: ...


def place(store: Store, order_id: str) -> None:
    store.save(order_id)


class MemoryStore:
    def save(self, order_id: str) -> None:
        print(order_id)


place(MemoryStore(), "order-1")
