"""Example 49: Stabilizing an Unstable Vendor API Behind an Interface."""

import abc  # => imports the abc module


class PaymentGateway(abc.ABC):  # => the STABLE interface -- protects Checkout from vendor churn
    @abc.abstractmethod
    def charge(self, cents: int) -> str:  # => no body -- required by every vendor adapter
        ...  # => the ellipsis stub -- concrete vendor adapters below fill this in


class StripeGateway(PaymentGateway):  # => wraps VENDOR A's own, unstable method shape
    def charge(self, cents: int) -> str:  # => defines the charge() method
        return self._stripe_create_charge(amount_cents=cents)  # => delegates to the vendor's OWN, unstable-shaped method

    def _stripe_create_charge(self, amount_cents: int) -> str:  # => Stripe's OWN naming/shape
        return f"stripe:charged {amount_cents} cents"  # => returns this value to the caller


class PaypalGateway(PaymentGateway):  # => wraps VENDOR B's DIFFERENTLY-shaped method entirely
    def charge(self, cents: int) -> str:  # => defines the charge() method
        dollars: float = cents / 100  # => Paypal's OWN API happens to want dollars, not cents
        return self._paypal_send_payment(dollars)  # => delegates to the vendor's OWN, differently-shaped method

    def _paypal_send_payment(self, dollars: float) -> str:  # => Paypal's OWN naming/shape
        return f"paypal:sent ${dollars:.2f}"  # => returns this value to the caller


class Checkout:  # => the CLIENT -- depends ONLY on PaymentGateway, never on a vendor by name
    def __init__(self, gateway: PaymentGateway) -> None:  # => the constructor
        self.gateway = gateway  # => held as the stable abstraction, swappable at construction

    def pay(self, cents: int) -> str:  # => defines the pay() method
        return self.gateway.charge(cents)  # => Checkout's OWN code never changes, ever


stripe_checkout: Checkout = Checkout(StripeGateway())  # => wired to vendor A
print(stripe_checkout.pay(500))  # => Checkout.pay() itself never mentions "stripe" anywhere
# => Output: stripe:charged 500 cents

paypal_checkout: Checkout = Checkout(PaypalGateway())  # => SWAPPED to vendor B, no Checkout edit
print(paypal_checkout.pay(500))  # => the SAME Checkout.pay() call-site, a different vendor underneath
# => Output: paypal:sent $5.00
# => Swapping StripeGateway for PaypalGateway required editing zero lines inside the Checkout class
