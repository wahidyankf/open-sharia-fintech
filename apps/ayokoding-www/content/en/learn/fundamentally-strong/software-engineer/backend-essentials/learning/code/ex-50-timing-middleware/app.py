"""Example 50: Middleware -- Timing Header."""  # => module docstring for this example

# => co-16: the clock starts BEFORE call_next() and stops AFTER it, so the
# => elapsed time genuinely covers routing plus the handler, not just this wrapper
import time  # => stdlib high-resolution clock -- no third-party dependency needed

from fastapi import FastAPI, Request  # => Request is what every middleware receives first
from starlette.middleware.base import (  # => co-16: the two building blocks every middleware needs
    BaseHTTPMiddleware,  # => the base class FastAPI's own middleware system builds on
    RequestResponseEndpoint,  # => the precise type of "the rest of the pipeline", for typing call_next
)  # => closes the multi-line import from starlette.middleware.base
from starlette.responses import Response  # => the type dispatch() must always return

app = FastAPI()  # => the ASGI application uvicorn will serve


class TimingMiddleware(BaseHTTPMiddleware):  # => co-16: wraps EVERY request/response pair
    async def dispatch(  # => co-16: dispatch()'s signature spans three lines
        self,
        request: Request,
        call_next: RequestResponseEndpoint,  # => call_next runs the rest of the app
    ) -> Response:  # => must return the Response that eventually reaches the client
        start = time.perf_counter()  # => co-16: wall-clock start, BEFORE the handler runs
        response = await call_next(request)  # => the handler (and any inner middleware) runs here
        elapsed = time.perf_counter() - start  # => elapsed time AFTER the handler returned
        response.headers["X-Process-Time"] = (  # => co-04: mutates the OUTGOING response headers
            f"{elapsed:.6f}"  # => co-04: seconds, formatted as a string response header
        )  # => closes the header assignment
        return response  # => the SAME response object, now carrying the timing header


app.add_middleware(TimingMiddleware)  # => applies to EVERY route, with zero per-route code

# => perf_counter(), not time.time() -- a monotonic clock immune to system
# => clock adjustments, which is what any real timing measurement needs


@app.get("/tasks")  # => co-08: a handler that knows NOTHING about timing
def list_tasks() -> list[dict[str, str]]:  # => a plain handler, unaware any middleware even exists
    return [{"title": "Buy milk"}]  # => the middleware measures this AFTER it returns
