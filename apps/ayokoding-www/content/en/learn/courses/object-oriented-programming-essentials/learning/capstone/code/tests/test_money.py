"""Capstone: pytest coverage for Money's invariant and eq/hash contract."""

import pytest

from domain.money import Money


def test_money_equal_amounts_compare_equal() -> None:
    assert Money(500) == Money(500)  # => co-05: value equality, not identity


def test_money_is_hashable_and_dedups_in_a_set() -> None:
    assert (
        len({Money(500), Money(500), Money(300)}) == 2
    )  # => frozen -> auto __hash__ alongside __eq__


def test_money_rejects_negative_amount() -> None:
    with pytest.raises(
        ValueError
    ):  # => co-17: __post_init__ rejects this before construction completes
        Money(-1)


def test_money_rejects_bad_currency_code() -> None:
    with pytest.raises(
        ValueError
    ):  # => co-17: the second invariant -- currency must be 3 letters
        Money(100, "US")


def test_money_add_combines_same_currency() -> None:
    assert Money(200) + Money(300) == Money(
        500
    )  # => __add__ returns a NEW, still-valid Money


def test_money_add_rejects_mismatched_currency() -> None:
    with pytest.raises(ValueError):  # => guards against silently mixing currencies
        _ = Money(200, "USD") + Money(
            300, "EUR"
        )  # => discarding the result -- only the raise matters


# => Run: pytest -- Output: 6 passed
