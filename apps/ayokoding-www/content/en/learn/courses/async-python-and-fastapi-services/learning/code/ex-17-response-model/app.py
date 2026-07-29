"""Example 17: Shaping the Output with a response model.

Run: uvicorn app:app --port 8000, then:
curl -X POST -H 'Content-Type: application/json' -d '{"name":"widget","secret_note":"internal"}' localhost:8000/items
(co-14)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves


class ItemIn(BaseModel):  # => the INPUT shape -- includes a field the response must NEVER leak (co-13)
    name: str  # => safe to echo back
    secret_note: str  # => sent by the client, but the response model below omits it


class ItemOut(BaseModel):  # => the OUTPUT shape -- a strict subset of ItemIn's fields (co-14)
    name: str  # => the ONLY field this model is allowed to expose


@app.post("/items", response_model=ItemOut)  # => response_model FILTERS the return value to ItemOut's fields
def create_item(item: ItemIn) -> ItemOut:  # => validated by ItemIn on the way in, filtered by ItemOut out
    # => even if the handler leaked item.secret_note, response_model would strip it -- filtering is on the
    # => OUTGOING side, independent of what the handler body computes (co-14)
    return ItemOut(name=item.name)  # => the response body contains name ONLY, never secret_note
