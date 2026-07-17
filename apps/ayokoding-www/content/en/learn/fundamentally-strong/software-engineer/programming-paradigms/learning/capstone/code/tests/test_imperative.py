"""Tests for the imperative Sequential Transaction Processor."""

from paradigms.imperative import process_transactions_imperative


def test_matches_the_shared_expected_result() -> None:
    balance, rejected = process_transactions_imperative([50, -200, 30, -1000, 20], starting_balance=100)
    assert (balance, rejected) == (200, [1, 3])  # => the one expected result every paradigm must match


def test_a_transaction_that_exactly_zeroes_the_balance_is_accepted() -> None:
    balance, rejected = process_transactions_imperative([-100], starting_balance=100)
    assert (balance, rejected) == (0, [])  # => landing exactly at zero is NOT rejected, only negative is


def test_an_empty_transaction_list_returns_the_starting_balance_unchanged() -> None:
    assert process_transactions_imperative([], starting_balance=42) == (42, [])
