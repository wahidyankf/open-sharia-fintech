"""Example 18: pytest verification for The Single-Underscore Convention."""

from example import BankAccount


def test_single_underscore_field_is_still_reachable() -> None:
    account: BankAccount = BankAccount(75.0)
    # => a single leading underscore is a NAMING CONVENTION, not enforced access control
    assert (
        account._balance == 75.0
    )  # => still directly accessible, unlike __balance (Example 19)


# => Run: pytest -- Output: 1 passed
