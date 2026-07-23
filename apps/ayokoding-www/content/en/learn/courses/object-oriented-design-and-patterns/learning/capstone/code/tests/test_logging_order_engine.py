"""Capstone Step 3: pytest coverage for the LoggingOrderEngine decorator."""

from domain.logging_order_engine import LoggingOrderEngine
from domain.notifications import NotificationLog
from domain.order_engine import NoDiscount, OrderEngine, TenPercentOff


def test_decorator_preserves_checkout_totals() -> None:
    logging_engine = LoggingOrderEngine(OrderEngine())
    logging_engine.add_item("Book", 20.0)
    assert logging_engine.checkout(NoDiscount()) == 20.0


def test_decorator_adds_an_audit_log_without_touching_order_engine() -> None:
    logging_engine = LoggingOrderEngine(OrderEngine())
    logging_engine.add_item("Book", 20.0)
    logging_engine.add_item("Pen", 5.0)
    logging_engine.checkout(NoDiscount())
    logging_engine.checkout(TenPercentOff())
    assert logging_engine.audit_log == [25.0, 22.5]  # => the decorator observed both totals, from OUTSIDE OrderEngine


def test_decorator_forwards_observers_to_the_wrapped_engine() -> None:
    log = NotificationLog()
    logging_engine = LoggingOrderEngine(OrderEngine())
    logging_engine.add_observer(log)  # => forwarded transparently to the wrapped OrderEngine
    logging_engine.add_item("Book", 20.0)
    logging_engine.checkout(NoDiscount())
    assert log.messages == ["order checked out: total 20.00"]  # => the wrapped engine's own observer still fired


# => Run: pytest -q -- Output: 3 passed
