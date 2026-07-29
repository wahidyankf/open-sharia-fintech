"""Example 35: Overriding a Dependency in Tests -- the test.

app.dependency_overrides swaps the real provider for a fake, so the handler uses the fake store. Run: pytest -v.
"""

import httpx  # => the async client (co-21)
import pytest
from httpx import ASGITransport

from app import UserStore, app, get_user_store  # => the app + its provider (co-15, co-21)


class FakeUserStore(UserStore):  # => a fake that NEVER touches a database
    async def current_user(self) -> str:  # => returns a fixed value, independent of any DB
        return "fake-user"  # => the value the test expects the handler to see


async def fake_provider():  # => a replacement provider yielding the fake store
    yield FakeUserStore()  # => same async-generator shape as the real one (co-15)


@pytest.mark.asyncio  # => run on an event loop
async def test_handler_uses_overridden_dependency() -> None:  # => proves the override took effect
    app.dependency_overrides[get_user_store] = fake_provider  # => SWAP real for fake (co-15, co-21)
    try:  # => ensure the override is cleared even if the request failed
        transport = ASGITransport(app=app)  # => in-process transport (co-21)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/me")  # => the handler now sees FakeUserStore, not UserStore
            assert response.status_code == 200
            assert response.json() == {"user": "fake-user"}  # => the FAKE value, proving the override worked
    finally:
        app.dependency_overrides.clear()  # => reset so other tests are unaffected (co-15)
