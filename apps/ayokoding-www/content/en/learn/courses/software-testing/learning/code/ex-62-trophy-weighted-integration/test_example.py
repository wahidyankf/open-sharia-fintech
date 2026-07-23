"""Example 62: Reweight the Same Suite Toward Integration -- the Testing Trophy."""

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python


class Cart:  # => the SAME unit under test as Example 61 -- only the test WEIGHTING changes here  # fmt: skip
    def __init__(self) -> None:  # => cheap to construct -- unchanged from Example 61  # fmt: skip
        self.items: list[tuple[str, float]] = []  # => (name, price) pairs, in insertion order  # fmt: skip

    def add_item(self, name: str, price: float) -> None:  # => appends one line item  # fmt: skip
        self.items.append((name, price))  # => the ONLY mutation this class exposes  # fmt: skip

    def total(self) -> float:  # => sums every line item's price  # fmt: skip
        return sum(price for _, price in self.items)  # => pure aggregation, no side effects  # fmt: skip


class PricingService:  # => co-10: a real, un-mocked collaborator -- the trophy's biggest tier uses it  # fmt: skip
    def apply_discount(self, total: float, pct: float) -> float:  # => percent off a total  # fmt: skip
        return round(total * (1 - pct), 2)  # => rounded to cents, like a real checkout would  # fmt: skip


class ReceiptFormatter:  # => a SECOND real collaborator -- more integration surface than Example 61  # fmt: skip
    """Formats a final total as a receipt line -- another real, non-stubbed piece."""  # => co-23

    def format_total(self, total: float) -> str:  # => co-23: exercised for real below  # fmt: skip
        return f"TOTAL: ${total:.2f}"  # => co-23: real string formatting, never mocked  # fmt: skip


def checkout(
    cart: Cart, pricing: PricingService, discount_pct: float
) -> float:  # => the e2e path
    return pricing.apply_discount(cart.total(), discount_pct)  # => composes the REAL collaborators  # fmt: skip


# ---- unit tier: FEW tests now -- Kent C. Dodds's trophy spends LESS effort here than a pyramid does ----
def test_unit_total_sums_items() -> None:  # => co-01: still arrange-act-assert, just fewer of these  # fmt: skip
    cart = Cart()  # => arrange: a fresh Cart  # fmt: skip
    cart.add_item("pen", 2.0)  # => act: add one item  # fmt: skip
    assert cart.total() == 2.0  # => assert: the total reflects that one item  # fmt: skip


def test_unit_empty_cart_total_is_zero() -> None:  # => 2nd and LAST unit test in this reweighted suite  # fmt: skip
    assert Cart().total() == 0  # => co-01: the trivial base case, asserted inline  # fmt: skip


# ---- integration tier: MOST tests now -- the trophy's thickest layer, real collaborators combined ----
def test_integration_cart_plus_pricing() -> None:  # => co-23: real Cart + real PricingService  # fmt: skip
    cart = Cart()  # => a REAL Cart  # fmt: skip
    cart.add_item("widget", 100.0)  # => arrange: one $100 item  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService  # fmt: skip
    assert pricing.apply_discount(cart.total(), 0.10) == 90.0  # => 10% off a real $100 total  # fmt: skip


def test_integration_cart_plus_pricing_plus_formatter() -> None:  # => THREE real objects together  # fmt: skip
    cart = Cart()  # => a REAL Cart  # fmt: skip
    cart.add_item("widget", 100.0)  # => arrange: one $100 item  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService  # fmt: skip
    formatter = ReceiptFormatter()  # => a REAL ReceiptFormatter -- the THIRD real object  # fmt: skip
    discounted = pricing.apply_discount(cart.total(), 0.10)  # => act: real discount computed  # fmt: skip
    assert formatter.format_total(discounted) == "TOTAL: $90.00"  # => the FULL real chain, formatted  # fmt: skip


def test_integration_pricing_plus_formatter_zero_total() -> None:  # => an edge case, still integrated  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService, no Cart needed for this edge case  # fmt: skip
    formatter = ReceiptFormatter()  # => a REAL ReceiptFormatter  # fmt: skip
    assert (
        formatter.format_total(pricing.apply_discount(0.0, 0.5)) == "TOTAL: $0.00"
    )  # => zero-total edge


def test_integration_multi_item_cart_through_full_chain() -> None:  # => a richer cart, same real chain  # fmt: skip
    cart = Cart()  # => a REAL Cart  # fmt: skip
    cart.add_item("a", 10.0)  # => arrange: first item  # fmt: skip
    cart.add_item("b", 20.0)  # => arrange: second item  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService  # fmt: skip
    formatter = ReceiptFormatter()  # => a REAL ReceiptFormatter  # fmt: skip
    assert (
        formatter.format_total(pricing.apply_discount(cart.total(), 0.0))
        == "TOTAL: $30.00"
    )  # => real chain


def test_integration_discount_rounds_to_cents() -> None:  # => 5th integration test -- MORE than unit+e2e combined  # fmt: skip
    cart = Cart()  # => a REAL Cart  # fmt: skip
    cart.add_item("odd", 10.0)  # => arrange: an item that forces a repeating-decimal discount  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService  # fmt: skip
    assert pricing.apply_discount(cart.total(), 1 / 3) == 6.67  # => rounding behavior, exercised for real  # fmt: skip


# ---- e2e tier: still few -- the trophy's TOP, unchanged in SHAPE from a pyramid, just proportion ----
def test_e2e_checkout_flow_end_to_end() -> None:  # => the ONLY e2e test -- same as before  # fmt: skip
    cart = Cart()  # => arrange: a fresh Cart, the flow's starting point  # fmt: skip
    cart.add_item("widget", 50.0)  # => act: first item added  # fmt: skip
    cart.add_item("gadget", 50.0)  # => act: second item added  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService, part of the FULL flow  # fmt: skip
    assert checkout(cart, pricing, discount_pct=0.20) == 80.0  # => the full flow, one assertion  # fmt: skip
