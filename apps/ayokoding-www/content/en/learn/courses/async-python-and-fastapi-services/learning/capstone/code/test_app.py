"""Capstone async FastAPI service -- async acceptance suite (co-21).

Drives the app in-process via httpx ASGITransport, each test against a FRESH temp DB. Run: pytest -v.
"""

from pathlib import Path

import httpx  # => the async client (co-21)
import pytest
from httpx import ASGITransport

from app import main  # => the app under test (co-21)
from app.main import app  # => the ASGI application


@pytest.fixture()
def client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> httpx.AsyncClient:  # => a client per test
    db_file = tmp_path / "capstone.db"  # => a FRESH DB file per test
    main.settings.db_path = str(
        db_file
    )  # => point the shared settings at the temp file (co-24)
    transport = ASGITransport(
        app=app
    )  # => in-process transport -- runs startup (init_db) against the temp DB (co-21)
    return httpx.AsyncClient(
        transport=transport, base_url="http://test"
    )  # => a pooled client


@pytest.mark.asyncio
async def test_health_is_200(client: httpx.AsyncClient) -> None:  # => liveness, no DB
    async with client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_crud_round_trip(
    client: httpx.AsyncClient,
) -> None:  # => create, read, update, delete (co-16, co-17)
    async with client:
        created = await client.post(
            "/tasks", json={"title": "write report", "description": "Q3"}
        )
        assert created.status_code == 201
        task_id = created.json()["id"]

        read = await client.get(
            f"/tasks/{task_id}"
        )  # => reads back the created row (co-16)
        assert read.status_code == 200
        assert read.json()["status"] == "todo"

        updated = await client.put(  # => update -> done
            f"/tasks/{task_id}",
            json={"title": "write report", "description": "Q3", "status": "done"},
        )
        assert updated.status_code == 200
        assert updated.json()["status"] == "done"

        deleted = await client.delete(f"/tasks/{task_id}")  # => delete (co-17)
        assert deleted.status_code == 204

        gone = await client.get(f"/tasks/{task_id}")  # => now missing -> 404 (co-17)
        assert gone.status_code == 404


@pytest.mark.asyncio
async def test_invalid_body_returns_422(
    client: httpx.AsyncClient,
) -> None:  # => validation at the boundary (co-13)
    async with client:
        response = await client.post(
            "/tasks", json={"title": ""}
        )  # => empty title violates min_length
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_pagination_and_filter(
    client: httpx.AsyncClient,
) -> None:  # => pagination + filtering (co-11)
    async with client:
        for i in range(5):  # => seed 5 tasks
            await client.post("/tasks", json={"title": f"task {i}"})
        page = await client.get(
            "/tasks", params={"limit": 2, "offset": 0}
        )  # => first page of 2
        body = page.json()
        assert len(body["items"]) == 2
        assert body["total"] == 5
        assert body["next"] == 2  # => a next page exists


@pytest.mark.asyncio
async def test_streaming_endpoint(
    client: httpx.AsyncClient,
) -> None:  # => the streaming endpoint (co-22)
    async with client:
        response = await client.get("/events")
        assert response.status_code == 200
        assert (
            "event" in response.text
        )  # => the streamed body arrived incrementally (co-22)
