"""Capstone: pytest coverage for Account's encapsulated balance invariant."""

import pytest

from domain.account import Account
from domain.money import Money


def test_account_deposit_increases_balance() -> None:
    account: Account = Account("Alice", Money(1000))
    account.deposit(Money(500))
    assert account.balance == Money(1500)  # => the only sanctioned way balance grows


def test_account_withdraw_decreases_balance() -> None:
    account: Account = Account("Alice", Money(1000))
    account.withdraw(Money(400))
    assert account.balance == Money(600)  # => the only sanctioned way balance shrinks


def test_account_rejects_overdraft() -> None:
    account: Account = Account("Alice", Money(100))
    with pytest.raises(
        ValueError
    ):  # => co-17: the core invariant -- no overdraft, ever
        account.withdraw(Money(200))


def test_account_rejects_negative_opening_balance() -> None:
    with pytest.raises(
        ValueError
    ):  # => Money itself rejects this before Account even runs
        Account("Alice", Money(-50))


def test_account_rejects_non_positive_deposit() -> None:
    account: Account = Account("Alice", Money(100))
    with pytest.raises(
        ValueError
    ):  # => co-17: the same guard fires on the deposit path too
        account.deposit(Money(0))


def test_account_rejects_mismatched_currency_withdraw() -> None:
    account: Account = Account("Alice", Money(1000, "USD"))
    with pytest.raises(
        ValueError
    ):  # => co-17: withdraw guards currency match too, same as deposit does via Money.__add__
        account.withdraw(Money(500, "JPY"))


# => Run: pytest -- Output: 6 passed
