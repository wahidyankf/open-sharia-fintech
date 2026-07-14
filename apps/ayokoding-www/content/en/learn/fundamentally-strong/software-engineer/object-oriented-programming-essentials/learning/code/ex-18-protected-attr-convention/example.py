"""Example 18: The Single-Underscore Convention."""


class BankAccount:  # => begins the BankAccount class body
    def __init__(
        self, opening_balance: float = 0.0
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self._balance: float = (
            opening_balance  # => single underscore: "internal, do not touch"
        )


account: BankAccount = BankAccount(75.0)  # => constructs account
print(account._balance)  # => TECHNICALLY reachable -- Python enforces nothing here
# => Output: 75.0
# => `_name` communicates "internal" to every reader of the code, but Python performs no access check at all
