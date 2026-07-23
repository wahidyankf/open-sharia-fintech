"""Example 61: Organize a Suite in Pyramid Shape -- Many Unit, Some Integration, Few E2E."""

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python


class Cart:  # => co-10: the unit under test -- no collaborators, cheap to construct  # fmt: skip
    """A minimal shopping cart -- pure in-memory state, no IO."""  # => co-10: no collaborators at all  # fmt: skip

    def __init__(self) -> None:  # => co-10: cheap to construct -- ideal for MANY unit tests  # fmt: skip
        self.items: list[tuple[str, float]] = []  # => (name, price) pairs, in insertion order  # fmt: skip

    def add_item(self, name: str, price: float) -> None:  # => appends one line item  # fmt: skip
        self.items.append((name, price))  # => co-10: the ONLY mutation this class exposes  # fmt: skip

    def total(self) -> float:  # => sums every line item's price  # fmt: skip
        return sum(price for _, price in self.items)  # => co-10: pure aggregation, no side effects  # fmt: skip


class PricingService:  # => co-10/co-23: a REAL collaborator -- not stubbed for the integration tier  # fmt: skip
    """A tiny, real discount calculator -- exercised for real in the integration tests below."""  # => co-23

    def apply_discount(self, total: float, pct: float) -> float:  # => percent off a total  # fmt: skip
        return round(total * (1 - pct), 2)  # => rounded to cents, like a real checkout would  # fmt: skip


def checkout(
    cart: Cart, pricing: PricingService, discount_pct: float
) -> float:  # => co-10: the e2e path
    """The full user-facing flow: fill a cart, then check out with a discount applied."""  # => co-10
    return pricing.apply_discount(cart.total(), discount_pct)  # => composes BOTH collaborators  # fmt: skip


# ---- unit tier: MANY tests, each isolated, each fast, each testing ONE method ----
def test_unit_add_single_item() -> None:  # => co-01: arrange-act-assert, one behavior per test  # fmt: skip
    cart = Cart()  # => arrange: a fresh Cart, no items yet  # fmt: skip
    cart.add_item("pen", 1.50)  # => act: the ONE behavior this test targets  # fmt: skip
    assert cart.items == [("pen", 1.50)]  # => assert: the item landed, in the expected shape  # fmt: skip


def test_unit_add_multiple_items() -> None:  # => co-01: a SECOND unit test, still one behavior  # fmt: skip
    cart = Cart()  # => arrange: a fresh Cart, independent of the test above  # fmt: skip
    cart.add_item("pen", 1.50)  # => act: first addition  # fmt: skip
    cart.add_item("notebook", 3.00)  # => act: second addition  # fmt: skip
    assert len(cart.items) == 2  # => confirms BOTH items were recorded, in order  # fmt: skip


def test_unit_total_empty_cart() -> None:  # => the trivial base case -- zero items, zero total  # fmt: skip
    assert Cart().total() == 0  # => co-01: a fresh Cart, asserted inline -- nothing else to arrange  # fmt: skip


def test_unit_total_single_item() -> None:  # => co-01: 4th unit test -- total() with one item  # fmt: skip
    cart = Cart()  # => arrange: a fresh Cart  # fmt: skip
    cart.add_item("pen", 1.50)  # => act: add exactly one item  # fmt: skip
    assert cart.total() == 1.50  # => assert: the total equals that single item's price  # fmt: skip


def test_unit_total_multiple_items() -> None:  # => co-01: 5th unit test -- total() sums correctly  # fmt: skip
    cart = Cart()  # => arrange: a fresh Cart  # fmt: skip
    cart.add_item("pen", 1.50)  # => act: first item  # fmt: skip
    cart.add_item("notebook", 3.00)  # => act: second item  # fmt: skip
    assert cart.total() == 4.50  # => confirms summation, not just item count  # fmt: skip


def test_unit_items_recorded_in_order() -> None:  # => 6th unit test -- insertion order matters too  # fmt: skip
    cart = Cart()  # => arrange: a fresh Cart  # fmt: skip
    cart.add_item("first", 1.0)  # => act: added FIRST  # fmt: skip
    cart.add_item("second", 2.0)  # => act: added SECOND  # fmt: skip
    assert [name for name, _ in cart.items] == ["first", "second"]  # => order is preserved  # fmt: skip


# ---- integration tier: SOME tests, real collaborators combined, past the unit seam ----
def test_integration_cart_plus_pricing_applies_discount() -> None:  # => co-23: TWO real objects  # fmt: skip
    cart = Cart()  # => a REAL Cart, not a mock  # fmt: skip
    cart.add_item("widget", 100.0)  # => arrange: one $100 item  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService, not a mock -- co-23's defining trait  # fmt: skip
    assert pricing.apply_discount(cart.total(), 0.10) == 90.0  # => 10% off a real $100 total  # fmt: skip


def test_integration_cart_plus_pricing_zero_discount_is_noop() -> None:  # => 2nd integration test  # fmt: skip
    cart = Cart()  # => a REAL Cart, again unstubbed  # fmt: skip
    cart.add_item("widget", 100.0)  # => arrange: the same $100 item  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService  # fmt: skip
    assert pricing.apply_discount(cart.total(), 0.0) == 100.0  # => 0% off changes nothing  # fmt: skip


# ---- e2e tier: FEW tests, the full user-facing flow, top to bottom ----
def test_e2e_checkout_flow_end_to_end() -> None:  # => co-10: ONE test, the WHOLE flow  # fmt: skip
    cart = Cart()  # => arrange: a fresh Cart, the flow's starting point  # fmt: skip
    cart.add_item("widget", 50.0)  # => act: first item added, as a real shopper would  # fmt: skip
    cart.add_item("gadget", 50.0)  # => act: second item added  # fmt: skip
    pricing = PricingService()  # => a REAL PricingService, part of the FULL flow  # fmt: skip
    assert checkout(cart, pricing, discount_pct=0.20) == 80.0  # => the full flow, one assertion  # fmt: skip
