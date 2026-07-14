"""Example 16: Reject a Negative Deposit."""


class BankAccount:  # => begins the BankAccount class body
    def __init__(
        self, opening_balance: float = 0.0
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self._balance: float = opening_balance  # => stores _balance on this instance

    def deposit(self, amount: float) -> float:  # => defines the deposit() method
        if amount < 0:  # => guards the invariant: a deposit can never be negative
            raise ValueError(
                "deposit amount must be non-negative"
            )  # => rejects the whole call
        self._balance += amount  # => only reached when the amount passed validation
        return self._balance  # => returns this value to the caller

    @property  # => marks the next method as a computed attribute
    def balance(self) -> float:  # => defines the balance() method
        return self._balance  # => returns this value to the caller


account: BankAccount = BankAccount()  # => constructs account
try:  # => the block below is expected to raise
    account.deposit(-10.0)  # => triggers the guard above
except ValueError as exc:  # => catches the raised exception to demonstrate it fired
    print(exc)  # => prints the exact message the guard raised
# => Output: deposit amount must be non-negative
# => `pytest.raises(ValueError)` turns "this call must fail" into a first-class, passing assertion
