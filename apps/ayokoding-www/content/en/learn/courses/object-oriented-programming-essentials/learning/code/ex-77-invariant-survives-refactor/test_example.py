"""Example 77: pytest verification for An Invariant Still Holds After a Composition Refactor."""

import pytest

from example import BankAccount


def test_valid_deposit_still_works_after_refactor() -> None:
    account: BankAccount = BankAccount()
    assert account.deposit(50.0) == 50.0


def test_invariant_still_cannot_be_violated_after_refactor() -> None:
    account: BankAccount = BankAccount()
    with pytest.raises(
        ValueError
    ):  # => the ORIGINAL invariant, now enforced by a collaborator
        account.deposit(-10.0)


# => Run: pytest -- Output: 2 passed
