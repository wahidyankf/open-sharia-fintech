"""Tests for Example 46: Layering -- No SQL in the Handler."""

from pathlib import Path

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

SQL_KEYWORDS = ("SELECT", "INSERT", "UPDATE", "DELETE", "ALTER", "CREATE TABLE")


def test_app_module_contains_no_sql_keywords() -> None:
    # => co-24: a literal, mechanical check that the LAYERING boundary holds --
    #    app.py's own source text never mentions a SQL verb
    source = Path(__file__).parent.joinpath("app.py").read_text().upper()
    for keyword in SQL_KEYWORDS:
        assert keyword not in source, f"found {keyword!r} in app.py -- SQL leaked into the handler"


def test_list_tasks_still_works_through_the_layered_repository() -> None:
    response = client.get("/tasks")  # => the layering is invisible to the CALLER
    assert response.status_code == 200
    assert len(response.json()) == 2
