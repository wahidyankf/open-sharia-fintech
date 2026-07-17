"""Example 78: pytest verification of all three pattern-or-not scenarios."""

from example import (
    BuyOneGetOneFree,
    NoDiscount,
    TenPercentOff,
    checkout_total,
    convert_report_to_csv_line,
    format_welcome_email,
)


def test_scenario_1_plain_function_is_sufficient_with_no_second_variant_in_sight() -> None:
    assert format_welcome_email("Ada") == "Welcome, Ada!"  # => no Strategy needed for a single, stable format


def test_scenario_2_strategy_pattern_earns_its_keep_with_three_real_variants_today() -> None:
    assert checkout_total(100.0, NoDiscount()) == 100.0
    assert checkout_total(100.0, TenPercentOff()) == 90.0
    assert checkout_total(100.0, BuyOneGetOneFree()) == 50.0  # => three DISTINCT verdicts, justifying the interface


def test_scenario_3_plain_function_is_sufficient_for_a_one_off_throwaway_script() -> None:
    assert convert_report_to_csv_line(["2026-07-17", "42", "ok"]) == "2026-07-17,42,ok"  # => no Converter interface needed


# => Run: pytest -q -- Output: 3 passed
