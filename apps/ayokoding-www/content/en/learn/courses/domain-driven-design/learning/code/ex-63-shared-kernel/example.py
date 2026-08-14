"""Example 63: a shared kernel is a deliberate, small contract."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str  # => billing and payroll may share this stable value


def bill(value: Money) -> str:
    return value.currency


def pay(value: Money) -> str:
    return value.currency


assert bill(Money(1, "USD")) == pay(Money(2, "USD"))
