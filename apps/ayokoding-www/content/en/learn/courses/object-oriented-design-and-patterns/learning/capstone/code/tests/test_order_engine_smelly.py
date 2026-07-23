"""Capstone Step 1: the PINNING suite -- pins OrderEngineSmelly's current behavior before any refactor.

This suite exists to stay green THROUGHOUT every later refactor step, proving each step
preserves behavior. It is never deleted; `test_order_engine.py` re-proves the same
scenarios against the refactored OrderEngine, so both suites passing side by side is the
evidence that Step 2/3 changed the DESIGN without changing the BEHAVIOR.
"""

import pytest

from domain.order_engine_smelly import OrderEngineSmelly


def test_smelly_checkout_with_no_discount() -> None:
    engine = OrderEngineSmelly()
    engine.add_item("Book", 20.0)
    engine.add_item("Pen", 5.0)
    assert engine.checkout("none") == 25.0


def test_smelly_checkout_with_ten_percent_off() -> None:
    engine = OrderEngineSmelly()
    engine.add_item("Book", 20.0)
    engine.add_item("Pen", 5.0)
    assert engine.checkout("ten_percent") == 22.5


def test_smelly_checkout_with_bogo() -> None:
    engine = OrderEngineSmelly()
    engine.add_item("Book", 20.0)
    engine.add_item("Pen", 5.0)
    assert engine.checkout("bogo") == 12.5


def test_smelly_checkout_records_a_notification() -> None:
    engine = OrderEngineSmelly()
    engine.add_item("Book", 20.0)
    engine.checkout("none")
    assert engine.notifications == ["order checked out: total 20.00"]


def test_smelly_checkout_rejects_an_unknown_discount_type() -> None:
    engine = OrderEngineSmelly()
    engine.add_item("Book", 20.0)
    with pytest.raises(ValueError, match="unknown discount type"):
        engine.checkout("nonexistent")


# => Run: pytest -q -- Output: 5 passed
