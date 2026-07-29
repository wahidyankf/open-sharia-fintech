"""Example 26: Adding a Timing Header with Middleware.

An HTTP middleware wraps every request/response, adding an X-Process-Time header without touching any
handler. Run: uvicorn app:app --port 8000, then: curl -i localhost:8000/  (co-18)
"""

import time  # => only to measure request duration
from collections.abc import Awaitable, Callable  # => the typed shape of a middleware's call_next (co-18)

from fastapi import FastAPI, Request  # => Request is the inbound request the middleware forwards (co-18)
from fastapi.responses import Response  # => the outbound response the middleware mutates

app = FastAPI()  # => the ASGI application uvicorn serves


@app.middleware("http")  # => registers an HTTP middleware that wraps EVERY request/response (co-18)
async def add_timing_header(  # => call_next runs the downstream handler
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:  # => the middleware returns the (enriched) Response
    start = time.perf_counter()  # => capture the time BEFORE the handler runs
    response: Response = await call_next(request)  # => forward to the handler, await its response
    elapsed = time.perf_counter() - start  # => wall-clock duration of the whole handler chain
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"  # => mutate the outbound response (co-18)
    return response  # => the (now enriched) response is sent to the client


@app.get("/")  # => a route that knows nothing about timing -- the middleware adds it for free
def read_root() -> dict[str, str]:  # => a minimal handler
    return {"msg": "timed"}  # => the response body; the X-Process-Time header is added outside this function
