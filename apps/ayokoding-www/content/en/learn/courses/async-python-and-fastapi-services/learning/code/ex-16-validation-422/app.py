"""Example 16: Invalid Input Returns a 422.

The SAME app as ex-15 -- this example exists to POST an INVALID body and observe the automatic 422.
Run: uvicorn app:app --port 8000, then:
curl -s -w '\\nHTTP %{http_code}\\n' -X POST -H 'Content-Type: application/json' -d '{"name":"widget"}' localhost:8000/items
(co-13)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel  # => Pydantic models are the validation vocabulary (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves


class Item(BaseModel):  # => the shape a valid POST /items body must satisfy (co-12)
    name: str  # => required
    price: float  # => required -- omitting it is exactly the 422 this example triggers


@app.post("/items", status_code=201)  # => status 201 for a successful create (co-17)
def create_item(item: Item) -> Item:  # => validation runs BEFORE this body -- bad input never reaches here
    # => sending {"name":"widget"} (no price) fails validation and returns a 422, never reaching this return
    return item  # => only a fully-valid body reaches this line
