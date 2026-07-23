"""Capstone Step 3: LoggingOrderEngine -- a Decorator adding an audit log around the CLOSED OrderEngine.

co-21 (Decorator): wraps OrderEngine and forwards its interface, adding a cross-cutting
audit log without a single edit to order_engine.py.
"""

from __future__ import annotations

from domain.order_engine import DiscountStrategy, OrderEngine, OrderPlacedObserver


class LoggingOrderEngine:  # => co-21: adds an audit log around the CLOSED OrderEngine, from outside
    def __init__(self, wrapped: OrderEngine) -> None:
        self._wrapped = wrapped
        self.audit_log: list[float] = []

    def add_item(self, name: str, price: float) -> None:
        self._wrapped.add_item(name, price)

    def add_observer(self, observer: OrderPlacedObserver) -> None:
        self._wrapped.add_observer(observer)

    def checkout(self, discount: DiscountStrategy) -> float:
        total = self._wrapped.checkout(discount)
        self.audit_log.append(total)  # => the cross-cutting concern, bolted on from OUTSIDE OrderEngine
        return total
