"""Example 69: Drive a Whole Small System Through a Multi-Step Flow -- Verify the End-State."""

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from fastapi import FastAPI, HTTPException  # => co-25: the REAL app framework this whole system runs on  # fmt: skip
from fastapi.testclient import TestClient  # => co-25: drives the real app in-process  # fmt: skip
from pydantic import BaseModel  # => co-25: validates the shape every POST body must match  # fmt: skip

app = FastAPI()  # => co-25: the WHOLE small system this e2e test drives, start to finish  # fmt: skip
_CARTS: dict[str, list[dict[str, object]]] = {}  # => the app's OWN persistent state across every step  # fmt: skip


class LineItem(BaseModel):  # => the shape a caller POSTs to add to a cart  # fmt: skip
    name: str  # => co-25: Pydantic ENFORCES this field is present and a str  # fmt: skip
    price: float  # => co-25: Pydantic ENFORCES this field is present and a float  # fmt: skip


@app.post("/carts/{cart_id}/items")  # => step 1 of the user flow: ADD an item  # fmt: skip
def add_item(cart_id: str, item: LineItem) -> dict[str, object]:  # => the REAL handler for step 1  # fmt: skip
    _CARTS.setdefault(cart_id, []).append({"name": item.name, "price": item.price})  # => real mutation  # fmt: skip
    return {"cart_id": cart_id, "item_count": len(_CARTS[cart_id])}  # => real, cumulative state  # fmt: skip


@app.get("/carts/{cart_id}/total")  # => step 2/4 of the user flow: READ the running total  # fmt: skip
def get_total(cart_id: str) -> dict[str, object]:  # => the REAL handler for reading the total  # fmt: skip
    if cart_id not in _CARTS:  # => a genuine "no such cart" branch  # fmt: skip
        raise HTTPException(status_code=404, detail="cart not found")  # => a REAL 404  # fmt: skip
    total = sum(float(entry["price"]) for entry in _CARTS[cart_id])  # => a REAL sum over REAL state  # fmt: skip
    return {"cart_id": cart_id, "total": round(total, 2)}  # => co-25: real, rounded response body  # fmt: skip


@app.post("/carts/{cart_id}/checkout")  # => step 5 of the user flow: FINALIZE, clearing the cart  # fmt: skip
def checkout(cart_id: str) -> dict[str, object]:  # => the REAL handler for the FINAL step  # fmt: skip
    if cart_id not in _CARTS or not _CARTS[cart_id]:  # => a genuine "nothing to check out" branch  # fmt: skip
        raise HTTPException(status_code=400, detail="cannot checkout an empty cart")  # => a REAL 400  # fmt: skip
    total = sum(float(entry["price"]) for entry in _CARTS[cart_id])  # => a REAL sum, one final time  # fmt: skip
    item_count = len(_CARTS[cart_id])  # => captured BEFORE the cart is emptied below  # fmt: skip
    _CARTS[cart_id] = []  # => co-25: the REAL end-state change -- the cart is genuinely emptied  # fmt: skip
    return {
        "cart_id": cart_id,
        "receipt_total": round(total, 2),
        "items_purchased": item_count,
    }  # => real receipt


client = TestClient(app)  # => co-25: drives the WHOLE app, every step, over ONE shared client  # fmt: skip


def test_e2e_full_shopping_flow_reaches_correct_end_state() -> None:  # => co-25: the WHOLE flow  # fmt: skip
    cart_id = "cart-e2e-1"  # => one real cart, followed through every step below  # fmt: skip

    # Step 1: add the first item -- a REAL POST, mutating the REAL app state.
    step1 = client.post(f"/carts/{cart_id}/items", json={"name": "pen", "price": 1.50})  # => real POST  # fmt: skip
    assert step1.status_code == 200 and step1.json()["item_count"] == 1  # => 1st item landed  # fmt: skip

    # Step 2: add a second item -- state accumulates ACROSS requests, like a real user session.
    step2 = client.post(
        f"/carts/{cart_id}/items", json={"name": "notebook", "price": 3.00}
    )  # => 2nd POST
    assert step2.status_code == 200 and step2.json()["item_count"] == 2  # => 2nd item landed too  # fmt: skip

    # Step 3: read the running total -- confirms BOTH prior writes are reflected together.
    step3 = client.get(f"/carts/{cart_id}/total")  # => a REAL GET, reading the accumulated state  # fmt: skip
    assert step3.status_code == 200 and step3.json()["total"] == 4.50  # => 1.50 + 3.00, for real  # fmt: skip

    # Step 4: checkout -- the flow's FINAL action, which must see the FULL accumulated state.
    step4 = client.post(f"/carts/{cart_id}/checkout")  # => a REAL POST, finalizing the flow  # fmt: skip
    assert step4.status_code == 200  # => confirms checkout itself succeeded  # fmt: skip
    assert (
        step4.json()
        == {  # => co-25: the end-state this WHOLE flow was built to reach  # fmt: skip
            "cart_id": cart_id,  # => the SAME cart this whole flow followed  # fmt: skip
            "receipt_total": 4.50,  # => the accumulated total, matches step 3's real read  # fmt: skip
            "items_purchased": 2,  # => both real items counted  # fmt: skip
        }
    )

    # Step 5: confirm the SIDE EFFECT of checkout -- the cart is genuinely empty afterward.
    step5 = client.get(f"/carts/{cart_id}/total")  # => a REAL GET, AFTER the cart was emptied  # fmt: skip
    assert step5.json()["total"] == 0  # => co-25: the RESULTING end-state, not just step 4's response  # fmt: skip
