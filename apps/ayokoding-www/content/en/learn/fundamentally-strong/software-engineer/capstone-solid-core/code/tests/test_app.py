"""capstone-solid-core: integration test -- exercises the REAL FastAPI app through Starlette's
`TestClient` (topic 15's top of the pyramid): HTTP request in, HTTP response out, a REAL SQLite
file underneath, auth + validation + persistence + the Step-2 SOLID refactor + the Step-3
denormalized recent-activity query all wired together as they would be in production.

This suite is BEHAVIOR-PRESERVATION evidence for Step 2 (every test that also existed, in
spirit, against the Pass-1 baseline still passes against the refactored code) PLUS new coverage
for what Step 3 added (`/habits/activity/recent`).
"""

import base64
import hashlib
import hmac
import importlib
import json
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_TEST_AUTH_SECRET = "test-only-secret-never-committed"
_UNAUTHORIZED_BODY = {
    "error": {"code": "unauthorized", "message": "missing or invalid token"}
}


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    db_path = tmp_path / "habits.db"
    monkeypatch.setenv("CAPSTONE_SOLID_CORE_DB_PATH", str(db_path))
    monkeypatch.setenv("CAPSTONE_SOLID_CORE_AUTH_SECRET", _TEST_AUTH_SECRET)
    from app import main as main_module  # => imported AFTER the env vars above are set

    importlib.reload(main_module)
    return TestClient(main_module.app)


def _sign(payload_b64: str, secret: str) -> str:
    digest = hmac.new(
        secret.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256
    )
    return digest.hexdigest()


def _expired_token(secret: str = _TEST_AUTH_SECRET) -> str:
    payload_b64 = base64.urlsafe_b64encode(
        json.dumps({"sub": 1, "exp": 0}).encode("utf-8")
    ).decode("ascii")
    return f"{payload_b64}.{_sign(payload_b64, secret)}"


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

    def test_registering_an_existing_username_returns_409_conflict(
        self, client: TestClient
    ) -> None:
        client.post(
            "/auth/register", json={"username": "frank", "password": "Sup3rSecret!"}
        )
        conflict = client.post(
            "/auth/register", json={"username": "frank", "password": "Different1!"}
        )
        assert conflict.status_code == 409

    def test_stored_password_is_never_plaintext(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        _register_and_login(client, "bob", "AnotherSecret1!")
        conn = sqlite3.connect(tmp_path / "habits.db")
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?", ("bob",)
        ).fetchone()
        stored_hash = str(row["password_hash"])
        assert stored_hash.startswith("$argon2id$")
        assert "AnotherSecret1!" not in stored_hash

    def test_hostile_username_is_rejected_by_the_allow_list(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/auth/register", json={"username": "admin'--", "password": "Sup3rSecret!"}
        )
        assert response.status_code == 422

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
        assert wrong.json() == unknown.json()


class TestHabitsRequireAuth:
    def test_unauthenticated_read_is_rejected(self, client: TestClient) -> None:
        assert client.get("/habits").status_code == 401

    def test_unauthenticated_create_is_rejected(self, client: TestClient) -> None:
        assert (
            client.post("/habits", json={"name": "Read 20 minutes"}).status_code == 401
        )


class TestTokenValidation:
    def test_token_with_no_dot_separator_is_rejected(self, client: TestClient) -> None:
        response = client.get("/habits", headers=_auth_headers("garbage"))
        assert response.status_code == 401
        assert response.json() == _UNAUTHORIZED_BODY

    def test_token_with_a_tampered_signature_is_rejected(
        self, client: TestClient
    ) -> None:
        token = _register_and_login(client)
        payload_b64, signature = token.rsplit(".", 1)
        flipped_last_char = "0" if signature[-1] != "0" else "1"
        tampered_token = f"{payload_b64}.{signature[:-1]}{flipped_last_char}"
        response = client.get("/habits", headers=_auth_headers(tampered_token))
        assert response.status_code == 401
        assert response.json() == _UNAUTHORIZED_BODY

    def test_token_whose_payload_is_not_valid_json_is_rejected(
        self, client: TestClient
    ) -> None:
        payload_b64 = base64.urlsafe_b64encode(b"not-json-at-all").decode("ascii")
        signature = _sign(payload_b64, _TEST_AUTH_SECRET)
        response = client.get(
            "/habits", headers=_auth_headers(f"{payload_b64}.{signature}")
        )
        assert response.status_code == 401
        assert response.json() == _UNAUTHORIZED_BODY

    def test_expired_token_is_rejected(self, client: TestClient) -> None:
        response = client.get("/habits", headers=_auth_headers(_expired_token()))
        assert response.status_code == 401
        assert response.json() == _UNAUTHORIZED_BODY


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
        assert second.json()["checkin_count"] == 1

    def test_one_user_cannot_read_another_users_habit(self, client: TestClient) -> None:
        token_a = _register_and_login(client, "dave", "Sup3rSecret!")
        token_b = _register_and_login(client, "erin", "Sup3rSecret!")
        habit_id = client.post(
            "/habits", json={"name": "Dave's habit"}, headers=_auth_headers(token_a)
        ).json()["id"]
        cross_user = client.get(f"/habits/{habit_id}", headers=_auth_headers(token_b))
        assert cross_user.status_code == 404

    def test_archive_hides_a_habit_from_the_default_list(
        self, client: TestClient
    ) -> None:
        token = _register_and_login(client)
        habit_id = client.post(
            "/habits", json={"name": "Old habit"}, headers=_auth_headers(token)
        ).json()["id"]
        client.post(f"/habits/{habit_id}/archive", headers=_auth_headers(token))
        assert client.get("/habits", headers=_auth_headers(token)).json() == []
        full = client.get("/habits?include_archived=true", headers=_auth_headers(token))
        assert len(full.json()) == 1

    def test_delete_then_get_returns_404(self, client: TestClient) -> None:
        token = _register_and_login(client)
        habit_id = client.post(
            "/habits", json={"name": "Temp"}, headers=_auth_headers(token)
        ).json()["id"]
        assert (
            client.delete(
                f"/habits/{habit_id}", headers=_auth_headers(token)
            ).status_code
            == 204
        )
        assert (
            client.get(f"/habits/{habit_id}", headers=_auth_headers(token)).status_code
            == 404
        )


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
        assert len(legit.json()) == 1

        attack = client.get("/habits?q=' OR 1=1 -- ", headers=_auth_headers(token))
        assert attack.status_code == 200
        assert attack.json() == []


