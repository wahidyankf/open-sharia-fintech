"""Example 21: Read Request Header."""

from fastapi import FastAPI, Header  # => Header() reads an incoming HTTP header

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.get("/whoami")  # => a route whose only job is to echo request metadata
def whoami(x_request_id: str | None = Header(default=None)) -> dict[str, str | None]:
    """Header() maps a param name to a header -- FastAPI converts case/hyphens."""
    # => "x_request_id" reads the "X-Request-Id" header (underscores -> hyphens,
    # => case-insensitive, per RFC 9110's header-name rules) -- FastAPI does that
    # => name translation automatically; nothing here spells "X-Request-Id" out
    return {"x_request_id": x_request_id}  # => echoes whatever the client sent
    # => a client that never sends X-Request-Id gets back "x_request_id": null
