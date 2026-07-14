"""Capstone: PaymentMethod -- an ABC interface with two polymorphic implementations.

co-11 (abstraction / ABC): PaymentMethod cannot be instantiated on its own -- Python
enforces this at construction time. co-10 (polymorphism): `process_payment` is ONE
call-site that works identically whether it is handed a CardPayment or a
BankTransferPayment, with zero branching on which concrete type it received.
"""

from __future__ import annotations

import abc

from domain.account import Account
from domain.money import Money


class PaymentMethod(
    abc.ABC
):  # => abc.ABC marks this as an INTERFACE, never directly instantiable
    @abc.abstractmethod  # => marks the next method as a REQUIRED contract for every subclass
    def process(
        self, account: Account, amount: Money
    ) -> str:  # => no body -- subclasses supply one
        ...


class CardPayment(PaymentMethod):  # => CardPayment extends PaymentMethod
    def __init__(
        self, last4: str
    ) -> None:  # => the constructor -- runs once, automatically
        self.last4: str = last4  # => stores last4 on this instance

    def process(
        self, account: Account, amount: Money
    ) -> str:  # => defines the process() method
        account.deposit(
            amount
        )  # => delegates to Account's own guarded deposit -- co-17 still applies
        return f"card ending {self.last4} deposited {amount.amount} {amount.currency}"


class BankTransferPayment(
    PaymentMethod
):  # => BankTransferPayment extends PaymentMethod
    def __init__(
        self, iban: str
    ) -> None:  # => the constructor -- runs once, automatically
        self.iban: str = iban  # => stores iban on this instance

    def process(
        self, account: Account, amount: Money
    ) -> str:  # => defines the process() method
        account.deposit(
            amount
        )  # => the SAME Account.deposit call-site CardPayment also uses
        return f"bank transfer {self.iban} deposited {amount.amount} {amount.currency}"


def process_payment(method: PaymentMethod, account: Account, amount: Money) -> str:
    # => co-10: ONE function, typed against the INTERFACE -- never a concrete subclass
    return method.process(
        account, amount
    )  # => dispatches to whichever concrete class was actually passed
