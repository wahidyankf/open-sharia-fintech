"""Kata 3 (after): encapsulation fix -- state hidden behind methods, the invariant can't be bypassed."""


class BankBalance:
    def __init__(self, amount: int) -> None:
        self._balance = amount  # underscore-prefixed -- convention signals "route through methods only"

    def withdraw(self, amount: int) -> bool:
        if self._balance - amount < 0:
            return False
        self._balance -= amount
        return True

    def read(self) -> int:
        return self._balance


account = BankBalance(50)
succeeded = account.withdraw(100)  # the ONLY way to change balance -- and it correctly refuses
print(succeeded)
print(account.read())
