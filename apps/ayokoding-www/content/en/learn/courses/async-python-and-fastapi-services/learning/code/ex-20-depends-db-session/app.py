"""Example 20: Injecting a Database Session with Depends.

An async generator dependency opens a session, yields it, and closes it -- once per request. Run:
uvicorn app:app --port 8000, then: curl localhost:8000/version  (co-15, co-16)
"""

from collections.abc import AsyncIterator  # => the typed shape of an async-generator dependency (co-15)

import aiosqlite  # => an async driver -- query waits yield to the loop instead of blocking (co-16)
from fastapi import Depends, FastAPI  # => Depends wires the provider (co-15)

app = FastAPI()  # => the ASGI application uvicorn serves
DB_PATH = ":memory:"  # => an in-memory SQLite DB for this self-contained example


async def get_session() -> AsyncIterator[aiosqlite.Connection]:  # => an ASYNC generator dependency (co-15, co-05)
    # => "async with" opens the connection and GUARANTEES close on exit, even if the handler raised (co-05)
    async with aiosqlite.connect(DB_PATH) as db:  # => acquire an async connection
        yield db  # => hand the live session to the handler for the duration of the request
    # => after the yield: the connection is closed automatically when the block exits (co-15 teardown)


@app.get("/version")  # => a route that NEEDS a database session
async def read_version(session: aiosqlite.Connection = Depends(get_session)) -> dict[str, str]:  # => injected
    # => the handler is async because it AWAITS the query -- a sync handler would block the loop (co-16)
    cursor = await session.execute("SELECT sqlite_version()")  # => an async query that yields to the loop
    row = await cursor.fetchone()  # => fetch the single result row
    version = str(row[0]) if row is not None else "unknown"  # => narrow to a plain string
    return {"sqlite_version": version}  # => the injected session did the work (co-15, co-14)
