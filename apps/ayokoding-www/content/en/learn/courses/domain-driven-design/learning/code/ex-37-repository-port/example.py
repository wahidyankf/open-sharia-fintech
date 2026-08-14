"""Example 37: the domain owns a repository capability."""

from typing import Protocol


class OrderRepository(Protocol):
    def add(
        self, order_id: str
    ) -> None: ...  # => port names the required persistence operation
    def get(
        self, order_id: str
    ) -> str: ...  # => implementation remains outside the domain


print(OrderRepository.__name__)  # => Output: OrderRepository
