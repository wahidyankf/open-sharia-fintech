"""Example 15: Encapsulate a Bank Balance."""


class BankAccount:  # => begins the BankAccount class body
    def __init__(
        self, opening_balance: float = 0.0
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self._balance: float = (
            opening_balance  # => single leading underscore: internal state
        )

    def deposit(
        self, amount: float
    ) -> float:  # => the ONLY sanctioned way to grow _balance
        self._balance += amount  # => mutates the guarded field
        return self._balance  # => returns the new balance for convenience

    @property  # => marks the next method as a computed attribute
    def balance(
        self,
    ) -> float:  # => read access without exposing the raw field for writes
        return self._balance  # => returns this value to the caller


account: BankAccount = BankAccount()  # => constructs account
new_balance: float = account.deposit(
    100.0
)  # => routes the mutation through the guarded method
print(new_balance, account.balance)  # => both reflect the SAME underlying _balance
# => Output: 100.0 100.0
# => Routing every mutation of `_balance` through `deposit()` means the invariant "balance changes only through sanctioned methods" holds by construction, not by convention alone
