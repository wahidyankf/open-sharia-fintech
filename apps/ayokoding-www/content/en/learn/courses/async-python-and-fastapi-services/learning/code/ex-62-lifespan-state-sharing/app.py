"""Example 62: Sharing State via app state in a Lifespan.

A lifespan sets up shared state on app.state once at startup; every request reads it via request.app.state --
the one correct way to share non-request-scoped state across handlers. Run: uvicorn app:app --port 8000. (co-18)
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request  # => Request reads app.state (co-18)


class FeatureFlags:  # => shared configuration read by every request
    def __init__(self) -> None:
        self.new_search = True  # => a flag resolved once at startup


@asynccontextmanager  # => lifespan factory
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # => setup once at startup, teardown at shutdown (co-18)
    app.state.flags = FeatureFlags()  # => stash shared state on app.state (co-18)
    yield  # => the app runs here, every request reading the same flags
    # => no teardown needed for this in-memory object (co-18)


app = FastAPI(lifespan=lifespan)  # => register the lifespan (co-18)


@app.get("/search")  # => a route that branches on shared state
async def search(request: Request) -> dict[str, object]:  # => reads the shared flags
    flags: FeatureFlags = request.app.state.flags  # => the flags set ONCE at startup (co-18)
    return {"engine": "new" if flags.new_search else "old"}  # => reflects the shared flag (co-14)
