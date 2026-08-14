# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 10: declare a policy-owned storage port."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from typing import Protocol


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class OrderStore(Protocol):
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def save(self, order_id: str) -> None: ...
