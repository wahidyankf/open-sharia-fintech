# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 8: keep presentation dependent on a repository contract."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from typing import Protocol


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class OrderReader(Protocol):
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def get(self, order_id: str) -> str: ...


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class MemoryOrders:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def get(self, order_id: str) -> str:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        return "paid"


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def render_order(repository: OrderReader, order_id: str) -> str:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return f"Order {order_id}: {repository.get(order_id)}"


# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(render_order(MemoryOrders(), "order-1"))
