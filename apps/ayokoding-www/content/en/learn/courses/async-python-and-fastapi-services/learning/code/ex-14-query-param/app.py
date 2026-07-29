"""Example 14: A Typed Query Parameter.

Run: uvicorn app:app --port 8000, then: curl 'localhost:8000/items' and
curl 'localhost:8000/items?limit=3'  (co-11)
"""

from fastapi import FastAPI  # => the web framework (co-10)

app = FastAPI()  # => the ASGI application uvicorn serves


@app.get("/items")  # => no "{limit}" placeholder here, so limit is inferred as a QUERY param (co-11)
def list_items(limit: int = 10) -> dict[str, int]:  # => a DEFAULT makes the param OPTIONAL ("= 10")
    # => "?limit=3" sets limit=3; omitting "limit" entirely uses the default 10 (co-11)
    return {"limit": limit}  # => echoes whichever value was actually used (co-14)
