# => Keeps this domain step explicit and reviewable.
"""Example 22: a cross-account operation is a domain service."""


# => Gives domain rules a single, named home.
class Account:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, balance: int) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.balance = balance


# => Names policy so callers do not recreate the rule.
def transfer(source: Account, target: Account, amount: int) -> None:
    # => Checks policy before a state change is allowed.
    if source.balance < amount:
        raise ValueError("insufficient funds")  # => validate before either change
    # => Keeps this domain step explicit and reviewable.
    source.balance -= amount
    target.balance += amount  # => both balances change as one operation


# => Keeps this domain step explicit and reviewable.
a, b = Account(10), Account(0)
# => Keeps this domain step explicit and reviewable.
transfer(a, b, 4)
# => Proves the stated business rule is observable.
assert (a.balance, b.balance) == (6, 4)
