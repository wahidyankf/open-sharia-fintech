"""Example 43: An Async HTTP Client Service with a Pool.

A pooled async httpx client opened ONCE in a lifespan and reused across requests, so connection pooling
actually pays off instead of a fresh client per call. Run: uvicorn app:app --port 8000. (co-16, co-18)
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager  # => turns an async gen into a lifespan (co-18)

import httpx  # => the async HTTP client (co-16)
from fastapi import FastAPI, Request  # => Request reads app.state (co-18)


@asynccontextmanager  # => lifespan factory
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # => open once at startup, close at shutdown (co-18)
    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:  # => a POOLED client reused by every request
        app.state.client = client  # => stash it on app.state (co-18)
        yield  # => the app serves many requests sharing the one client
    # => the async with closes the client (and its pool) on shutdown (co-18)


app = FastAPI(lifespan=lifespan)  # => register the lifespan (co-18)


@app.get("/fetch")  # => a route that calls an upstream using the shared client
async def fetch(request: Request) -> dict[str, str]:  # => reads the shared client
    client: httpx.AsyncClient = request.app.state.client  # => the pooled client -- reused, not created per call (co-18)
    try:
        response = await client.get("https://example.com")  # => an async upstream call (co-16)
        return {"status": "ok", "upstream_status": str(response.status_code)}  # => the upstream's status (co-14)
    except httpx.HTTPError as exc:  # => a typed upstream failure
        return {"status": "error", "reason": str(exc)}  # => a structured error, never a 500 traceback (co-17)
