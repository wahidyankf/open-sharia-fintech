"""Example 42: An In Process Rate Limit Middleware.

A simple in-process rate limiter as middleware: a lock-guarded per-client counter allows N requests per window,
rejecting the rest with 429. Run: uvicorn app:app --port 8000, then hit / many times fast. (co-18, co-23)
"""

import asyncio  # => asyncio.Lock guards the shared limiter state (co-23)
import time  # => wall-clock for the window
from collections.abc import Awaitable, Callable  # => the typed shape of call_next (co-18)

from fastapi import FastAPI, Request  # => Request identifies the caller (co-18)
from fastapi.responses import JSONResponse, Response  # => the 429 response

app = FastAPI()  # => the ASGI application uvicorn serves

MAX_HITS = 3  # => allow this many hits per window
WINDOW = 1.0  # => the window length in seconds
_hits: dict[str, list[float]] = {}  # => caller -> timestamps within the current window (co-23)
_lock = asyncio.Lock()  # => guards _hits across concurrent requests (co-23)


@app.middleware("http")  # => wraps every request (co-18)
async def rate_limit(  # => call_next runs the downstream handler
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    client = request.client.host if request.client else "unknown"  # => identify the caller
    now = time.monotonic()  # => a monotonic clock for window math
    async with _lock:  # => the critical section -- no lost updates under concurrency (co-23)
        recent = [t for t in _hits.get(client, []) if now - t < WINDOW]  # => drop timestamps outside the window
        if len(recent) >= MAX_HITS:  # => over the limit for this window
            return JSONResponse(status_code=429, content={"error": "rate limited"})  # => 429 Too Many Requests
        recent.append(now)  # => record this hit
        _hits[client] = recent  # => store the updated list
    return await call_next(request)  # => under the limit -- proceed to the handler


@app.get("/")  # => a route that is rate-limited by the middleware above
def read_root() -> dict[str, str]:  # => minimal handler
    return {"msg": "ok"}  # => only the first MAX_HITS calls per window return 200
