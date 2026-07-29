"""Example 51: Graceful Shutdown Drains In Flight Work.

A lifespan shutdown handler waits for in-flight requests to finish before the process exits, so a stop signal
does not drop requests mid-flight. Run: uvicorn app:app --port 8000, then send SIGINT. (co-18, co-24)
"""

import asyncio  # => asyncio.Event + wait_for orchestrate the drain (co-24)

from fastapi import FastAPI  # => the web framework (co-10)

app = FastAPI()  # => the ASGI application uvicorn serves

_in_flight = 0  # => count of requests currently being served
_drained = asyncio.Event()  # => set when the in-flight count reaches zero at shutdown (co-24)


@app.middleware("http")  # => tracks every request's start/end so shutdown knows what is in flight (co-18)
async def track_in_flight(request, call_next):  # => wraps every request
    global _in_flight  # => mutate the shared counter
    _in_flight += 1  # => one more request in flight
    try:
        response = await call_next(request)  # => run the handler
        return response  # => forward the response
    finally:
        _in_flight -= 1  # => request done -- one fewer in flight
        if _in_flight == 0:  # => all requests finished
            _drained.set()  # => unblock a waiting shutdown (co-24)


@app.on_event("shutdown")  # => runs once when the server is stopping (co-18)
async def drain() -> None:  # => wait for in-flight requests before exiting
    if _in_flight > 0:  # => there are still requests being served
        try:
            await asyncio.wait_for(_drained.wait(), timeout=5.0)  # => bounded wait (co-24) -- never hang forever
        except asyncio.TimeoutError:  # => some request took longer than the deadline
            pass  # => exit anyway after the bound -- graceful, but not indefinite (co-24)


@app.get("/")  # => a route that contributes to the in-flight count
async def root() -> dict[str, str]:  # => minimal handler
    return {"msg": "ok"}  # => hitting this during shutdown is drained, not dropped
