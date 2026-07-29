"""Example 75: An Idempotency Key for Writes.

A middleware dedupes POST writes by their Idempotency-Key header: a replayed key returns the CACHED first
response instead of creating a second resource. Run: uvicorn app:app --port 8000, then POST twice with the
same key. (co-18, co-23)
"""

import asyncio  # => asyncio.Lock guards the cache (co-23)

from fastapi import FastAPI, Request, Response  # => Request reads the header (co-18)

app = FastAPI()  # => the ASGI application uvicorn serves

_cache: dict[str, tuple[int, bytes]] = {}  # => idempotency-key -> (status, body) of the FIRST call (co-23)
_lock = asyncio.Lock()  # => guards _cache against concurrent replays (co-23)


@app.middleware("http")  # => wraps every request (co-18)
async def idempotency(request: Request, call_next) -> Response:  # => dedupes writes by key
    key = request.headers.get("Idempotency-Key")  # => the dedup key (co-18)
    if request.method == "POST" and key is not None:  # => only POST writes are deduped
        async with _lock:  # => the critical section -- no race on the cache (co-23)
            cached = _cache.get(key)  # => a prior result for this key?
        if cached is not None:  # => a replay -> return the cached first response
            status, body = cached  # => the original status + body
            return Response(content=body, status_code=status, media_type="application/json")  # => the SAME response (co-23)
        response: Response = await call_next(request)  # => first call -> run the handler
        async with _lock:  # => cache it under the lock
            _cache[key] = (response.status_code, response.body)  # => store for future replays (co-23)
        return response  # => the first-call response
    return await call_next(request)  # => non-POST or no key -> pass through unchanged


@app.post("/orders")  # => a write route protected by idempotency
async def create_order() -> dict[str, int]:  # => would create a row in a real service
    return {"created": 1}  # => a replayed key returns THIS cached body, not a second create (co-14)
