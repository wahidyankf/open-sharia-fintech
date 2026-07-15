"""Capstone: a tiny 2-endpoint FastAPI app -- Step 4's integration test drives this over HTTP."""
# Standing in for this plan's "Backend-Essentials" app: an in-memory order service with just
# enough surface (add an item, read the total) to give Step 4 a real HTTP boundary to test
# through, built directly on the SAME service.py logic Steps 1-3 already verified in isolation.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from fastapi import FastAPI  # => co-25: the REAL, if tiny, ASGI app Step 4 drives with TestClient  # fmt: skip
from pydantic import BaseModel  # => co-23: validates every POST body against the Item shape below  # fmt: skip

from service import RealTaxGateway, compute_order_total  # => co-01: reuses Steps 1-3's SAME logic  # fmt: skip

app = FastAPI()  # => the WHOLE small system Step 4's integration test drives, end to end  # fmt: skip
_ORDERS: dict[str, list[float]] = {}  # => the app's own in-memory state, real across requests  # fmt: skip


class Item(BaseModel):  # => the shape a caller POSTs to add a line item  # fmt: skip
    price: float  # => co-23: Pydantic REJECTS a request body that doesn't match this field  # fmt: skip


@app.post("/orders/{order_id}/items")  # => endpoint 1 of 2 -- adds one line item  # fmt: skip
def add_item(order_id: str, item: Item) -> dict[str, object]:  # => co-25: the REAL route handler  # fmt: skip
    _ORDERS.setdefault(order_id, []).append(item.price)  # => genuine, cumulative in-memory state  # fmt: skip
    return {
        "order_id": order_id,
        "item_count": len(_ORDERS[order_id]),
    }  # => co-25: real response body


@app.get("/orders/{order_id}/total")  # => endpoint 2 of 2 -- reads the computed total  # fmt: skip
def get_total(order_id: str) -> dict[str, object]:  # => co-25: the SECOND real route handler  # fmt: skip
    prices = _ORDERS.get(order_id, [])  # => co-25: an EMPTY list for an order that never existed  # fmt: skip
    # region="US-OR" (Oregon has NO state sales tax) sidesteps needing a REAL external tax
    # call for this demo app -- RealTaxGateway.rate_for_region() would raise if it were ever
    # actually invoked, but 0% regions never reach that line in THIS deliberately tiny app.
    total = compute_order_total(prices, region="US-OR", tax_gateway=_ZeroRateGateway())  # => co-01/co-23  # fmt: skip
    return {"order_id": order_id, "total": total}  # => co-25: the SAME logic Steps 1-3 verified alone  # fmt: skip


class _ZeroRateGateway(RealTaxGateway):  # => a tiny, HONEST override -- avoids a NotImplementedError  # fmt: skip
    """A trivial always-zero gateway for this demo app's one hardcoded, tax-free region."""  # => co-12

    def rate_for_region(self, region: str) -> float:  # => co-12: genuinely returns 0, not a mock  # fmt: skip
        return 0.0  # => co-12: a REAL, honest override -- not a MagicMock standing in for this  # fmt: skip
