"""Example 21: An Async Database Query Yields to the Loop.

A handler that AWAITS its queries keeps the event loop free to serve other requests during each query's
latency -- the central throughput win of async DB access. Run: uvicorn app:app --port 8000, then:
curl localhost:8000/now  (co-16)
"""

from collections.abc import AsyncIterator

import aiosqlite  # => the async driver -- query waits yield to the loop (co-16)
from fastapi import Depends, FastAPI  # => Depends injects the session (co-15)

app = FastAPI()  # => the ASGI application uvicorn serves
DB_PATH = ":memory:"


async def get_session() -> AsyncIterator[aiosqlite.Connection]:  # => one session per request, opened+closed (co-15)
    async with aiosqlite.connect(DB_PATH) as db:  # => async acquire
        yield db  # => hand the live session to the handler
    # => closed automatically on block exit


@app.get("/now")  # => a route whose entire latency is one async query
async def now(session: aiosqlite.Connection = Depends(get_session)) -> dict[str, str]:  # => injected session
    # => AWAITING the query means other requests keep flowing during this call's latency (co-16, co-02)
    cursor = await session.execute("SELECT datetime('now')")  # => async -- yields control while the DB works
    row = await cursor.fetchone()  # => fetch one row, also awaited
    now_str = str(row[0]) if row is not None else ""  # => narrow to a plain string
    return {"now": now_str}  # => the loop stayed responsive the whole time (co-16)
