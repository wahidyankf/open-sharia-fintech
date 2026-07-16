"""Capstone acceptance suite -- auth, injection-safety, XSS-safety, headers, pagination,
all in one green run against the hardened app."""

import importlib
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv(
        "CAPSTONE_DB_PATH", str(tmp_path / "tasks.db")
    )  # => a FRESH DB file per test
    monkeypatch.setenv(
        "CAPSTONE_AUTH_SECRET", "test-only-secret-never-committed"
    )  # => co-17: test-scoped only
    from app import (
        main as main_module,
    )  # => imported here so the env vars above are set BEFORE module load

    importlib.reload(main_module)
    return TestClient(main_module.app)


def _register_and_login(
    client: TestClient, username: str = "alice", password: str = "Sup3rSecret!"
) -> str:
    client.post("/auth/register", json={"username": username, "password": password})
    login = client.post(
        "/auth/login", json={"username": username, "password": password}
    )
    token: str = login.json()["access_token"]
    return token


class TestHealthAndReadiness:  # => unchanged behavior from Backend-Essentials
    def test_health_is_always_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_ready_is_200_when_db_is_reachable(self, client: TestClient) -> None:
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}


class TestAuthArgon2id:  # => co-09, co-10, co-11, co-12: the NEW auth surface
    def test_register_then_login_succeeds_end_to_end(self, client: TestClient) -> None:
        token = _register_and_login(client)
        assert token != ""

    def test_stored_password_is_never_plaintext(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        _register_and_login(client, "bob", "AnotherSecret1!")
        conn = sqlite3.connect(
            tmp_path / "tasks.db"
        )  # => reads the DB FILE DIRECTLY, bypassing the API
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?", ("bob",)
        ).fetchone()
        stored_hash = str(row["password_hash"])
        assert stored_hash.startswith(
            "$argon2id$"
        )  # => co-09: a real PHC-format argon2id hash
        assert (
            "AnotherSecret1!" not in stored_hash
        )  # => the raw password is provably NOT in storage

    def test_login_rejects_wrong_password(self, client: TestClient) -> None:
        client.post(
            "/auth/register", json={"username": "carol", "password": "RightPassword1!"}
        )
        response = client.post(
            "/auth/login", json={"username": "carol", "password": "WrongPassword1!"}
        )
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "unauthorized"

    def test_login_unknown_user_gets_same_generic_error(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/auth/login", json={"username": "no_such_user", "password": "whatever12"}
        )
        assert response.status_code == 401
        assert (
            response.json()["error"]["message"] == "invalid username or password"
        )  # => co-23: no enumeration

    def test_register_rejects_hostile_username(self, client: TestClient) -> None:
        response = client.post(
            "/auth/register", json={"username": "admin'--", "password": "ValidPass1!"}
        )
        assert (
            response.status_code == 422
        )  # => co-07: the allow-list pattern rejects this before any SQL runs

    def test_register_rejects_short_password(self, client: TestClient) -> None:
        response = client.post(
            "/auth/register", json={"username": "dave", "password": "short"}
        )
        assert response.status_code == 422

    def test_duplicate_username_is_conflict(self, client: TestClient) -> None:
        client.post(
            "/auth/register", json={"username": "erin", "password": "FirstPass1!"}
        )
        response = client.post(
            "/auth/register", json={"username": "erin", "password": "SecondPass1!"}
        )
        assert response.status_code == 409


class TestCrudRoundTrip:  # => unchanged behavior from Backend-Essentials, now gated by REAL tokens
    def test_create_read_update_delete(self, client: TestClient) -> None:
        token = _register_and_login(client)
        auth_header = {"Authorization": f"Bearer {token}"}
        created = client.post(
            "/tasks",
            json={"title": "write the report", "description": "Q3 summary"},
            headers=auth_header,
        )
        assert created.status_code == 201
        task_id = created.json()["id"]

        read = client.get(f"/tasks/{task_id}")  # => reads are open, no token needed
        assert read.status_code == 200

        updated = client.put(
            f"/tasks/{task_id}",
            json={
                "title": "write the report",
                "description": "Q3 summary",
                "status": "done",
            },
            headers=auth_header,
        )
        assert updated.status_code == 200
        assert updated.json()["status"] == "done"

        deleted = client.delete(f"/tasks/{task_id}", headers=auth_header)
        assert deleted.status_code == 204

        gone = client.get(f"/tasks/{task_id}")
        assert gone.status_code == 404


