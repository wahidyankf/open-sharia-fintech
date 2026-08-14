"""Worked Example 10: declare a policy-owned storage port."""

from typing import Protocol


class OrderStore(Protocol):
    def save(self, order_id: str) -> None: ...
