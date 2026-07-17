"""Example 7: pytest verification for Encapsulation Private State."""

import pytest

from example import BankBalance


def test_deposit_and_withdraw_change_balance_through_the_api() -> None:
    account = BankBalance(100)  # => fresh account, isolated from the module-level demo
    account.deposit(50)  # => via the sanctioned method
    account.withdraw(30)  # => via the sanctioned method
    assert account.read() == 120  # => 100 + 50 - 30


def test_invariant_holds_after_a_rejected_withdrawal() -> None:
    account = BankBalance(100)  # => fresh account
    with pytest.raises(ValueError):  # => the guard must refuse an over-large withdrawal
        account.withdraw(9999)
    assert account.read() == 100  # => the invariant held -- balance is unchanged by the rejection


# => Run: pytest -- Output: 2 passed
