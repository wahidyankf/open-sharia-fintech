"""Worked Example 8: keep presentation dependent on a repository contract."""

from typing import Protocol


class OrderReader(Protocol):
    def get(self, order_id: str) -> str: ...


class MemoryOrders:
    def get(self, order_id: str) -> str:
        return "paid"


def render_order(repository: OrderReader, order_id: str) -> str:
    return f"Order {order_id}: {repository.get(order_id)}"


print(render_order(MemoryOrders(), "order-1"))
