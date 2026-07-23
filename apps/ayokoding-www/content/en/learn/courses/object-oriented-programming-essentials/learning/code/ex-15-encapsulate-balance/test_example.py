"""Example 15: pytest verification for Encapsulate a Bank Balance."""

from example import BankAccount


def test_deposit_raises_reported_balance() -> None:
    account: BankAccount = BankAccount()
    result: float = account.deposit(
        100.0
    )  # => deposit both mutates and returns the new balance
    assert result == 100.0
    assert account.balance == 100.0  # => the read-only property reflects the same state


# => Run: pytest -- Output: 1 passed
