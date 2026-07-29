"""Example 33: Testing an Endpoint with Async httpx -- the test.

An async httpx client drives the app IN-PROCESS via ASGITransport -- no real socket, no running server.
Run: pytest -v  (co-21)
"""

import httpx  # => the async HTTP client used to exercise the app (co-21)
import pytest
from httpx import ASGITransport

from app import app  # => the ASGI app imported directly -- driven in-process (co-21)


@pytest.mark.asyncio  # => runs the test coroutine on an event loop (co-21)
async def test_root_returns_ok() -> None:  # => an async test function
    transport = ASGITransport(app=app)  # => wire the client directly to the app -- no network (co-21)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:  # => pooled client
        response = await client.get("/")  # => a real request/response cycle, in-process
        assert response.status_code == 200  # => co-03: the expected status
        assert response.json() == {"msg": "ok"}  # => the expected body (co-14)
