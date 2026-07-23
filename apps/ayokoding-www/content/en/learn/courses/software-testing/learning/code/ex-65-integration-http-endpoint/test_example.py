"""Example 65: Hit a Small FastAPI Endpoint with TestClient -- Status and Body, For Real."""
# TestClient reaches every REAL layer here -- routing, Pydantic validation, the handler
# function -- with no mocking of FastAPI anywhere in this file.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from fastapi import FastAPI, HTTPException  # => co-23: the REAL app framework, unmocked  # fmt: skip
from fastapi.testclient import TestClient  # => co-23: drives the real app in-process  # fmt: skip
from pydantic import BaseModel  # => co-23: validates the response shape this endpoint promises  # fmt: skip

app = FastAPI()  # => co-23: a REAL, if tiny, FastAPI app -- standing in for "Backend-Essentials"  # fmt: skip
_ITEMS: dict[int, str] = {1: "widget", 2: "gadget"}  # => the app's own in-memory state  # fmt: skip


class Item(BaseModel):  # => the response SHAPE this endpoint promises callers -- Pydantic-validated  # fmt: skip
    id: int  # => co-23: Pydantic ENFORCES this field is present and an int  # fmt: skip
    name: str  # => co-23: Pydantic ENFORCES this field is present and a str  # fmt: skip


@app.get("/items/{item_id}", response_model=Item)  # => co-23: a REAL route, not a stubbed handler  # fmt: skip
def get_item(item_id: int) -> Item:  # => the handler under test -- runs for real via TestClient below  # fmt: skip
    if item_id not in _ITEMS:  # => a genuine "not found" branch, exercised below too  # fmt: skip
        raise HTTPException(status_code=404, detail="item not found")  # => a REAL 404, not simulated  # fmt: skip
    return Item(id=item_id, name=_ITEMS[item_id])  # => the REAL response body, built from REAL state  # fmt: skip


client = TestClient(app)  # => co-23: drives the REAL ASGI app in-process -- no network socket needed  # fmt: skip


def test_integration_get_existing_item_returns_200_and_body() -> (
    None
):  # => the happy path, for real
    response = client.get("/items/1")  # => a genuine request through the REAL FastAPI routing layer  # fmt: skip
    assert response.status_code == 200  # => co-23: the REAL handler's status code, not asserted-away  # fmt: skip
    assert response.json() == {"id": 1, "name": "widget"}  # => the REAL, validated response body  # fmt: skip


def test_integration_get_missing_item_returns_404() -> None:  # => the REAL error branch, exercised  # fmt: skip
    response = client.get("/items/999")  # => an id that genuinely isn't in _ITEMS  # fmt: skip
    assert response.status_code == 404  # => the REAL HTTPException, translated to a REAL status code  # fmt: skip
    assert response.json() == {"detail": "item not found"}  # => FastAPI's REAL error envelope shape  # fmt: skip


def test_integration_get_second_item_returns_its_own_data() -> (
    None
):  # => confirms per-id state, not a fluke
    response = client.get("/items/2")  # => a DIFFERENT id, still a real request  # fmt: skip
    assert response.status_code == 200  # => still a real, successful response  # fmt: skip
    assert response.json()["name"] == "gadget"  # => a DIFFERENT id returns DIFFERENT real data  # fmt: skip
