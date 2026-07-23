"""Capstone acceptance suite -- CRUD + validation + auth + pagination, all in one green run."""

import importlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

AUTH = {"Authorization": "Bearer s3cr3t-token-abc123"}


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("CAPSTONE_DB_PATH", str(tmp_path / "tasks.db"))  # => a FRESH DB file per test
    from app import main as main_module  # => imported here so the env var above is set BEFORE module load

    importlib.reload(main_module)
    return TestClient(main_module.app)


class TestHealthAndReadiness:  # => Step 1 of the capstone spec
    def test_health_is_always_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_ready_is_200_when_db_is_reachable(self, client: TestClient) -> None:
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}


class TestCrudRoundTrip:  # => Step 2 of the capstone spec
    def test_create_read_update_delete(self, client: TestClient) -> None:
        created = client.post("/tasks", json={"title": "write the report", "description": "Q3 summary"}, headers=AUTH)
        assert created.status_code == 201
        task_id = created.json()["id"]

        read = client.get(f"/tasks/{task_id}")  # => reads are open, no token needed
        assert read.status_code == 200
        assert read.json()["status"] == "todo"

        updated = client.put(
            f"/tasks/{task_id}",
            json={"title": "write the report", "description": "Q3 summary", "status": "done"},
            headers=AUTH,
        )
        assert updated.status_code == 200
        assert updated.json()["status"] == "done"

        deleted = client.delete(f"/tasks/{task_id}", headers=AUTH)
        assert deleted.status_code == 204

        gone = client.get(f"/tasks/{task_id}")
        assert gone.status_code == 404
        assert gone.json()["error"]["code"] == "not_found"

    def test_invalid_body_returns_structured_422(self, client: TestClient) -> None:
        response = client.post("/tasks", json={"title": ""}, headers=AUTH)  # => empty title violates min_length
        assert response.status_code == 422

    def test_invalid_status_on_put_is_422(self, client: TestClient) -> None:
        created = client.post("/tasks", json={"title": "x"}, headers=AUTH).json()
        response = client.put(
            f"/tasks/{created['id']}",
            json={"title": "x", "description": "", "status": "not_a_real_status"},
            headers=AUTH,
        )
        assert response.status_code == 422  # => co-10: the Literal status type rejects this


class TestTokenCheckMiddleware:  # => Step 3 of the capstone spec
    def test_create_without_token_is_401(self, client: TestClient) -> None:
        response = client.post("/tasks", json={"title": "x"})
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "unauthorized"

    def test_create_with_invalid_token_is_401(self, client: TestClient) -> None:
        response = client.post("/tasks", json={"title": "x"}, headers={"Authorization": "Bearer garbage"})
        assert response.status_code == 401

    def test_reads_never_require_a_token(self, client: TestClient) -> None:
        assert client.get("/tasks").status_code == 200
        assert client.get("/health").status_code == 200

    def test_put_and_delete_also_require_a_token(self, client: TestClient) -> None:
        created = client.post("/tasks", json={"title": "x"}, headers=AUTH).json()
        task_id = created["id"]
        assert client.put(f"/tasks/{task_id}", json={"title": "x", "description": "", "status": "todo"}).status_code == 401
        assert client.delete(f"/tasks/{task_id}").status_code == 401


class TestPaginationAndFiltering:  # => Step 4 of the capstone spec
    def test_pagination_window_and_metadata(self, client: TestClient) -> None:
        for i in range(15):
            client.post("/tasks", json={"title": f"task {i}"}, headers=AUTH)
        page = client.get("/tasks", params={"limit": 5, "offset": 0})
        body = page.json()
        assert len(body["items"]) == 5
        assert body["total"] == 15
        assert body["next"] == 5

        last_page = client.get("/tasks", params={"limit": 5, "offset": 10})
        assert len(last_page.json()["items"]) == 5
        assert last_page.json()["next"] is None

    def test_status_filter_narrows_results(self, client: TestClient) -> None:
        ids = [client.post("/tasks", json={"title": f"t{i}"}, headers=AUTH).json()["id"] for i in range(4)]
        for task_id in ids[:2]:  # => mark exactly TWO of the four as done
            client.put(f"/tasks/{task_id}", json={"title": "t", "description": "", "status": "done"}, headers=AUTH)
        response = client.get("/tasks", params={"status": "done", "limit": 50})
        body = response.json()
        assert body["total"] == 2  # => the FILTERED total, not all 4
        assert all(t["status"] == "done" for t in body["items"])

    def test_limit_over_maximum_is_422(self, client: TestClient) -> None:
        response = client.get("/tasks", params={"limit": 1000})
        assert response.status_code == 422
