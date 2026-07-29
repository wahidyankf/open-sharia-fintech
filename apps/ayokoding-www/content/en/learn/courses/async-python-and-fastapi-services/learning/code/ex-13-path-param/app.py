"""Example 13: A Typed Path Parameter.

Run: uvicorn app:app --port 8000, then: curl localhost:8000/items/5  (co-11)
"""

from fastapi import FastAPI  # => the web framework (co-10)

app = FastAPI()  # => the ASGI application uvicorn serves


@app.get("/items/{item_id}")  # => {item_id} is a path-parameter PLACEHOLDER in the route template (co-11)
def read_item(item_id: int) -> dict[str, int]:  # => the matching name + int type = a typed PATH param
    # => a NON-numeric segment (e.g. /items/abc) fails validation with a 422 before this body runs (co-13)
    return {"item_id": item_id}  # => the SAME typed int, echoed back as JSON (co-14)
