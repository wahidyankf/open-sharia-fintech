"""Example 22: Set Response Header."""

from fastapi import FastAPI, Response  # => Response is injected to let a handler set headers

app = FastAPI()  # => the ASGI application uvicorn will serve


@app.get("/version")  # => a route that reports a build/version header
def version(response: Response) -> dict[str, str]:
    """FastAPI injects a Response object when a handler declares that param."""
    # => declaring "response: Response" as a parameter is a form of dependency
    # => injection (co-23 previews here) -- FastAPI supplies the LIVE response
    # => object this specific request will use, before the handler even runs
    response.headers["X-App-Version"] = "1.0.0"  # => set BEFORE returning the body
    # => mutating .headers here still lands on the wire -- the return below
    # => supplies only the BODY, not the headers, which are already queued
    return {"ok": "true"}  # => the header rides along with this JSON body
