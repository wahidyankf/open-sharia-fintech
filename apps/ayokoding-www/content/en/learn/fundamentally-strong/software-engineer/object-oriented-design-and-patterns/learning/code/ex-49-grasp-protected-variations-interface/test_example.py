"""Example 49: pytest verification for Protected Variations Behind an Interface."""

from example import Checkout, PaypalGateway, StripeGateway


def test_stripe_backed_checkout_charges_through_the_vendor_adapter() -> None:
    checkout: Checkout = Checkout(StripeGateway())
    assert checkout.pay(500) == "stripe:charged 500 cents"


def test_swapping_the_vendor_requires_no_checkout_class_changes() -> None:
    # => same Checkout class, same pay() call-site, only the injected gateway differs
    checkout: Checkout = Checkout(PaypalGateway())
    assert checkout.pay(500) == "paypal:sent $5.00"


# => Run: pytest -- Output: 2 passed
