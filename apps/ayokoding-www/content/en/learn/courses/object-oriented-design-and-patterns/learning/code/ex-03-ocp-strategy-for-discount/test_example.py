"""Example 3: pytest verification for Replace an If/Elif Chain with Strategy Objects."""

import inspect

from example import Checkout, HolidayDiscount, LoyaltyDiscount, NoDiscount


def test_checkout_source_never_names_a_concrete_discount() -> None:
    source: str = inspect.getsource(Checkout)  # => reads Checkout's own source text, nothing else
    # => none of the three concrete strategy class names appear inside Checkout
    assert "NoDiscount" not in source
    assert "LoyaltyDiscount" not in source
    assert "HolidayDiscount" not in source  # => proves zero edits were needed to add it


def test_each_strategy_computes_its_own_price() -> None:
    assert Checkout(NoDiscount()).total(100.0) == 100.0
    assert Checkout(LoyaltyDiscount()).total(100.0) == 90.0
    assert Checkout(HolidayDiscount()).total(100.0) == 75.0  # => added with no edits


# => Run: pytest -- Output: 2 passed
