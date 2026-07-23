"""Tests for Example 76: Health vs Readiness."""

import importlib
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


def test_health_never_depends_on_the_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TASKS_DB_PATH", str(tmp_path / "unreachable" / "tasks.db"))  # => the PARENT dir does not exist -- any DB access here would genuinely fail
    import app as app_module  # => re-import to pick up the fresh env var at module load time

    importlib.reload(app_module)
    client = TestClient(app_module.app)
    response = client.get("/health")  # => co-08: THIS example's focus -- liveness, unaffected by the DB
    assert response.status_code == 200  # => still 200 even though the "DB" is entirely unreachable
    assert response.json() == {"status": "ok"}


def test_readiness_fails_when_db_is_genuinely_unreachable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TASKS_DB_PATH", str(tmp_path / "unreachable" / "tasks.db"))
    import app as app_module

    importlib.reload(app_module)
    client = TestClient(app_module.app)
    response = client.get("/ready")  # => co-14: THIS example's focus -- a REAL sqlite3.connect() attempt
    assert response.status_code == 503  # => co-03: genuinely fails because the parent directory is missing
    assert response.json()["status"] == "not_ready"


def test_readiness_succeeds_when_db_is_reachable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TASKS_DB_PATH", str(tmp_path / "tasks.db"))  # => a genuinely writable, valid path
    import app as app_module

    importlib.reload(app_module)
    client = TestClient(app_module.app)
    response = client.get("/ready")
    assert response.status_code == 200  # => the contrast case -- a REAL, reachable database
    assert response.json() == {"status": "ready"}


os.environ.pop("TASKS_DB_PATH", None)  # => cleanup so later example runs in the same process start fresh