class TestTokenCheckMiddleware:
    def test_create_without_token_is_401(self, client: TestClient) -> None:
        response = client.post("/tasks", json={"title": "x"})
        assert response.status_code == 401

    def test_create_with_garbage_token_is_401(self, client: TestClient) -> None:
        response = client.post(
            "/tasks",
            json={"title": "x"},
            headers={"Authorization": "Bearer garbage.notasignature"},
        )
        assert (
            response.status_code == 401
        )  # => co-11: a forged signature never verifies

    def test_reads_never_require_a_token(self, client: TestClient) -> None:
        assert client.get("/tasks").status_code == 200
        assert client.get("/health").status_code == 200


class TestSqlInjectionIsFixed:  # => co-01, co-03: the Step 1 attack, re-run against the SHIPPED code
    def test_injection_payload_returns_no_extra_rows(self, client: TestClient) -> None:
        token = _register_and_login(client)
        auth_header = {"Authorization": f"Bearer {token}"}
        client.post("/tasks", json={"title": "write the report"}, headers=auth_header)
        client.post(
            "/tasks", json={"title": "rotate prod db credentials"}, headers=auth_header
        )

        legit = client.get("/tasks/search", params={"q": "report"})
        assert len(legit.json()) == 1  # => a genuine substring match still works

        attack = client.get("/tasks/search", params={"q": "' OR '1'='1"})
        assert attack.status_code == 200
        assert (
            attack.json() == []
        )  # => the injection payload matches NO title substring anymore


class TestXssIsFixed:  # => co-01, co-06: the Step 3 attack, re-run against the SHIPPED code
    def test_view_route_escapes_hostile_title(self, client: TestClient) -> None:
        token = _register_and_login(client)
        auth_header = {"Authorization": f"Bearer {token}"}
        created = client.post(
            "/tasks", json={"title": "<script>alert(1)</script>"}, headers=auth_header
        )
        task_id = created.json()["id"]
        response = client.get(f"/tasks/{task_id}/view")
        assert response.status_code == 200
        assert (
            "<script>" not in response.text
        )  # => the payload never appears as executable markup
        assert (
            "&lt;script&gt;" in response.text
        )  # => it appears ONLY as inert, escaped text


class TestSecurityHeaders:  # => co-19
    def test_headers_present_on_every_response(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.headers["content-security-policy"] == "default-src 'self'"
        assert response.headers["x-content-type-options"] == "nosniff"
        assert "strict-transport-security" in response.headers

    def test_headers_present_even_on_error_responses(self, client: TestClient) -> None:
        response = client.get("/tasks/999999")
        assert response.status_code == 404
        assert (
            response.headers["x-content-type-options"] == "nosniff"
        )  # => the middleware wraps EVERY response


class TestPaginationAndFiltering:  # => unchanged behavior from Backend-Essentials
    def test_pagination_window_and_metadata(self, client: TestClient) -> None:
        token = _register_and_login(client)
        auth_header = {"Authorization": f"Bearer {token}"}
        for i in range(15):
            client.post("/tasks", json={"title": f"task {i}"}, headers=auth_header)
        page = client.get("/tasks", params={"limit": 5, "offset": 0})
        body = page.json()
        assert len(body["items"]) == 5
        assert body["total"] == 15
        assert body["next"] == 5

    def test_limit_over_maximum_is_422(self, client: TestClient) -> None:
        response = client.get("/tasks", params={"limit": 1000})
        assert response.status_code == 422
