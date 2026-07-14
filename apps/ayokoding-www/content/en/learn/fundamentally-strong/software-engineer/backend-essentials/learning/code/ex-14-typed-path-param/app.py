"""Example 14: Typed Path Param."""

from fastapi import FastAPI  # => the web framework this whole tier builds on

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.get("/items/{item_id}")  # => {item_id} is a path parameter placeholder
def read_item(item_id: int) -> dict[str, int]:
    """FastAPI parses the path segment and converts it to int automatically."""
    # => the parameter name "item_id" MATCHES the "{item_id}" placeholder above
    # => -- that name match is how FastAPI knows this is a PATH param, not a
    # => query param (contrast with Example 15, where the name is NOT in the path)
    # => a non-numeric segment (e.g. "/items/abc") fails validation with a 422
    return {"item_id": item_id}  # => the SAME typed int, echoed back as JSON
