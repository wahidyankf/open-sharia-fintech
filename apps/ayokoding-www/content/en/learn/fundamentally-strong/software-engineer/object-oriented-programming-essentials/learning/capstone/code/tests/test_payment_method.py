"""Capstone: pytest coverage proving PaymentMethod is polymorphic across implementations."""

import pytest

from domain.account import Account
from domain.money import Money
from domain.payment_method import (
    BankTransferPayment,
    CardPayment,
    PaymentMethod,
    process_payment,
)


def test_payment_method_cannot_be_instantiated_directly() -> None:
    with pytest.raises(
        TypeError
    ):  # => co-11: an ABC with an unimplemented method always rejects this
        PaymentMethod()  # type: ignore  # => deliberately triggers the ABC instantiation guard


def test_card_payment_deposits_into_account() -> None:
    account: Account = Account("Alice", Money(0))
    result: str = process_payment(CardPayment("4242"), account, Money(500))
    assert account.balance == Money(
        500
    )  # => the deposit genuinely landed on the account
    assert (
        "4242" in result
    )  # => the concrete implementation's own detail is still visible in the result


def test_bank_transfer_payment_deposits_into_account() -> None:
    account: Account = Account("Alice", Money(0))
    result: str = process_payment(BankTransferPayment("DE89"), account, Money(700))
    assert account.balance == Money(
        700
    )  # => the SAME call-site, a DIFFERENT concrete implementation
    assert "DE89" in result


def test_process_payment_call_site_is_implementation_agnostic() -> None:
    account: Account = Account("Alice", Money(0))
    methods: list[PaymentMethod] = [CardPayment("0000"), BankTransferPayment("XX00")]
    for (
        method
    ) in methods:  # => co-10: ONE loop body, dispatching polymorphically per element
        process_payment(method, account, Money(100))
    assert account.balance == Money(
        200
    )  # => both payments landed, regardless of concrete type


# => Run: pytest -- Output: 4 passed
