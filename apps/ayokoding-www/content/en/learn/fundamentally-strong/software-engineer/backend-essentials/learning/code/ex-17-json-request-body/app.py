"""Example 17: JSON Request Body."""

from fastapi import FastAPI  # => the web framework this whole tier builds on
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve


class Item(BaseModel):  # => a typed request-body model
    """A typed request-body model -- Pydantic validates incoming JSON against it."""

    name: str  # => required string field -- missing/wrong type fails validation
    price: float  # => required float field -- a second, independent constraint


@app.post("/items")  # => POST is the method this route pairs a body with (co-02)
def create_item(item: Item) -> Item:
    """FastAPI parses the JSON body into an Item instance before this runs."""
    # => the parameter "item: Item" is what tells FastAPI to parse the request
    # => BODY (co-13) as JSON and validate it (co-10) against the Item model --
    # => by the time this LINE runs, validation already happened -- a malformed
    # => body never reaches here at all; it gets a 422 before create_item starts
    # => item.name/item.price are already validated, typed Python values here
    return item  # => Pydantic re-serializes the model back to JSON on the way out
    # => the round trip: JSON in -> validated Item -> JSON out, all automatic
