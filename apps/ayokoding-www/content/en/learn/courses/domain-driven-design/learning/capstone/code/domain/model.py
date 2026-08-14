"""Tactical DDD model: values, an aggregate root, and a repository port."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("quantity must be positive")


@dataclass(frozen=True)
class Money:
    cents: int

    def __post_init__(self) -> None:
        if self.cents < 0:
            raise ValueError("money cannot be negative")


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str
    total: Money


class Order:
    """Aggregate root: all line changes and the credit invariant enter here."""

    def __init__(self, order_id: str, credit_limit: Money) -> None:
        self.order_id = order_id
        self._credit_limit = credit_limit
        self._lines: list[tuple[Quantity, Money]] = []
        self.pending_events: list[OrderPlaced] = []

    @property
    def total(self) -> Money:
        return Money(
            sum(quantity.value * price.cents for quantity, price in self._lines)
        )

    @property
    def lines(self) -> tuple[tuple[Quantity, Money], ...]:
        return tuple(self._lines)

    def add_line(self, quantity: Quantity, unit_price: Money) -> None:
        next_total = self.total.cents + quantity.value * unit_price.cents
        if next_total > self._credit_limit.cents:
            raise ValueError("credit limit exceeded")
        self._lines.append((quantity, unit_price))

    def place(self) -> None:
        if not self._lines:
            raise ValueError("order needs a line")
        self.pending_events.append(OrderPlaced(self.order_id, self.total))


class OrderRepository(Protocol):
    def add(self, order: Order) -> None: ...
    def get(self, order_id: str) -> Order: ...
