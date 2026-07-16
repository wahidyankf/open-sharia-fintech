"""Pass-1 capstone: integration test -- exercises the REAL FastAPI app through Starlette's
`TestClient` (topic 15's top of the pyramid): HTTP request in, HTTP response out, a REAL
SQLite file underneath, auth + validation + persistence all wired together as they would be
in production, only the transport is in-process instead of a socket.
"""

import importlib
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv(
        "CAPSTONE1_DB_PATH", str(tmp_path / "habits.db")
    )  # => a FRESH DB file per test
    monkeypatch.setenv("CAPSTONE1_AUTH_SECRET", "test-only-secret-never-committed")
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


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


class TestHealthAndReadiness:
    def test_health_is_always_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_ready_is_200_when_db_is_reachable(self, client: TestClient) -> None:
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}


class TestAuth:
    def test_register_then_login_succeeds_end_to_end(self, client: TestClient) -> None:
        token = _register_and_login(client)
        assert token != ""

    def test_stored_password_is_never_plaintext(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        _register_and_login(client, "bob", "AnotherSecret1!")
        conn = sqlite3.connect(
            tmp_path / "habits.db"
        )  # => reads the DB FILE DIRECTLY, bypassing the API
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?", ("bob",)
        ).fetchone()
        stored_hash = str(row["password_hash"])
        assert stored_hash.startswith(
            "$argon2id$"
        )  # => a real PHC-format argon2id hash
        assert (
            "AnotherSecret1!" not in stored_hash
        )  # => the raw password is provably NOT in storage

    def test_hostile_username_is_rejected_by_the_allow_list(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/auth/register", json={"username": "admin'--", "password": "Sup3rSecret!"}
        )
        assert (
            response.status_code == 422
        )  # => Pydantic's Field(pattern=...) rejects it before any handler runs

    def test_wrong_password_gets_the_same_generic_error_as_unknown_user(
        self, client: TestClient
    ) -> None:
        _register_and_login(client, "carol", "RightPassword1!")
        wrong = client.post(
            "/auth/login", json={"username": "carol", "password": "WrongPassword1!"}
        )
        unknown = client.post(
            "/auth/login",
            json={"username": "nosuchuser", "password": "WrongPassword1!"},
        )
        assert wrong.status_code == 401
        assert unknown.status_code == 401
        assert (
            wrong.json() == unknown.json()
        )  # => identical body -- no username-enumeration signal


class TestHabitsRequireAuth:
    def test_unauthenticated_read_is_rejected(self, client: TestClient) -> None:
        response = client.get("/habits")
        assert response.status_code == 401

    def test_unauthenticated_create_is_rejected(self, client: TestClient) -> None:
        response = client.post("/habits", json={"name": "Read 20 minutes"})
        assert response.status_code == 401


