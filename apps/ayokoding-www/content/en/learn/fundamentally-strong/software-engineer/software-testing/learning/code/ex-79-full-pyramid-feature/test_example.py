"""Example 79: One Feature, Every Tier -- Unit + Integration + E2E, All Green."""
# One coupon feature, tested at all THREE pyramid tiers -- co-10's pure function alone, co-23's
# real collaborator combo, and co-25's whole-system HTTP flow -- all green, all genuinely run.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from fastapi import FastAPI, HTTPException  # => co-25: the web framework the e2e tier drives  # fmt: skip
from fastapi.testclient import TestClient  # => co-25: drives the app WITHOUT a real network socket  # fmt: skip
from pydantic import BaseModel  # => co-25: request-body validation for the add-item endpoint  # fmt: skip

# ---------------------------------------------------------------------------
# The feature: applying a coupon code to a cart total.
# ---------------------------------------------------------------------------


def coupon_discount_pct(code: str) -> float:  # => co-10: pure logic -- the UNIT tier's target  # fmt: skip
    """Pure lookup -- no IO, no collaborators -- ideal unit-test material."""
    table = {"SAVE10": 0.10, "SAVE20": 0.20}  # => the WHOLE rulebook, in one literal dict  # fmt: skip
    return table.get(code.upper(), 0.0)  # => an unknown code means NO discount, not an error  # fmt: skip


class Cart:  # => co-23: a real collaborator the integration tier combines with the coupon logic  # fmt: skip
    def __init__(self) -> None:  # => starts empty -- every test below builds its OWN cart  # fmt: skip
        self.items: list[float] = []  # => co-23: REAL mutable state, not a double of any kind  # fmt: skip

    def add(self, price: float) -> None:  # => the ONE mutation this class exposes  # fmt: skip
        self.items.append(price)  # => appends one line-item price  # fmt: skip

    def subtotal(self) -> float:  # => derives a total from CURRENT items, never cached  # fmt: skip
        return sum(self.items)  # => co-23: a REAL sum over REAL items, no mocking involved  # fmt: skip


def apply_coupon(
    cart: Cart, code: str
) -> float:  # => co-23: composes CART + the pure coupon logic
    discount = coupon_discount_pct(code)  # => co-10: the SAME function the unit tier tests alone  # fmt: skip
    return round(cart.subtotal() * (1 - discount), 2)  # => co-23: real cart state * pure discount  # fmt: skip


app = FastAPI()  # => co-25: the WHOLE small system the e2e tier drives  # fmt: skip
_CARTS: dict[str, Cart] = {}  # => co-25: process-lifetime state, keyed by cart id, real HTTP hits this  # fmt: skip


class AddItemRequest(BaseModel):  # => co-25: validates the JSON body of the add-item endpoint  # fmt: skip
    price: float  # => the ONE field this endpoint requires, enforced by pydantic  # fmt: skip


@app.post("/carts/{cart_id}/items")  # => co-25: a REAL route, hit through the TestClient below  # fmt: skip
def add_item(
    cart_id: str, body: AddItemRequest
) -> dict[str, object]:  # => co-25: real endpoint handler
    _CARTS.setdefault(cart_id, Cart()).add(body.price)  # => co-25: creates-or-reuses the REAL cart  # fmt: skip
    return {"subtotal": _CARTS[cart_id].subtotal()}  # => co-25: the REAL cart's REAL running total  # fmt: skip


@app.post("/carts/{cart_id}/apply-coupon")  # => co-25: the second REAL route the e2e tier exercises  # fmt: skip
def apply_coupon_endpoint(
    cart_id: str, code: str
) -> dict[str, object]:  # => co-25: real handler #2
    if (
        cart_id not in _CARTS
    ):  # => co-25: guards against a coupon applied to a cart that never existed
        raise HTTPException(status_code=404, detail="cart not found")  # => a REAL 404, over REAL HTTP  # fmt: skip
    return {"total": apply_coupon(_CARTS[cart_id], code)}  # => co-25: the SAME apply_coupon() the  # fmt: skip
    # => integration tier tested directly, now reached through a REAL HTTP endpoint


client = TestClient(app)  # => co-25: drives `app` in-process -- real ASGI routing, no real socket  # fmt: skip


# ---- UNIT tier: the pure function, alone, no collaborators ----
def test_unit_coupon_discount_pct_known_code() -> None:  # => co-10: fastest, most isolated tier  # fmt: skip
    assert coupon_discount_pct("SAVE10") == 0.10  # => co-10: pure input -> pure output, no setup at all  # fmt: skip


def test_unit_coupon_discount_pct_unknown_code() -> None:  # => co-10: still isolated, still instant  # fmt: skip
    assert coupon_discount_pct("BOGUS") == 0.0  # => co-10: the default-to-zero branch, proven directly  # fmt: skip


# ---- INTEGRATION tier: Cart + coupon logic, combined, no HTTP involved ----
def test_integration_apply_coupon_to_real_cart() -> None:  # => co-23: real Cart, real coupon lookup  # fmt: skip
    cart = Cart()  # => arrange: a genuinely fresh Cart, not a double of one  # fmt: skip
    cart.add(50.0)  # => arrange: first REAL line-item  # fmt: skip
    cart.add(50.0)  # => arrange: second REAL line-item, subtotal now genuinely 100.0  # fmt: skip
    assert apply_coupon(cart, "SAVE20") == 80.0  # => 100 * (1 - 0.20), through the REAL chain  # fmt: skip


# ---- E2E tier: the full HTTP flow, add item then apply coupon, through the real app ----
def test_e2e_add_item_then_apply_coupon_through_http() -> None:  # => co-25: the WHOLE system, live  # fmt: skip
    add_response = client.post("/carts/pyramid-cart/items", json={"price": 40.0})  # => real POST #1  # fmt: skip
    assert add_response.status_code == 200 and add_response.json()["subtotal"] == 40.0  # fmt: skip
    # => co-25: confirms the FIRST real HTTP round-trip landed correctly before the second begins

    coupon_response = (
        client.post(  # => real POST #2, over the SAME in-process ASGI app  # fmt: skip
            "/carts/pyramid-cart/apply-coupon", params={"code": "SAVE10"}
        )
    )
    assert coupon_response.status_code == 200  # => co-25: proves the route itself resolved, no 404  # fmt: skip
    assert coupon_response.json() == {"total": 36.0}  # => 40 * (1 - 0.10), reached via REAL HTTP  # fmt: skip
