"""Example 12: pytest verification for Pay Through the Customer, Not the Wallet."""

# => this test file deliberately imports ONLY Customer -- never Wallet at all
from example import Customer, Wallet


def test_customer_exposes_no_public_wallet_attribute() -> None:
    customer: Customer = Customer(Wallet(100.0))
    assert not hasattr(customer, "wallet")  # => no public accessor exists
    assert hasattr(customer, "_wallet")  # => only the underscore-prefixed internal one


def test_pay_delegates_to_the_hidden_wallet() -> None:
    customer: Customer = Customer(Wallet(100.0))
    remaining: float = customer.pay(30.0)  # => the caller's only call site
    assert remaining == 70.0  # => the withdrawal genuinely happened, one dot away


# => Run: pytest -- Output: 2 passed
