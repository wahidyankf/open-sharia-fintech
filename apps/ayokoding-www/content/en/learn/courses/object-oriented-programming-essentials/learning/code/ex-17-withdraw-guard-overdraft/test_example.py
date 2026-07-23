"""Example 17: pytest verification for Guard Against Overdrafting on Withdraw."""

import pytest

from example import BankAccount


def test_overdraw_is_rejected_and_balance_unchanged() -> None:
    account: BankAccount = BankAccount(opening_balance=50.0)
    with pytest.raises(ValueError):
        account.withdraw(100.0)  # => more than the current balance
    assert account.balance == 50.0  # => the rejected call left state untouched


# => Run: pytest -- Output: 1 passed
