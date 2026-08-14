"""Example 22: a cross-account operation is a domain service."""


class Account:
    def __init__(self, balance: int) -> None:
        self.balance = balance


def transfer(source: Account, target: Account, amount: int) -> None:
    if source.balance < amount:
        raise ValueError("insufficient funds")  # => validate before either change
    source.balance -= amount
    target.balance += amount  # => both balances change as one operation


a, b = Account(10), Account(0)
transfer(a, b, 4)
assert (a.balance, b.balance) == (6, 4)
