"""Example 68: the tiny REAL provider app the pact from Example 67 is verified against."""
# This app's route/response shape MUST match Example 67's recorded pact exactly, or the
# real Verifier.verify() call in test_example.py fails against the real, running server.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from fastapi import FastAPI, HTTPException  # => co-24: a REAL app framework, not a stub server  # fmt: skip

app = FastAPI()  # => co-24: a REAL FastAPI app playing the "catalog-provider" role from the pact  # fmt: skip
_ITEMS: dict[int, dict[str, object]] = {1: {"id": 1, "name": "widget"}}  # => matches Example 67's body  # fmt: skip


@app.get("/items/{item_id}")  # => co-24: MUST match the pact's recorded request path exactly  # fmt: skip
def get_item(item_id: int) -> dict[str, object]:  # => the REAL handler the verifier hits below  # fmt: skip
    if item_id not in _ITEMS:  # => a real "not found" branch, not exercised by ex-67's ONE interaction  # fmt: skip
        raise HTTPException(status_code=404)  # => a REAL 404, matching REST conventions  # fmt: skip
    return _ITEMS[item_id]  # => MUST match the pact's recorded response body exactly  # fmt: skip
