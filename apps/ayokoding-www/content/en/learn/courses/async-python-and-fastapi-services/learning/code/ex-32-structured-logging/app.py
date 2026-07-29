"""Example 32: One Structured Log Line per Request.

A middleware emits one STRUCTURED (key=value) log line per request, so logs are grep-able and aggregatable --
not free-form prose. Run: uvicorn app:app --port 8000, then: curl localhost:8000/  (co-24, co-18)
"""

import logging  # => the standard-library logging module (co-24)
import time  # => request timing
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request  # => Request carries method + path (co-18)
from fastapi.responses import Response  # => status code is read from the response

app = FastAPI()  # => the ASGI application uvicorn serves

logging.basicConfig(level=logging.INFO, format="%(message)s")  # => one line per record, the message is JSON-ish
logger = logging.getLogger("app")  # => a named logger every handler/middleware shares (co-24)


@app.middleware("http")  # => wraps every request/response (co-18)
async def structured_log(  # => one structured record per request
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.perf_counter()  # => baseline
    response: Response = await call_next(request)  # => run the downstream handler
    elapsed_ms = (time.perf_counter() - start) * 1000.0  # => milliseconds
    # => a STRUCTURED line: fixed keys, machine-parseable -- the production-logging shape (co-24)
    logger.info(  # => emitted exactly once per request (co-18)
        "method=%s path=%s status=%d duration_ms=%.3f",  # => key=value pairs, stable across every route
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response  # => the unmodified response


@app.get("/")  # => a route that produces one log line when hit
def read_root() -> dict[str, str]:  # => minimal handler
    return {"msg": "logged"}  # => hitting this emits: method=GET path=/ status=200 duration_ms=...
