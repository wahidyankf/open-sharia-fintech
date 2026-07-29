"""Example 34: Testing a Validation Failure Path -- the test.

Asserts the 422 returned when a required field is missing -- the red/green test for co-13. Run: pytest -v.
"""

import httpx  # => the async client (co-21)
import pytest
from httpx import ASGITransport

from app import app  # => the app under test (co-21)


@pytest.mark.asyncio  # => run on an event loop
async def test_missing_field_returns_422() -> None:  # => the red/green test for the validation rule
    transport = ASGITransport(app=app)  # => in-process transport (co-21)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/items", json={})  # => an EMPTY body -- missing the required "name"
        assert response.status_code == 422  # => co-13: validation rejected it before the handler ran
