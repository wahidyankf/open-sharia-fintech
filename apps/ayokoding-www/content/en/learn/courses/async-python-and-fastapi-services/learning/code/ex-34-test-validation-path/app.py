"""Example 34: Testing a Validation Failure Path -- the app under test.

A POST route with a required field; the test asserts a 422 when the field is missing. Run: pytest -v. (co-21, co-13)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI()  # => the ASGI application uvicorn serves


class Item(BaseModel):  # => the body shape
    name: str  # => required -- omitting it is the 422 the test asserts


@app.post("/items", status_code=201)  # => a create route
def create_item(item: Item) -> Item:  # => validation runs before the handler body
    return item  # => only a valid body reaches here
