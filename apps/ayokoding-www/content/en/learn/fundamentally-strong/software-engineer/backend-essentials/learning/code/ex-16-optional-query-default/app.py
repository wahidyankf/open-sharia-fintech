"""Example 16: Optional Query Default."""

from fastapi import FastAPI  # => the web framework this whole tier builds on

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.get("/items")  # => a listing route -- the shape every later pagination
# => example (co-19) in this topic's Advanced tier eventually builds on
def list_items(limit: int = 10) -> dict[str, int]:
    """A default value makes the query param optional -- "= 10" is the default."""
    # => compare with Example 15's "q: str" (no default -> required): the
    # => PRESENCE of a default value is the ONLY thing that makes limit optional
    # => "?limit=5" sets limit=5; omitting "limit" entirely uses 10
    return {"limit": limit}  # => echoes whichever value was actually used
