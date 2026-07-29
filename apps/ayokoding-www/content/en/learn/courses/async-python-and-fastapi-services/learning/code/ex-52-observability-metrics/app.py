"""Example 52: Observability Metrics on an Endpoint.

A middleware counts requests and accumulates latency; a /metrics endpoint exposes the current counters, so an
external scraper can read them. Run: uvicorn app:app --port 8000, then curl localhost:8000/metrics. (co-24, co-18)
"""

import time  # => request timing
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request  # => Request carries method + path (co-18)
from fastapi.responses import PlainTextResponse, Response  # => a text metrics body

app = FastAPI()  # => the ASGI application uvicorn serves

_request_count = 0  # => a monotonic counter scraped at /metrics (co-24)
_latency_seconds = 0.0  # => accumulated latency, scraped at /metrics (co-24)


@app.middleware("http")  # => wraps every request to update the metrics (co-18)
async def record_metrics(  # => call_next runs the downstream handler
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    global _request_count, _latency_seconds  # => mutate the shared counters
    start = time.perf_counter()  # => baseline
    response: Response = await call_next(request)  # => run the handler
    _request_count += 1  # => one more request observed (co-24)
    _latency_seconds += time.perf_counter() - start  # => accumulate latency (co-24)
    return response  # => the unmodified response


@app.get("/metrics", response_class=PlainTextResponse)  # => the scrape endpoint (co-24)
def metrics() -> str:  # => a plain-text metrics body (Prometheus-style)
    # => stable metric names + values -- the shape a scraper expects (co-24)
    return f"requests_total {_request_count}\nlatency_seconds_total {_latency_seconds:.6f}\n"


@app.get("/")  # => a route that, when hit, increments the counters above
def root() -> dict[str, str]:  # => minimal handler
    return {"msg": "ok"}  # => hitting this moves requests_total up by one
