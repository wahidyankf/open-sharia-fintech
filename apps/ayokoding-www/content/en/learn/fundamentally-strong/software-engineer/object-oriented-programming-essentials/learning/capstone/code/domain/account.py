"""Capstone: Account -- an entity that encapsulates its own balance invariant.

co-02 (encapsulation): `_balance` only ever changes through `deposit`/`withdraw`, never
through direct assignment -- the class is the single place "balance never goes negative"
is enforced. co-07 (properties): `balance` is a read-only computed view over the private
field. co-17 (invariant enforcement): the same overdraft guard applies on every mutating
path, not just at construction time.
"""

from __future__ import annotations

from domain.money import Money


class Account:
    """A named account holding a non-negative Money balance."""

    def __init__(
        self, owner: str, opening_balance: Money
    ) -> None:  # => the constructor
        self._owner: str = owner  # => stores owner on this instance
        self._balance: Money = (
            opening_balance  # => co-02: private -- never assigned to directly again
        )

    @property  # => marks the next method as a computed, read-only attribute
    def owner(self) -> str:  # => defines the owner() method
        return self._owner  # => returns this value to the caller

    @property  # => marks the next method as a computed, read-only attribute
    def balance(self) -> Money:  # => defines the balance() method
        return (
            self._balance
        )  # => co-07: read-only view -- callers cannot do account.balance = ...

    def deposit(self, amount: Money) -> None:  # => defines the deposit() method
        if amount.amount <= 0:  # => co-17: rejects a zero or negative deposit outright
            raise ValueError("deposit amount must be positive")
        self._balance = (
            self._balance + amount
        )  # => the ONLY line in this class that grows the balance

    def withdraw(self, amount: Money) -> None:  # => defines the withdraw() method
        if (
            amount.amount <= 0
        ):  # => co-17: rejects a zero or negative withdrawal outright
            raise ValueError("withdraw amount must be positive")
        if (
            amount.currency != self._balance.currency
        ):  # => co-17: same currency guard deposit gets for free via Money.__add__
            raise ValueError("cannot withdraw Money in a different currency")
        if (
            amount.amount > self._balance.amount
        ):  # => co-17: the core invariant -- no overdraft, ever
            raise ValueError("insufficient funds")
        self._balance = Money(
            self._balance.amount - amount.amount, self._balance.currency
        )
        # => the ONLY line in this class that shrinks the balance -- always via a fresh Money
