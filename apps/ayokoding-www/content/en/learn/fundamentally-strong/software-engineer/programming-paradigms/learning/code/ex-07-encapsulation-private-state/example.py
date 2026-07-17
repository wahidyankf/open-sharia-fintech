"""Example 7: Encapsulation Private State."""


class BankBalance:  # => the invariant we protect: balance never goes negative
    def __init__(self, opening: int) -> None:  # => constructor establishes the invariant up front
        if opening < 0:  # => guard: reject an invalid starting state immediately
            raise ValueError("opening balance cannot be negative")  # => refuse to construct
        self._balance: int = opening  # => hidden behind a single underscore -- "internal, don't touch"

    def deposit(self, amount: int) -> None:  # => the ONLY sanctioned way to increase the balance
        if amount < 0:  # => guard against a "negative deposit" that would secretly withdraw
            raise ValueError("deposit amount cannot be negative")
        self._balance += amount  # => the sole line that increases _balance

    def withdraw(self, amount: int) -> None:  # => the ONLY sanctioned way to decrease the balance
        if amount > self._balance:  # => guard: this is what keeps the invariant intact
            raise ValueError("insufficient funds")  # => refuse rather than let balance go negative
        self._balance -= amount  # => the sole line that decreases _balance

    def read(self) -> int:  # => the ONLY sanctioned way to observe the balance from outside
        return self._balance  # => callers never touch _balance directly


account = BankBalance(100)  # => open with 100
account.deposit(50)  # => goes through the guarded method
account.withdraw(30)  # => goes through the guarded method
print(account.read())  # => 100 + 50 - 30 = 120
# => Output: 120

try:  # => attempt to violate the invariant via the sanctioned API
    account.withdraw(9999)  # => far more than the current balance
except ValueError as exc:  # => the guard inside withdraw() catches it before _balance is touched
    print(f"blocked: {exc}")  # => the invariant held -- balance is untouched by the rejected call
# => Output: blocked: insufficient funds
print(account.read())  # => confirms the rejected withdrawal never touched _balance
# => Output: 120
