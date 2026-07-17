"""Example 63: pytest verification that behavior moved onto the entity."""

import pytest

from example import AccountService, AnemicAccount, RichAccount


def test_anemic_version_lets_the_invariant_be_bypassed_via_direct_field_access() -> None:
    account = AnemicAccount(balance=100.0)
    account.balance = -50.0  # => NOTHING stops this: the invariant only lives in AccountService.withdraw
    assert account.balance == -50.0  # => the anemic model allows an invalid balance to exist


def test_rich_account_enforces_the_same_invariant_and_cannot_be_bypassed() -> None:
    account = RichAccount(balance=100.0)
    with pytest.raises(AttributeError):  # => balance has no setter -- direct mutation is impossible
        account.balance = -50.0  # type: ignore[misc]  # => deliberately demonstrates the blocked mutation path
    account.withdraw(30.0)  # => the only sanctioned way to change balance
    assert account.balance == 70.0


def test_both_versions_agree_on_a_legal_withdrawal() -> None:
    anemic = AnemicAccount(balance=100.0)
    AccountService().withdraw(anemic, 40.0)
    rich = RichAccount(balance=100.0)
    rich.withdraw(40.0)
    assert anemic.balance == rich.balance == 60.0  # => same math, different ownership of the behavior


# => Run: pytest -q -- Output: 3 passed
