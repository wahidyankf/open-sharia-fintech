"""Example 53: A remotebrowser Shaped Fan Out and Aggregate.

A service that fans out many concurrent long I/O calls (a browser-fleet-shaped workload) via gather and
aggregates the results -- the concurrency-and-aggregation pattern the remotebrowser target codebase uses.
Run: uvicorn app:app --port 8000, then: curl localhost:8000/fanout. (co-04, co-16, co-22)
"""

import asyncio  # => gather + semaphore (co-04)

from fastapi import FastAPI  # => the web framework (co-10)

app = FastAPI()  # => the ASGI application uvicorn serves

CONCURRENCY = 4  # => a bounded fleet size -- cap simultaneous in-flight calls (co-04)
_semaphore = asyncio.Semaphore(CONCURRENCY)  # => limits concurrent "browser" calls


async def run_browser(session_id: int) -> dict[str, object]:  # => a stand-in for one remote-browser command
    async with _semaphore:  # => never more than CONCURRENCY run at once (co-04)
        await asyncio.sleep(0.05)  # => simulate a slow remote-browser I/O wait (co-02, co-16)
        return {"session": session_id, "ok": True}  # => a per-call result


@app.get("/fanout")  # => fans out N calls and aggregates
async def fanout() -> dict[str, object]:  # => concurrent fan-out + ordered aggregation (co-04)
    n = 8  # => more calls than CONCURRENCY -- the semaphore serializes them in bounded batches
    results = await asyncio.gather(*(run_browser(i) for i in range(n)))  # => all run concurrently up to the cap (co-04)
    ok = sum(1 for r in results if r["ok"])  # => aggregate: count successes
    return {"total": n, "succeeded": ok, "results": list(results)}  # => aggregated payload (co-14, co-22)
