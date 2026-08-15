# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 9: show a pass-through layer with no policy."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from typing import Protocol


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class OrderReader(Protocol):
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def get(self, order_id: str) -> str: ...


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def service_get(order_id: str, repository: OrderReader) -> str:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return repository.get(order_id)
