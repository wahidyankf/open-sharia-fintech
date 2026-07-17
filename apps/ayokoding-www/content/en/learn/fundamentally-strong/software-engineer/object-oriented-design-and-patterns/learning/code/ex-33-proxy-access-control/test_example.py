"""Example 33: pytest verification for A Protection Proxy Checks Permission."""

import pytest

from example import BankAccountProxy, RealBankAccount


def test_admin_role_withdrawal_succeeds() -> None:
    account: RealBankAccount = RealBankAccount(balance=1000.0)
    BankAccountProxy(account, role="admin").withdraw(100.0)
    assert account.balance == 900.0  # => the real account was genuinely mutated


def test_guest_role_withdrawal_is_blocked() -> None:
    account: RealBankAccount = RealBankAccount(balance=1000.0)
    with pytest.raises(PermissionError):  # => must raise, never silently succeed
        BankAccountProxy(account, role="guest").withdraw(50.0)
    assert account.balance == 1000.0  # => the blocked call never reached the real account


# => Run: pytest -- Output: 2 passed
