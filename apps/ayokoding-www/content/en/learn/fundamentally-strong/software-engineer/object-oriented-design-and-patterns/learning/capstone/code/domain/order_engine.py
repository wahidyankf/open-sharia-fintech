"""Capstone Step 2 + 3: OrderEngine -- SOLID refactor of OrderEngineSmelly, plus Strategy + factory + Observer.

co-01 (SRP): OrderEngine handles item management and checkout orchestration ONLY -- pricing
is delegated to a DiscountStrategy, notification is delegated to observers.
co-02 (OCP): a new discount rule registers into `_DISCOUNT_REGISTRY` via
`register_discount_strategy` -- OrderEngine.checkout() is never edited to add one.
co-05 (DIP): `checkout()` depends on the `DiscountStrategy` PROTOCOL, never a concrete class.
co-16 (factory): `make_discount_strategy` centralizes strategy selection by name.
co-25 (Strategy): `DiscountStrategy` and its implementations are the classic Strategy shape.
co-26 (Observer): `OrderPlacedObserver` decouples OrderEngine from whatever reacts to a checkout.
"""

from __future__ import annotations

from typing import Protocol


class DiscountStrategy(Protocol):  # => co-25: the Strategy interface every discount rule implements
    def apply(self, subtotal: float) -> float: ...


class NoDiscount:
    def apply(self, subtotal: float) -> float:
        return subtotal


class TenPercentOff:
    def apply(self, subtotal: float) -> float:
        return subtotal * 0.90


class BuyOneGetOneFree:
    def apply(self, subtotal: float) -> float:
        return subtotal * 0.50


# => co-02 + co-16: a REGISTRY, not a fixed if/elif -- new strategies are pure additions
_DISCOUNT_REGISTRY: dict[str, DiscountStrategy] = {
    "none": NoDiscount(),
    "ten_percent": TenPercentOff(),
    "bogo": BuyOneGetOneFree(),
}


def register_discount_strategy(name: str, strategy: DiscountStrategy) -> None:  # => co-02: the OCP extension point
    _DISCOUNT_REGISTRY[name] = strategy


def make_discount_strategy(name: str) -> DiscountStrategy:  # => co-16: the factory -- callers never construct directly
    if name not in _DISCOUNT_REGISTRY:
        raise ValueError(f"unknown discount type {name!r}")
    return _DISCOUNT_REGISTRY[name]


class OrderPlacedObserver(Protocol):  # => co-26: the Observer interface -- OrderEngine never imports a concrete listener
    def on_order_placed(self, total: float) -> None: ...


class OrderEngine:  # => co-01: SRP -- item management + checkout orchestration ONLY
    def __init__(self) -> None:
        self._items: dict[str, float] = {}
        self._observers: list[OrderPlacedObserver] = []

    def add_item(self, name: str, price: float) -> None:
        self._items[name] = price

    def add_observer(self, observer: OrderPlacedObserver) -> None:  # => co-02: a new listener needs no edit here
        self._observers.append(observer)

    def checkout(self, discount: DiscountStrategy) -> float:  # => co-05: depends on the ABSTRACT strategy
        subtotal = sum(self._items.values())
        total = discount.apply(subtotal)  # => co-25: delegates the varying part entirely
        for observer in self._observers:  # => co-26: notifies every registered observer, none hard-coded
            observer.on_order_placed(total)
        return total
