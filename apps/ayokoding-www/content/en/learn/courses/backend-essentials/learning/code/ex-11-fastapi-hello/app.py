"""Example 11: FastAPI Hello."""

from fastapi import FastAPI  # => the web framework this whole tier builds on

# => the ASGI application object uvicorn will serve -- this exact module-level
# => name ("app") is what "uvicorn app:app" means: module "app", attribute "app"
app = FastAPI()  # => uvicorn imports THIS exact module-level name


@app.get("/")  # => decorator-based ROUTING: GET "/" maps to read_root (co-07)
def read_root() -> dict[str, str]:
    """Return a dict -- FastAPI serializes it to a JSON response body."""
    # => contrast this with Example 1's raw-server equivalent: no manual
    # => json.dumps(), no manual Content-Type header, no manual send_response()
    return {"msg": "hello"}  # => FastAPI turns this into {"msg": "hello"} JSON
    # => and automatically sets Content-Type: application/json (co-09)
