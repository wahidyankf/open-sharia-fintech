"""Example 17: Guard Against Overdrafting on Withdraw."""


class BankAccount:  # => begins the BankAccount class body
    def __init__(
        self, opening_balance: float = 0.0
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self._balance: float = opening_balance  # => stores _balance on this instance

    def withdraw(self, amount: float) -> float:  # => defines the withdraw() method
        if (
            amount > self._balance
        ):  # => guards the invariant: balance never goes negative
            raise ValueError(
                "insufficient funds"
            )  # => rejects the overdrawing call entirely
        self._balance -= amount  # => only reached when funds are sufficient
        return self._balance  # => returns this value to the caller

    @property  # => marks the next method as a computed attribute
    def balance(self) -> float:  # => defines the balance() method
        return self._balance  # => returns this value to the caller


account: BankAccount = BankAccount(opening_balance=50.0)  # => constructs account
try:  # => the block below is expected to raise
    account.withdraw(100.0)  # => exceeds the current balance -- should be rejected
except ValueError:  # => catches the ValueError raised above
    pass  # => the raise itself is the assertion; balance must remain untouched below
print(account.balance)  # => confirms the rejected withdrawal left balance unchanged
# => Output: 50.0
# => A rejected mutation must leave state exactly as it was
