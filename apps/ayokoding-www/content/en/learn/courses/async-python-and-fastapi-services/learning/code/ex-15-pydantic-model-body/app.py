"""Example 15: A Pydantic Model as a Request Body.

Run: uvicorn app:app --port 8000, then:
curl -X POST -H 'Content-Type: application/json' -d '{"name":"widget","price":9.99}' localhost:8000/items
(co-12, co-11)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves


class Item(BaseModel):  # => a typed REQUEST-BODY model -- Pydantic validates incoming JSON against it (co-12)
    name: str  # => required string field -- a missing/wrong type fails validation (co-13)
    price: float  # => required float field -- a second, independent constraint


@app.post("/items")  # => POST is the method this route pairs a body with (co-11)
def create_item(item: Item) -> Item:  # => a Pydantic-model PARAM tells FastAPI to parse the BODY as JSON
    # => by the time this line runs, the body was ALREADY parsed + validated -- a bad body never reaches here
    return item  # => Pydantic re-serializes the model back to JSON on the way out (co-14)
