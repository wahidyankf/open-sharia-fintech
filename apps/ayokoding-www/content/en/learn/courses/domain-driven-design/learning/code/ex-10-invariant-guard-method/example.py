# => Keeps this domain step explicit and reviewable.
"""Example 10: a guard keeps an account non-negative."""


# => Gives domain rules a single, named home.
class Account:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, balance: int) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.balance = balance

    # => Names policy so callers do not recreate the rule.
    def withdraw(self, amount: int) -> None:
        if amount > self.balance:  # => the root checks before changing state
            # => Stops invalid business state at the boundary.
            raise ValueError("insufficient funds")
        self.balance -= amount  # => every reachable balance remains non-negative


# => Keeps scenario data close to the rule it exercises.
account = Account(10)
# => Separates the expected failure path from valid flow.
try:
    # => Keeps this domain step explicit and reviewable.
    account.withdraw(11)
# => Turns the rejected case into an explicit outcome.
except ValueError:
    pass  # => rejection preserves the valid prior state
assert account.balance == 10  # => the invariant still holds
