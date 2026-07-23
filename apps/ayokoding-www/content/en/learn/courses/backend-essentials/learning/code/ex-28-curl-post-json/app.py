"""Example 28: curl POST JSON."""

from fastapi import FastAPI  # => the web framework this whole tier builds on
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

app = FastAPI()  # => the ASGI application uvicorn will serve


class Echo(BaseModel):  # => a body echoed straight back, proving the round trip
    """A body echoed straight back -- proves the full round-trip works end to end."""

    message: str  # => arbitrary text the caller sends
    count: int  # => a second, differently-typed field in the same body
    # => str AND int in one model confirms co-10's validation checks BOTH types


@app.post("/echo")  # => the final beginner-tier route; curl exercises it below
def echo(payload: Echo) -> Echo:
    """The dev loop (co-22): serve with uvicorn, exercise with curl, read JSON back."""
    # => this is the smallest possible "does the whole pipeline work" example:
    # => curl sends JSON -> FastAPI parses+validates it (co-10, co-13) -> this
    # => handler returns it unchanged -> FastAPI serializes it back out (co-09)
    return payload  # => whatever curl sent, serialized straight back out
    # => byte-for-byte the same shape, just round-tripped through validation
