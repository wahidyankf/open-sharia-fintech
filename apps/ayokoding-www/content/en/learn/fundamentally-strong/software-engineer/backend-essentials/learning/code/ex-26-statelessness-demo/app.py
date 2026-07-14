"""Example 26: Statelessness Demo."""

from fastapi import FastAPI, Header  # => Header() reads an incoming HTTP header

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.get("/whoami")  # => a route whose response depends only on THIS request
def whoami(x_caller: str | None = Header(default=None)) -> dict[str, str]:
    """Nothing here is remembered between calls -- every request is self-contained."""
    # => no module-level "last caller" variable is read or written -- the handler
    # => has ZERO memory of any request that came before this one (co-05)
    # => contrast with Example 24's `items` dict: THAT is intentional, in-process
    # => state (a fake database). THIS handler deliberately holds none at all
    caller = x_caller if x_caller is not None else "anonymous"
    # => the ternary reduces "no header sent" to a readable default value
    return {"you_are": caller}  # => derived ENTIRELY from THIS request's own header
