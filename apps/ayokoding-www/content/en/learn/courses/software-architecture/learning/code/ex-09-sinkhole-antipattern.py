"""Worked Example 9: show a pass-through layer with no policy."""

from typing import Protocol


class OrderReader(Protocol):
    def get(self, order_id: str) -> str: ...


def service_get(order_id: str, repository: OrderReader) -> str:
    return repository.get(order_id)
