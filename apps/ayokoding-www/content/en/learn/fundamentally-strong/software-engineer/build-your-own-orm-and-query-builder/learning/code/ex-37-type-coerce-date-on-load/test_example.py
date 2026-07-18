"""Example 37: pytest verification for Date Coercion on Load."""

import datetime

from example import coerce_date_on_load


def test_iso_string_coerces_to_date_instance() -> None:
    result = coerce_date_on_load("2026-07-04")  # => a well-formed ISO date string
    assert isinstance(result, datetime.date)  # => a real date object, not a string
    assert result == datetime.date(2026, 7, 4)  # => the exact calendar date


def test_year_month_day_fields_are_correct() -> None:
    result = coerce_date_on_load("1999-12-31")  # => an end-of-year edge case
    assert (result.year, result.month, result.day) == (1999, 12, 31)  # => every field parsed correctly


# => Run: pytest -- Output: 2 passed
