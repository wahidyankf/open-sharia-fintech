"""Tests for Example 44: An Additive ALTER TABLE + Backfill Migration."""

import repository
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_pre_existing_row_reads_back_with_backfilled_priority() -> None:
    # => app.py already ran create_v1_schema() then migrate_add_priority_column()
    #    at import time -- this re-queries that SAME already-migrated row over HTTP
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Buy milk", "priority": 3}


def test_migration_mechanics_directly() -> None:
    # => co-15: insert a row under the OLD schema, migrate, then re-query --
    #    spelled out explicitly here, independent of the app's own startup sequence
    repository.create_v1_schema()  # => fresh v1 db: one row, no "priority" column yet
    assert "priority" not in repository.column_names()  # => column genuinely absent

    repository.migrate_add_priority_column()  # => run the additive migration + backfill
    assert "priority" in repository.column_names()  # => column now exists

    after = repository.get_task(1)  # => the SAME row, inserted before the column existed
    assert after is not None
    assert after["title"] == "Buy milk"  # => untouched by the migration
    assert after["priority"] == 3  # => backfilled, not left NULL
