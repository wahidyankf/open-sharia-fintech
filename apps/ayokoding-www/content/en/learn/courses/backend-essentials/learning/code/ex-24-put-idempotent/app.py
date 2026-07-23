"""Example 24: PUT Idempotent."""

from fastapi import FastAPI  # => the web framework this whole tier builds on
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve

# => an in-memory store, module-level -- good enough to demonstrate PUT
# => semantics; Intermediate Example 35+ replaces this with real SQLite
items: dict[int, str] = {}  # => maps item_id -> name, cleared on every restart


class Item(BaseModel):  # => the full replacement payload PUT expects
    """The full replacement payload PUT expects."""

    # => only one field here, but a real Item would list EVERY field the
    # => resource has -- PUT's contract is "send the complete new state"
    name: str  # => PUT REPLACES the whole resource, so this is the WHOLE state


@app.put("/items/{item_id}")  # => PUT means "create or fully replace" (RFC 9110)
def replace_item(item_id: int, item: Item) -> dict[str, str]:
    """Two identical PUTs must leave the resource in the SAME final state."""
    # => item_id (path) identifies WHICH resource; item (body) is its full
    # => replacement value -- combining both params is how PUT's semantics work
    items[item_id] = item.name  # => always OVERWRITES, never appends/accumulates
    # => a SECOND identical call writes the SAME value again -- idempotent (co-02)
    return {"item_id": str(item_id), "name": items[item_id]}
    # => reads back the JUST-written value, confirming the overwrite landed
