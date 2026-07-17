"""Example 76: pytest verification for Refactoring Shared-Mutable Code to Pass State Explicitly."""

from example import deposit_pure


def test_explicit_state_threading_needs_no_global_reset_between_tests() -> None:
    balance = deposit_pure(0, 100)
    balance = deposit_pure(balance, 50)
    assert (
        balance == 150
    )  # => reproducible without resetting any module-level global first


# => Run: pytest -- Output: 1 passed
