"""Example 38: A Concurrency Safe Shared Counter.

A shared counter guarded by an asyncio.Lock across concurrent requests -- without the lock, concurrent
read-modify-writes lose updates. Run: uvicorn app:app --port 8000, then fire N concurrent:
curl localhost:8000/inc  (co-23)
"""

import asyncio  # => asyncio.Lock guards the shared mutable state (co-23)

from fastapi import FastAPI  # => the web framework (co-10)

app = FastAPI()  # => the ASGI application uvicorn serves

_counter: int = 0  # => module-level shared state -- the thing concurrent coroutines must coordinate on (co-23)
_lock = asyncio.Lock()  # => a cooperative lock: only one coroutine holds it at a time (co-23)


@app.post("/inc")  # => a write route that mutates the shared counter
async def increment() -> dict[str, int]:  # => async so it can await the lock
    # => acquiring the lock makes the read-modify-write block ATOMIC across coroutines (co-23)
    async with _lock:  # => only one request enters this block at a time -- no lost updates
        global _counter  # => mutating module-level state
        _counter += 1  # => the critical section: read + modify + write, uninterrupted by another coroutine
        return {"count": _counter}  # => the new value, consistent under concurrency (co-14)


@app.get("/count")  # => a read route
async def count() -> dict[str, int]:  # => reads the shared counter
    async with _lock:  # => a read under the lock avoids reading mid-write (co-23)
        return {"count": _counter}  # => a stable snapshot (co-14)
