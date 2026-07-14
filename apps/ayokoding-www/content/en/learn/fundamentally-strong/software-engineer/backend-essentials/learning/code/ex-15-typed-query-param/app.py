"""Example 15: Typed Query Param."""

from fastapi import FastAPI  # => the web framework this whole tier builds on

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.get("/search")  # => note: no "{q}" placeholder anywhere in this path
def search(q: str) -> dict[str, str]:
    """A parameter NOT in the path string is inferred as a required query param."""
    # => "q" does not appear inside "/search" above, so FastAPI infers it is a
    # => QUERY param instead -- the opposite inference rule from Example 14's
    # => path param, and it has no default value, so it is REQUIRED, not optional
    # => "?q=hi" becomes q="hi"; omitting "q" entirely returns a 422 (it is required)
    return {"query": q}  # => echoes the parsed, typed query value back
