"""Example 18: OpenAPI Docs Are Generated for Free.

FastAPI derives the full OpenAPI schema from the typed routes -- every path, parameter, model, and status
appears with no extra authoring. Run as a server: uvicorn app:app --port 8000, then curl localhost:8000/openapi.json
-- or run directly to print the generated schema's paths. (co-20)
"""

from fastapi import FastAPI  # => the web framework (co-10)
from pydantic import BaseModel  # => Pydantic models (co-12)

app = FastAPI(title="OpenAPI Demo")  # => the title appears in the generated schema's info block (co-20)


class Item(BaseModel):  # => this model becomes a schema COMPONENT in the generated OpenAPI doc (co-20)
    name: str  # => required string
    price: float  # => required float


@app.get("/items/{item_id}")  # => becomes a paths entry: GET /items/{item_id} (co-20)
def read_item(item_id: int) -> dict[str, int]:  # => item_id shows up as an integer path PARAMETER (co-11)
    return {"item_id": item_id}  # => the return type informs the response schema (co-14)


@app.post("/items")  # => becomes a paths entry: POST /items, body referencing the Item schema (co-20)
def create_item(item: Item) -> Item:  # => the Item body and Item response both appear in the schema (co-12)
    return item  # => round-tripped


if __name__ == "__main__":  # => run directly to INSPECT the generated schema without starting a server
    schema = app.openapi()  # => returns the dict FastAPI would serve at /openapi.json (co-20)
    print(sorted(schema["paths"].keys()))  # => Output: ['/items', '/items/{item_id}']
    print(schema["components"]["schemas"]["Item"]["required"])  # => Output: ['name', 'price']
