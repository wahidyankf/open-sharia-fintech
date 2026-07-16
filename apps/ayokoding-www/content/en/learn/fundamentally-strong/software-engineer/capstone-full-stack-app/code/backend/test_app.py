"""Full-stack capstone -- the API integration test (topic 15 Software Testing, Step 4 of the
capstone spec): drives the real FastAPI app through Starlette's TestClient, against a fresh
SQLite file per test, covering the create -> read -> update round trip, validation, CORS
preflight/response headers, and 404s.
"""

import importlib
import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

FRONTEND_ORIGIN = "http://127.0.0.1:8121"


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv(
        "CAPSTONE2_DB_PATH", str(tmp_path / "tasks.db")
    )  # => a FRESH DB file per test
    monkeypatch.setenv("CAPSTONE2_FRONTEND_ORIGIN", FRONTEND_ORIGIN)
    from app import (
        main as main_module,
    )  # => imported here so the env vars above are set BEFORE module load

    importlib.reload(main_module)
    return TestClient(main_module.app)


class _UnreachableConnection:  # => a fake conn whose every query genuinely raises, so /ready's
    # => except sqlite3.OperationalError branch is exercised for real, not mocked away
    def execute(self, *_args: object, **_kwargs: object) -> None:
        raise sqlite3.OperationalError("database is locked")


class TestHealthAndReadiness:
    def test_health_is_always_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_ready_is_200_when_db_is_reachable(self, client: TestClient) -> None:
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}

    def test_ready_is_503_when_db_ping_fails(self, client: TestClient) -> None:
        from app import (
            main as main_module,
        )  # => same module the `client` fixture just reloaded

        def broken_get_db() -> Iterator[_UnreachableConnection]:
            yield _UnreachableConnection()

        main_module.app.dependency_overrides[main_module.get_db] = broken_get_db
        try:
            response = client.get("/ready")
        finally:
            main_module.app.dependency_overrides.clear()  # => never leak into later tests

        assert response.status_code == 503
        assert response.json() == {
            "status": "not_ready",
            "reason": "database is locked",
        }


class TestCrudRoundTrip:  # => Steps 1 and 3 of the capstone spec
    def test_create_read_update(self, client: TestClient) -> None:
        created = client.post(
            "/tasks", json={"title": "write the report", "description": "Q3 summary"}
        )
        assert created.status_code == 201
        task_id = created.json()["id"]
        assert created.json()["status"] == "todo"

        listed = client.get("/tasks")  # => the CORS-safe read endpoint -- Step 1
        assert listed.status_code == 200
        assert any(t["id"] == task_id for t in listed.json())

        read = client.get(f"/tasks/{task_id}")
        assert read.status_code == 200

        updated = client.put(  # => Step 3: the update half of the create/update form
            f"/tasks/{task_id}",
            json={
                "title": "write the report",
                "description": "Q3 summary",
                "status": "done",
            },
        )
        assert updated.status_code == 200
        assert updated.json()["status"] == "done"

        refetched = client.get(
            "/tasks"
        )  # => the list reflects the update after refetch
        refetched_task = next(t for t in refetched.json() if t["id"] == task_id)
        assert refetched_task["status"] == "done"

    def test_invalid_body_returns_structured_422(self, client: TestClient) -> None:
        response = client.post(
            "/tasks", json={"title": ""}
        )  # => empty title violates min_length
        assert response.status_code == 422

    def test_invalid_status_on_put_is_422(self, client: TestClient) -> None:
        created = client.post("/tasks", json={"title": "x"}).json()
        response = client.put(
            f"/tasks/{created['id']}",
            json={"title": "x", "description": "", "status": "not_a_real_status"},
        )
        assert response.status_code == 422  # => the Literal status type rejects this

    def test_update_of_missing_task_is_404(self, client: TestClient) -> None:
        response = client.put(
            "/tasks/999999", json={"title": "x", "description": "", "status": "todo"}
        )
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "not_found"

    def test_read_of_missing_task_is_404(self, client: TestClient) -> None:
        assert client.get("/tasks/999999").status_code == 404


class TestCors:  # => Step 1 of the capstone spec: "CORS-safe read endpoint"
    def test_allowed_origin_gets_the_header_back(self, client: TestClient) -> None:
        response = client.get("/tasks", headers={"Origin": FRONTEND_ORIGIN})
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == FRONTEND_ORIGIN

    def test_other_origin_gets_no_cors_header(self, client: TestClient) -> None:
        response = client.get("/tasks", headers={"Origin": "http://evil.example.com"})
        assert (
            response.status_code == 200
        )  # => the request itself still succeeds server-side...
        assert (
            "access-control-allow-origin" not in response.headers
        )  # ...but the browser
        # => will block the SCRIPT from reading the response, since no allow-list header names it

    def test_preflight_for_the_allowed_origin_succeeds(
        self, client: TestClient
    ) -> None:
        response = client.options(
            "/tasks",
            headers={
                "Origin": FRONTEND_ORIGIN,
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == FRONTEND_ORIGIN


class TestSecurityHeaders:  # => topic 17 hardening reused
    def test_every_response_carries_the_header_baseline(
        self, client: TestClient
    ) -> None:
        response = client.get("/health")
        assert response.headers["content-security-policy"] == "default-src 'self'"
        assert response.headers["x-content-type-options"] == "nosniff"
        assert "strict-transport-security" in response.headers
