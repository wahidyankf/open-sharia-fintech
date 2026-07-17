"""Kata 3 (before): encapsulation violation -- direct field mutation bypasses the never-negative invariant."""


class BankBalance:
    def __init__(self, amount: int) -> None:
        self.balance = amount  # SMELL: public field -- nothing stops direct mutation

    def withdraw(self, amount: int) -> bool:
        if self.balance - amount < 0:
            return False
        self.balance -= amount
        return True


account = BankBalance(50)
account.balance = account.balance - 100  # BUG: bypasses withdraw()'s guard entirely
print(account.balance)
