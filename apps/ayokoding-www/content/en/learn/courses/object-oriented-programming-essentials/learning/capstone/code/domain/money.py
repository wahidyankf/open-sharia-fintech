"""Capstone: Money -- a frozen, hashable value object with a non-negative-amount invariant.

co-06 (dataclass value object): frozen=True gives immutability, and because eq=True
(the default) is paired with frozen=True, Python auto-generates a __hash__ consistent
with the auto-generated __eq__ -- co-05's eq/hash contract, satisfied for free.
co-17 (invariant enforcement): __post_init__ rejects a negative amount or a malformed
currency code the moment a Money is constructed, so no invalid Money can ever exist.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True
)  # => frozen -> immutable AND auto __hash__ alongside auto __eq__
class Money:
    """An immutable amount of money, stored in integer cents to avoid float rounding error."""

    amount: (
        int  # => whole cents -- never a float, so equality never suffers rounding drift
    )
    currency: str = "USD"  # => a default keeps most call-sites in this capstone terse

    def __post_init__(
        self,
    ) -> None:  # => runs once, right after the frozen fields are set
        if (
            self.amount < 0
        ):  # => co-17: the invariant -- a Money can never represent a negative amount
            raise ValueError(f"Money amount cannot be negative, got {self.amount}")
        if (
            len(self.currency) != 3
        ):  # => co-17: a second invariant -- currency must be a 3-letter code
            raise ValueError(f"currency must be a 3-letter code, got {self.currency!r}")

    def __add__(self, other: Money) -> Money:  # => defines the __add__() method
        if (
            self.currency != other.currency
        ):  # => guards against silently mixing currencies
            raise ValueError("cannot add Money in different currencies")
        return Money(
            self.amount + other.amount, self.currency
        )  # => returns a NEW Money -- frozen, no mutation
