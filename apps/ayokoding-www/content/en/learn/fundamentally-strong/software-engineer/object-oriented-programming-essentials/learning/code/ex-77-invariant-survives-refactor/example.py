"""Example 77: An Invariant Still Holds After a Composition Refactor."""


class Validator:  # => holds the invariant rule as its OWN, testable responsibility
    def check_non_negative(
        self, amount: float
    ) -> None:  # => defines the check_non_negative() method
        if amount < 0:  # => the ORIGINAL invariant, now living in its own collaborator
            raise ValueError(
                "amount must be non-negative"
            )  # => rejects the invalid amount


class BankAccount:  # => now COMPOSED with a Validator, instead of checking inline
    def __init__(
        self,
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self._balance: float = 0.0  # => stores _balance on this instance
        self._validator: Validator = (
            Validator()
        )  # => the invariant now lives in its own object

    def deposit(self, amount: float) -> float:  # => defines the deposit() method
        self._validator.check_non_negative(
            amount
        )  # => delegates the SAME rule as before
        self._balance += amount  # => only reached once the delegated validation passed
        return self._balance  # => returns this value to the caller


account: BankAccount = BankAccount()  # => constructs account
account.deposit(50.0)  # => a valid deposit, routed through the composed Validator
print(account._balance)  # => the happy path still works after the refactor
# => Output: 50.0
# => Refactoring WHERE an invariant lives (from an inline `if` check to a dedicated `Validator` collaborator) is orthogonal to WHETHER the invariant still holds
