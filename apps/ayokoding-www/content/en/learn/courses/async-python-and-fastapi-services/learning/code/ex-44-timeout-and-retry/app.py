"""Example 44: Timeout and Bounded Retry on an Upstream.

An upstream call wrapped in a timeout plus a BOUNDED retry -- a slow or failing upstream is cut off after a
fixed deadline, not allowed to stall the loop indefinitely. Run: uvicorn app:app --port 8000. (co-17, co-06)
"""

import asyncio  # => asyncio.timeout enforces a deadline (co-06)

from fastapi import FastAPI, HTTPException  # => HTTPException maps a failure (co-17)

app = FastAPI()  # => the ASGI application uvicorn serves

MAX_ATTEMPTS = 3  # => a BOUNDED retry -- never an unbounded loop (co-06)
TIMEOUT = 0.10  # => the per-attempt deadline in seconds


async def flaky_upstream(attempt: int) -> str:  # => a stand-in that fails until the 3rd attempt
    await asyncio.sleep(0.05)  # => simulates network latency (co-02)
    if attempt < 2:  # => fail the first two attempts
        raise RuntimeError("upstream unavailable")  # => a transient failure
    return "upstream-data"  # => succeeds on the third attempt


@app.get("/fetch")  # => a route that calls the flaky upstream with a timeout + retry
async def fetch() -> dict[str, str]:  # => bounded retry loop
    last_error: str = ""  # => remembers the most recent failure for the final 503
    for attempt in range(MAX_ATTEMPTS):  # => a BOUNDED number of attempts (co-06)
        try:
            async with asyncio.timeout(TIMEOUT):  # => cut off a slow call after TIMEOUT seconds (co-06)
                return {"data": await flaky_upstream(attempt)}  # => success -- return immediately
        except (RuntimeError, TimeoutError) as exc:  # => a transient failure or a timeout -> retry
            last_error = str(exc)  # => record and try again
    raise HTTPException(status_code=503, detail=f"upstream failed: {last_error}")  # => exhausted retries -> 503 (co-17)
