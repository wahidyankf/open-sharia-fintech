"""Example 10: a guard keeps an account non-negative."""


class Account:
    def __init__(self, balance: int) -> None:
        self.balance = balance

    def withdraw(self, amount: int) -> None:
        if amount > self.balance:  # => the root checks before changing state
            raise ValueError("insufficient funds")
        self.balance -= amount  # => every reachable balance remains non-negative


account = Account(10)
try:
    account.withdraw(11)
except ValueError:
    pass  # => rejection preserves the valid prior state
assert account.balance == 10  # => the invariant still holds
