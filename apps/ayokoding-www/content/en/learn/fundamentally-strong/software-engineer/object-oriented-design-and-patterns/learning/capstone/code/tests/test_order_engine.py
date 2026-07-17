"""Capstone Step 2 + 3: pytest coverage for the refactored OrderEngine, matching the pinning suite's
scenarios plus new extensibility proofs (OCP: new strategy/observer added without editing OrderEngine).
"""

import pytest

from domain.order_engine import (
    BuyOneGetOneFree,
    DiscountStrategy,
    NoDiscount,
    OrderEngine,
    TenPercentOff,
    make_discount_strategy,
    register_discount_strategy,
)


def test_checkout_with_no_discount_matches_the_pinned_smelly_behavior() -> None:
    engine = OrderEngine()
    engine.add_item("Book", 20.0)
    engine.add_item("Pen", 5.0)
    assert engine.checkout(NoDiscount()) == 25.0  # => SAME result as OrderEngineSmelly.checkout("none")


def test_checkout_with_ten_percent_off_matches_the_pinned_smelly_behavior() -> None:
    engine = OrderEngine()
    engine.add_item("Book", 20.0)
    engine.add_item("Pen", 5.0)
    assert engine.checkout(TenPercentOff()) == 22.5  # => SAME result as OrderEngineSmelly.checkout("ten_percent")


def test_checkout_with_bogo_matches_the_pinned_smelly_behavior() -> None:
    engine = OrderEngine()
    engine.add_item("Book", 20.0)
    engine.add_item("Pen", 5.0)
    assert engine.checkout(BuyOneGetOneFree()) == 12.5  # => SAME result as OrderEngineSmelly.checkout("bogo")


def test_factory_looks_up_the_correct_strategy_by_name() -> None:
    assert isinstance(make_discount_strategy("none"), NoDiscount)
    assert isinstance(make_discount_strategy("ten_percent"), TenPercentOff)
    assert isinstance(make_discount_strategy("bogo"), BuyOneGetOneFree)


def test_factory_rejects_an_unregistered_discount_name() -> None:
    with pytest.raises(ValueError, match="unknown discount type"):
        make_discount_strategy("nonexistent")


def test_a_new_discount_strategy_registers_without_editing_order_engine_or_the_factory() -> None:
    class ClearancePricing:  # => a NEW strategy, defined entirely in this test, added AFTER the fact
        def apply(self, subtotal: float) -> float:
            return subtotal * 0.25  # => 75% off clearance

    register_discount_strategy("clearance", ClearancePricing())  # => co-02: the OCP extension point in action
    engine = OrderEngine()
    engine.add_item("Book", 100.0)
    assert engine.checkout(make_discount_strategy("clearance")) == 25.0  # => works with ZERO edits to order_engine.py


def test_a_new_observer_registers_without_editing_order_engine() -> None:
    events: list[float] = []

    class ReceiptCollector:  # => a NEW observer, defined entirely in this test
        def on_order_placed(self, total: float) -> None:
            events.append(total)

    engine = OrderEngine()
    engine.add_item("Book", 20.0)
    engine.add_observer(ReceiptCollector())  # => co-26: a SECOND observer type, zero edits to OrderEngine
    engine.checkout(NoDiscount())
    assert events == [20.0]


def test_checkout_notifies_multiple_observers_independently() -> None:
    first: list[float] = []
    second: list[float] = []

    class Collector:
        def __init__(self, sink: list[float]) -> None:
            self._sink = sink

        def on_order_placed(self, total: float) -> None:
            self._sink.append(total)

    engine = OrderEngine()
    engine.add_item("Book", 40.0)
    engine.add_observer(Collector(first))
    engine.add_observer(Collector(second))
    engine.checkout(NoDiscount())
    assert first == [40.0]
    assert second == [40.0]  # => both observers fired independently, from the SAME checkout() call


def test_checkout_depends_on_the_abstract_discount_strategy_protocol() -> None:
    import typing

    hints = typing.get_type_hints(OrderEngine.checkout)  # => resolves the (stringified) annotation back to the real object
    assert hints["discount"] is DiscountStrategy  # => co-05: DIP -- the parameter is typed against the PROTOCOL


# => Run: pytest -q -- Output: 9 passed