class TestHabitsCrudAndStreak:
    def test_create_checkin_and_streak_round_trip(self, client: TestClient) -> None:
        token = _register_and_login(client)
        created = client.post(
            "/habits", json={"name": "Read 20 minutes"}, headers=_auth_headers(token)
        )
        assert created.status_code == 201
        habit_id = created.json()["id"]
        assert created.json()["current_streak"] == 0

        checkin = client.post(
            f"/habits/{habit_id}/checkins", json={}, headers=_auth_headers(token)
        )
        assert checkin.status_code == 201
        assert checkin.json()["current_streak"] == 1

        fetched = client.get(f"/habits/{habit_id}", headers=_auth_headers(token))
        assert fetched.status_code == 200
        assert fetched.json()["current_streak"] == 1
        assert fetched.json()["checkin_count"] == 1

    def test_checkin_on_the_same_day_twice_does_not_double_count(
        self, client: TestClient
    ) -> None:
        token = _register_and_login(client)
        habit_id = client.post(
            "/habits", json={"name": "Floss"}, headers=_auth_headers(token)
        ).json()["id"]
        client.post(
            f"/habits/{habit_id}/checkins", json={}, headers=_auth_headers(token)
        )
        second = client.post(
            f"/habits/{habit_id}/checkins", json={}, headers=_auth_headers(token)
        )
        assert second.json()["checkin_count"] == 1  # => idempotent, not 2

    def test_invalid_habit_name_yields_a_structured_error(
        self, client: TestClient
    ) -> None:
        token = _register_and_login(client)
        response = client.post(
            "/habits", json={"name": ""}, headers=_auth_headers(token)
        )
        assert response.status_code == 422
        assert "detail" in response.json()

    def test_one_user_cannot_read_another_users_habit(self, client: TestClient) -> None:
        token_a = _register_and_login(client, "dave", "Sup3rSecret!")
        token_b = _register_and_login(client, "erin", "Sup3rSecret!")
        habit_id = client.post(
            "/habits", json={"name": "Dave's habit"}, headers=_auth_headers(token_a)
        ).json()["id"]
        cross_user = client.get(f"/habits/{habit_id}", headers=_auth_headers(token_b))
        assert (
            cross_user.status_code == 404
        )  # => not 403 -- existence isn't confirmed to a non-owner either

    def test_one_user_cannot_check_in_another_users_habit(
        self, client: TestClient
    ) -> None:
        token_a = _register_and_login(client, "dave", "Sup3rSecret!")
        token_b = _register_and_login(client, "erin", "Sup3rSecret!")
        habit_id = client.post(
            "/habits", json={"name": "Dave's habit"}, headers=_auth_headers(token_a)
        ).json()["id"]
        cross_user = client.post(
            f"/habits/{habit_id}/checkins", json={}, headers=_auth_headers(token_b)
        )
        assert (
            cross_user.status_code == 404
        )  # => not 403 -- existence isn't confirmed to a non-owner either

    def test_one_user_cannot_archive_another_users_habit(
        self, client: TestClient
    ) -> None:
        token_a = _register_and_login(client, "dave", "Sup3rSecret!")
        token_b = _register_and_login(client, "erin", "Sup3rSecret!")
        habit_id = client.post(
            "/habits", json={"name": "Dave's habit"}, headers=_auth_headers(token_a)
        ).json()["id"]
        cross_user = client.post(
            f"/habits/{habit_id}/archive", headers=_auth_headers(token_b)
        )
        assert (
            cross_user.status_code == 404
        )  # => not 403 -- existence isn't confirmed to a non-owner either

    def test_one_user_cannot_delete_another_users_habit(
        self, client: TestClient
    ) -> None:
        token_a = _register_and_login(client, "dave", "Sup3rSecret!")
        token_b = _register_and_login(client, "erin", "Sup3rSecret!")
        habit_id = client.post(
            "/habits", json={"name": "Dave's habit"}, headers=_auth_headers(token_a)
        ).json()["id"]
        cross_user = client.delete(
            f"/habits/{habit_id}", headers=_auth_headers(token_b)
        )
        assert (
            cross_user.status_code == 404
        )  # => not 403 -- existence isn't confirmed to a non-owner either

    def test_archive_hides_a_habit_from_the_default_list(
        self, client: TestClient
    ) -> None:
        token = _register_and_login(client)
        habit_id = client.post(
            "/habits", json={"name": "Old habit"}, headers=_auth_headers(token)
        ).json()["id"]
        archived = client.post(
            f"/habits/{habit_id}/archive", headers=_auth_headers(token)
        )
        assert archived.status_code == 200
        assert archived.json()["archived"] is True

        default_list = client.get("/habits", headers=_auth_headers(token))
        assert default_list.json() == []  # => archived habits are hidden by default

        full_list = client.get(
            "/habits?include_archived=true", headers=_auth_headers(token)
        )
        assert (
            len(full_list.json()) == 1
        )  # => but still there when explicitly requested

    def test_delete_then_get_returns_404(self, client: TestClient) -> None:
        token = _register_and_login(client)
        habit_id = client.post(
            "/habits", json={"name": "Temp"}, headers=_auth_headers(token)
        ).json()["id"]
        delete = client.delete(f"/habits/{habit_id}", headers=_auth_headers(token))
        assert delete.status_code == 204
        after = client.get(f"/habits/{habit_id}", headers=_auth_headers(token))
        assert after.status_code == 404


class TestSearchIsInjectionSafe:
    def test_classic_sql_injection_payload_returns_no_rows_and_no_leak(
        self, client: TestClient
    ) -> None:
        token = _register_and_login(client)
        client.post(
            "/habits", json={"name": "Read 20 minutes"}, headers=_auth_headers(token)
        )
        client.post(
            "/habits", json={"name": "Drink water"}, headers=_auth_headers(token)
        )

        legit = client.get("/habits?q=Read", headers=_auth_headers(token))
        assert (
            len(legit.json()) == 1
        )  # => a normal substring search matches exactly one habit

        attack = client.get("/habits?q=' OR 1=1 -- ", headers=_auth_headers(token))
        assert attack.status_code == 200
        assert (
            attack.json() == []
        )  # => the payload is DATA, matches no real habit name, leaks nothing
