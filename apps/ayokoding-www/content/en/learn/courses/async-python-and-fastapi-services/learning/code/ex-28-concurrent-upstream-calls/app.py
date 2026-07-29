"""Example 28: Fanning Out Concurrent Upstream Calls.

A handler fans out to two slow upstream calls via gather -- the combined latency is ~the slower call, not the
sum. Run: uvicorn app:app --port 8000, then: curl localhost:8000/aggregate  (co-04, co-16)
"""

import asyncio  # => gather lives here (co-04)

from fastapi import FastAPI  # => the web framework (co-10)

app = FastAPI()  # => the ASGI application uvicorn serves


async def call_upstream(name: str, seconds: float) -> str:  # => a simulated slow upstream API call
    await asyncio.sleep(seconds)  # => yields to the loop while "waiting on the network" (co-02)
    return f"{name}@{seconds}s"  # => the upstream's response


@app.get("/aggregate")  # => a route that needs BOTH upstreams before it can respond
async def aggregate() -> dict[str, list[str]]:  # => gathers both concurrently
    # => gather runs both upstream calls at once -- the handler pays the SLOWER call's latency (co-04)
    results = await asyncio.gather(call_upstream("a", 0.10), call_upstream("b", 0.15))  # => ~0.15s, not 0.25s
    return {"results": list(results)}  # => both responses, in submission order (co-14)
