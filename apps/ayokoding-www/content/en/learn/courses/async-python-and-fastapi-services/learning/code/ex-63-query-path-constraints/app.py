"""Example 63: Query and Path Constraints.

Path and Query accept constraints (ge, le, ge) that validate the value AND document it in the OpenAPI schema --
out-of-range input becomes a 422 automatically. Run: uvicorn app:app --port 8000. (co-11, co-13)
"""

from fastapi import FastAPI, Path, Query  # => Path + Query carry constraints (co-11)

app = FastAPI()  # => the ASGI application uvicorn serves


@app.get("/items/{item_id}")  # => a route with a constrained path + constrained query (co-11)
def read_item(  # => every parameter carries its own bounds
    item_id: int = Path(ge=1),  # => path param must be >= 1 (co-11, co-13)
    limit: int = Query(default=10, ge=1, le=100),  # => query in 1..100, default 10 (co-13)
) -> dict[str, int]:  # => both validated before the handler runs
    return {"item_id": item_id, "limit": limit}  # => echoed, in-range guaranteed (co-14)
