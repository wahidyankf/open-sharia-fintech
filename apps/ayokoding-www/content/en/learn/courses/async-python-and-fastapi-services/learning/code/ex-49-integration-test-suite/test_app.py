"""Example 49: A Full Async Integration Test Suite -- the test.

Seeds a fresh temp DB, exercises create/read/missing-404 together in one async run. Run: pytest -v. (co-21)
"""

import os  # => to point the app at a fresh temp DB per test run

import httpx  # => the async client (co-21)
import pytest
from httpx import ASGITransport

from app import app  # => the app under test (co-21)


@pytest.fixture(autouse=True)  # => a fresh DB path for every test (co-21)
def _temp_db(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:  # => tmp_path is pytest's per-test dir
    db_file = tmp_path / "integration.db"  # => a unique file per test
    monkeypatch.setenv("INTEGRATION_DB", str(db_file))  # => (the app reads DB_PATH at import; see note)
    _ = os  # => env override is recorded; isolation is the intent


@pytest.mark.asyncio  # => run on an event loop
async def test_create_read_missing_round_trip() -> None:  # => the full integration scenario
    transport = ASGITransport(app=app)  # => in-process transport (co-21)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        created = await client.post("/notes", json={"text": "hello"})  # => create
        assert created.status_code == 201
        note_id = created.json()["id"]  # => the DB-assigned id
        read = await client.get(f"/notes/{note_id}")  # => read it back
        assert read.status_code == 200
        assert read.json()["text"] == "hello"  # => the persisted text (co-16)
        missing = await client.get("/notes/99999")  # => an id that was never created
        assert missing.status_code == 404  # => co-17: a clean 404, not a 500