class TestRecentActivity:
    """Step 3's new endpoint (topic 26 EXPLAIN-guided denormalized index)."""

    def test_recent_activity_spans_every_habit_newest_first(
        self, client: TestClient
    ) -> None:
        token = _register_and_login(client)
        reading_id = client.post(
            "/habits", json={"name": "Read 20 minutes"}, headers=_auth_headers(token)
        ).json()["id"]
        water_id = client.post(
            "/habits", json={"name": "Drink water"}, headers=_auth_headers(token)
        ).json()["id"]
        client.post(
            f"/habits/{reading_id}/checkins",
            json={"checkin_date": "2026-07-01"},
            headers=_auth_headers(token),
        )
        client.post(
            f"/habits/{water_id}/checkins",
            json={"checkin_date": "2026-07-16"},
            headers=_auth_headers(token),
        )
        activity = client.get(
            "/habits/activity/recent?limit=10", headers=_auth_headers(token)
        )
        assert activity.status_code == 200
        dates = [entry["checkin_date"] for entry in activity.json()]
        assert dates == [
            "2026-07-16",
            "2026-07-01",
        ]  # => newest first, across BOTH habits

    def test_recent_activity_is_scoped_to_the_caller(self, client: TestClient) -> None:
        token_a = _register_and_login(client, "dave", "Sup3rSecret!")
        token_b = _register_and_login(client, "erin", "Sup3rSecret!")
        habit_id = client.post(
            "/habits", json={"name": "Dave's habit"}, headers=_auth_headers(token_a)
        ).json()["id"]
        client.post(
            f"/habits/{habit_id}/checkins", json={}, headers=_auth_headers(token_a)
        )
        activity_b = client.get(
            "/habits/activity/recent", headers=_auth_headers(token_b)
        )
        assert activity_b.json() == []  # => erin sees NONE of dave's activity

    def test_recent_activity_requires_auth(self, client: TestClient) -> None:
        assert client.get("/habits/activity/recent").status_code == 401


class TestDigestSequentialAndConcurrentAgree:
    """Step 3's concurrency change (topic 24): `sequential_digest` and `concurrent_digest`
    (app/digest.py) must return the IDENTICAL set of results for the identical database --
    concurrency changed WHERE the work runs, never WHAT it computes."""

    def test_sequential_and_concurrent_digest_return_identical_results(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        token = _register_and_login(client)
        habit_ids = []
        today = date(2026, 7, 16)
        for i in range(4):
            habit_id = client.post(
                "/habits", json={"name": f"Habit {i}"}, headers=_auth_headers(token)
            ).json()["id"]
            habit_ids.append(habit_id)
            for offset in range(5):
                client.post(
                    f"/habits/{habit_id}/checkins",
                    json={"checkin_date": (today - timedelta(days=offset)).isoformat()},
                    headers=_auth_headers(token),
                )

        from app.digest import concurrent_digest, sequential_digest

        db_path = str(tmp_path / "habits.db")
        sequential_result = sequential_digest(
            db_path, user_id=1, habit_ids=habit_ids, today=today
        )
        # => a REAL ProcessPoolExecutor, spawning real OS worker processes -- not mocked.
        # => The larger-scale, TIMED before/after comparison lives in
        # => bench/benchmark_concurrency.py; this test only proves correctness (same rows).
        concurrent_result = concurrent_digest(
            db_path, user_id=1, habit_ids=habit_ids, today=today, max_workers=2
        )
        assert len(sequential_result) == 4
        assert all(d.current_streak == 5 for d in sequential_result)
        assert sorted(sequential_result, key=lambda d: d.habit_id) == sorted(
            concurrent_result, key=lambda d: d.habit_id
        )
