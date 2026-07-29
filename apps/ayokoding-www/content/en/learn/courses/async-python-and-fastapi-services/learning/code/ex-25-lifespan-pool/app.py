"""Example 25: Opening a Pool Once in a Lifespan Handler.

A lifespan context manager opens a shared resource ONCE at startup and closes it ONCE at shutdown, instead of
per request. Run: uvicorn app:app --port 8000, then: curl localhost:8000/pool  (co-18)
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager  # => the decorator that turns an async gen into a lifespan (co-18)

from fastapi import FastAPI, Request  # => Request reads app.state (co-18)


class Pool:  # => a stand-in for a connection pool / HTTP client opened once, shared by every request
    def __init__(self) -> None:
        self.open = False  # => not yet opened

    async def open_pool(self) -> None:  # => expensive setup that must NOT repeat per request (co-18)
        self.open = True  # => mark as ready

    async def close_pool(self) -> None:  # => teardown that runs exactly once on shutdown (co-18)
        self.open = False  # => mark as closed


@asynccontextmanager  # => makes the function below usable as FastAPI's lifespan= argument (co-18)
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # => runs once at startup, once at shutdown
    pool = Pool()  # => create the shared resource
    await pool.open_pool()  # => STARTUP: open before the app serves a single request
    app.state.pool = pool  # => stash it where every request can reach it (co-18)
    yield  # => the app runs here, serving many requests that all share the one pool
    await pool.close_pool()  # => SHUTDOWN: close after the app stops serving (co-18)


app = FastAPI(lifespan=lifespan)  # => register the lifespan handler (co-18)


@app.get("/pool")  # => a route that reads the shared pool
async def pool_status(request: Request) -> dict[str, bool]:  # => Request gives access to app.state
    pool: Pool = request.app.state.pool  # => the pool opened ONCE at startup -- shared, not per-request
    return {"open": pool.open}  # => confirms the shared resource is live (co-14)
