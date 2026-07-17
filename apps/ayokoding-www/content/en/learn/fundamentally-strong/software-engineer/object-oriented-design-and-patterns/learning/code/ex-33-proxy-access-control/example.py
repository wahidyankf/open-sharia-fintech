"""Example 33: A Protection Proxy Checks Permission Before Delegating."""


class RealBankAccount:  # => the REAL subject -- has no idea about permissions at all
    def __init__(self, balance: float) -> None:  # => the constructor
        self.balance = balance  # => stores balance on this instance

    def withdraw(self, amount: float) -> None:  # => defines the withdraw() method
        self.balance -= amount  # => the actual, unguarded mutation


class BankAccountProxy:  # => the PROTECTION PROXY -- adds a permission check IN FRONT
    def __init__(self, real_account: RealBankAccount, role: str) -> None:  # => holds the real subject AND the caller's role
        self._real: RealBankAccount = real_account  # => the object being protected
        self._role: str = role  # => the caller's role, checked before every delegation

    def withdraw(self, amount: float) -> None:  # => SAME interface as RealBankAccount
        if self._role != "admin":  # => the check RealBankAccount itself never performs
            raise PermissionError(f"role '{self._role}' cannot withdraw")  # => blocks the call entirely
        self._real.withdraw(amount)  # => only reached once the check has passed


account: RealBankAccount = RealBankAccount(balance=1000.0)  # => constructs account
admin_proxy: BankAccountProxy = BankAccountProxy(account, role="admin")  # => an authorized caller
guest_proxy: BankAccountProxy = BankAccountProxy(account, role="guest")  # => an unauthorized caller, SAME underlying account

admin_proxy.withdraw(100.0)  # => admin role passes the check -- delegates through
print(account.balance)  # => the withdrawal genuinely happened on the real account
# => Output: 900.0

try:  # => the block below is expected to raise
    guest_proxy.withdraw(50.0)  # => guest role fails the check -- never reaches RealBankAccount
except PermissionError as exc:  # => catches the PermissionError raised above
    print(exc)  # => confirms the exact rejection message
# => Output: role 'guest' cannot withdraw
print(account.balance)  # => unchanged -- the blocked withdrawal never touched the real account
# => Output: 900.0
# => The protection proxy enforces a permission check that the real subject itself does not know exists
