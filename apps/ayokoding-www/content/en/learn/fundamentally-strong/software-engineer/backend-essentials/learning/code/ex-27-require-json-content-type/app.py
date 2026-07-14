"""Example 27: Require JSON Content-Type."""

from fastapi import FastAPI  # => the web framework this whole tier builds on
from pydantic import BaseModel  # => Pydantic models are FastAPI's validation vocabulary

# => strict_content_type=True is the FastAPI 0.132.0+ DEFAULT -- no code below
# => opts into it explicitly; it is already active on this bare `FastAPI()` call
app = FastAPI()  # => the ASGI application uvicorn will serve


class Note(BaseModel):  # => a body FastAPI can only parse from a JSON-typed request
    """A body FastAPI can only parse from an application/json-typed request."""

    text: str  # => the one required field this minimal note model carries


@app.post("/notes")  # => a route whose Content-Type enforcement is a framework default
def create_note(note: Note) -> Note:
    """A wrong/missing Content-Type means the body is never even parsed as JSON."""
    # => this is co-21's "framework default" case: nothing in THIS handler, or
    # => anywhere else in this file, checks Content-Type by hand
    # => that unparsed body then fails Note's validation, and FastAPI's own
    # => native default returns 422 -- no hand-written check appears anywhere here
    return note  # => only reached when Content-Type AND the body both validate
