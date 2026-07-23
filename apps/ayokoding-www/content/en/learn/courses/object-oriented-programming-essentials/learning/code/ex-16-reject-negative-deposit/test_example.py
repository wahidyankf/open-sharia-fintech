"""Example 16: pytest verification for Reject a Negative Deposit."""

import pytest  # => pytest.raises asserts a specific exception is raised

from example import BankAccount


def test_negative_deposit_raises_value_error() -> None:
    account: BankAccount = BankAccount()
    with pytest.raises(ValueError):  # => the test PASSES only because ValueError fires
        account.deposit(-10.0)  # => the call expected to raise


# => Run: pytest -- Output: 1 passed
