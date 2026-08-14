"""Example 41: callers depend on the port, not a storage detail."""

from typing import Protocol


class Store(Protocol):
    def save(self, value: str) -> None: ...


class Memory:
    def __init__(self) -> None:
        self.value = ""

    def save(self, value: str) -> None:
        self.value = value  # => fake adapter implements the same port


def persist(store: Store) -> None:
    store.save("order")  # => domain caller names only the port


memory = Memory()
persist(memory)
assert memory.value == "order"
