"""Example 80: pytest verification that the system extends without editing any closed class."""

from example import (
    LoggingPricingEngine,
    MemberDiscountPricing,
    PricingEngine,
    ReceiptPrinter,
    StandardPricing,
    make_pricing_strategy,
)


def test_factory_chooses_the_correct_strategy_by_membership() -> None:
    assert isinstance(make_pricing_strategy(is_member=True), MemberDiscountPricing)
    assert isinstance(make_pricing_strategy(is_member=False), StandardPricing)


def test_engine_notifies_registered_listeners_on_every_order() -> None:
    engine = PricingEngine()
    receipts = ReceiptPrinter()
    engine.add_listener(receipts)
    engine.place_order(100.0, StandardPricing())
    assert receipts.receipts == ["receipt: $100.00"]


def test_a_second_listener_registers_without_editing_pricing_engine() -> None:
    engine = PricingEngine()
    first = ReceiptPrinter()
    second = ReceiptPrinter()
    engine.add_listener(first)
    engine.add_listener(second)  # => a SECOND listener, zero edits to PricingEngine's source
    engine.place_order(50.0, StandardPricing())
    assert first.receipts == ["receipt: $50.00"]
    assert second.receipts == ["receipt: $50.00"]


def test_decorator_logs_every_total_without_touching_pricing_engine() -> None:
    logging_engine = LoggingPricingEngine(PricingEngine())
    logging_engine.place_order(100.0, StandardPricing())
    logging_engine.place_order(100.0, MemberDiscountPricing())
    assert logging_engine.log == [100.0, 85.0]  # => decorator observed both, from OUTSIDE the closed class


def test_full_stack_strategy_factory_observer_decorator_work_together() -> None:
    logging_engine = LoggingPricingEngine(PricingEngine())
    receipts = ReceiptPrinter()
    logging_engine.add_listener(receipts)
    total = logging_engine.place_order(200.0, make_pricing_strategy(is_member=True))
    assert total == 170.0
    assert receipts.receipts == ["receipt: $170.00"]
    assert logging_engine.log == [170.0]


# => Run: pytest -q -- Output: 5 passed
