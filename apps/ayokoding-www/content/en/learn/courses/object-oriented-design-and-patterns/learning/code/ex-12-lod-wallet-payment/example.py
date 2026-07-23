"""Example 12: Pay Through the Customer, Not the Wallet."""


class Wallet:  # => a collaborator the OUTSIDE world should never touch directly
    def __init__(self, balance: float) -> None:  # => the constructor
        self._balance = balance  # => a leading underscore: internal to Wallet

    def withdraw(self, amount: float) -> float:  # => the ONLY sanctioned mutation
        if amount > self._balance:  # => guards the invariant: never go negative
            raise ValueError("insufficient funds")  # => rejects the call entirely
        self._balance -= amount  # => only reached once the amount is valid
        return self._balance  # => returns the new balance for convenience


class Customer:  # => sits BETWEEN the outside world and Wallet
    def __init__(self, wallet: Wallet) -> None:  # => the constructor
        self._wallet = wallet  # => underscore: Customer's OWN collaborator, not public
        # => no other method exposes _wallet -- it never leaks past this class boundary

    def pay(self, amount: float) -> float:  # => the tell-don't-ask entry point
        return self._wallet.withdraw(amount)  # => delegates internally -- the caller never sees Wallet at all


customer: Customer = Customer(Wallet(100.0))  # => wired together once, at construction
remaining: float = customer.pay(30.0)  # => the caller's ONLY call: customer.pay(amount)
print(remaining)  # => confirms the payment went through via a single dot
# => Output: 70.0
# => `customer.pay(30.0)` never reaches `customer.get_wallet().withdraw(30.0)` -- Wallet stays hidden
