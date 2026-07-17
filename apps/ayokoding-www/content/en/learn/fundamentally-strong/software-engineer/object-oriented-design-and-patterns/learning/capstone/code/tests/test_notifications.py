"""Capstone Step 3: pytest coverage for the concrete NotificationLog observer."""

from domain.notifications import NotificationLog
from domain.order_engine import NoDiscount, OrderEngine


def test_notification_log_records_a_formatted_message_on_checkout() -> None:
    engine = OrderEngine()
    engine.add_item("Book", 20.0)
    log = NotificationLog()
    engine.add_observer(log)
    engine.checkout(NoDiscount())
    assert log.messages == ["order checked out: total 20.00"]  # => same message format the smelly baseline pinned


def test_notification_log_accumulates_across_multiple_checkouts() -> None:
    engine = OrderEngine()
    log = NotificationLog()
    engine.add_observer(log)

    engine.add_item("Book", 20.0)
    engine.checkout(NoDiscount())

    engine.add_item("Pen", 5.0)
    engine.checkout(NoDiscount())

    assert log.messages == [
        "order checked out: total 20.00",
        "order checked out: total 25.00",
    ]


# => Run: pytest -q -- Output: 2 passed
