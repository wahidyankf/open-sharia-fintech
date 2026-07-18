"""Example 38: pytest verification for Coercion on Store."""

import datetime

from example import coerce_bool_on_store, coerce_date_on_store


def test_true_coerces_to_one() -> None:
    assert coerce_bool_on_store(True) == 1  # => driver-native int form


def test_false_coerces_to_zero() -> None:
    assert coerce_bool_on_store(False) == 0  # => driver-native int form


def test_date_coerces_to_iso_string() -> None:
    result = coerce_date_on_store(datetime.date(2026, 12, 25))  # => a fixed calendar date
    assert result == "2026-12-25"  # => driver-native TEXT form, ISO 8601


# => Run: pytest -- Output: 3 passed
