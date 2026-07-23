"""Example 18: Response Model."""

from fastapi import FastAPI  # => the web framework this whole tier builds on
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve


class ItemIn(BaseModel):  # => the INPUT validation shape
    """The request shape -- includes a field we deliberately never return."""

    name: str  # => safe to echo back to the client
    secret_note: str  # => a field the client sends, but the response must NOT leak


class ItemOut(BaseModel):  # => the OUTPUT filtering shape
    """The response shape -- a strict subset of ItemIn's fields."""

    name: str  # => the ONLY field this model is allowed to expose


@app.post("/items", response_model=ItemOut)  # => declares the OUTPUT shape (co-09)
def create_item(item: ItemIn) -> ItemOut:
    """response_model filters the return value down to ItemOut's fields only."""
    # => ItemIn is the INPUT validation shape (co-10); ItemOut is the OUTPUT
    # => filtering shape -- two distinct models is the pattern that keeps a
    # => field like secret_note reachable on the way IN but never on the way out
    # => even if this handler accidentally returned item.secret_note somewhere,
    # => response_model would still strip it -- the filtering happens on the
    # => OUTGOING side, independent of what the handler body actually computes
    return ItemOut(name=item.name)  # => secret_note never reaches the response body
