"""Example 63: Anti-Pattern -- Anemic Domain Model.

co-34 (anti-pattern recognition): an anemic model is a data class with all behavior
pulled into a separate service, so the "object" in object-oriented is data-only --
co-06 (grasp-information-expert) names the fix: move behavior onto the entity that
already holds the data the behavior needs.
"""

from __future__ import annotations

from dataclasses import dataclass

# ============================================================
# BEFORE: an anemic Account (data only) plus a service that does everything
# ============================================================


@dataclass  # => auto-generates __init__ from the balance field below
class AnemicAccount:  # => pure data -- no behavior at all, just fields
    balance: float  # => the only thing this "object" holds


# => contrast: nothing here stops other code from mutating account.balance directly, bypassing withdraw()
class AccountService:  # => ALL the behavior lives here instead, disconnected from the data it operates on
    def withdraw(self, account: AnemicAccount, amount: float) -> None:  # => reaches INTO the account to mutate it
        if amount > account.balance:  # => the invariant ("cannot overdraw") lives in the service, not the entity
            raise ValueError("insufficient funds")  # => nothing stops OTHER code from bypassing this check
        account.balance -= amount  # => direct field mutation, invariant enforced only if you remembered to call this
        # => this mutation is only safe if every caller remembers to call withdraw() instead of touching balance


# ============================================================
# AFTER: the entity owns its own behavior -- information-expert applied
# ============================================================


# => RichAccount fixes the anemia: balance and the rule that guards it now live in the same place
class RichAccount:  # => the entity now owns the data AND the behavior that guards it
    def __init__(self, balance: float) -> None:  # => takes the initial balance directly, same shape as AnemicAccount
        self._balance = balance  # => the same data, but now private -- no direct external mutation

    @property  # => exposes balance for reading without exposing a way to write it directly
    def balance(self) -> float:  # => read-only view of the balance
        return self._balance  # => the only way to read balance from outside the class

    def withdraw(self, amount: float) -> None:  # => information-expert: RichAccount holds balance, so IT withdraws
        if amount > self._balance:  # => the SAME invariant, but now impossible to bypass via direct field access
            raise ValueError("insufficient funds")  # => identical error to the anemic version
        self._balance -= amount  # => the only way balance can change is through this guarded method


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    anemic = AnemicAccount(balance=100.0)  # => the old version
    service = AccountService()  # => the disconnected service the old design requires
    service.withdraw(anemic, 30.0)  # => behavior lives OUTSIDE the object it operates on
    print(anemic.balance)  # => still correct here, but nothing prevents anemic.balance = 999 elsewhere
    # => Output: 70.0

    # => same starting balance as the anemic example above, for a fair side-by-side comparison
    rich = RichAccount(balance=100.0)  # => the refactored version
    rich.withdraw(30.0)  # => behavior lives ON the object, next to the data it guards
    print(rich.balance)  # => identical result to the anemic version
    # => Output: 70.0
