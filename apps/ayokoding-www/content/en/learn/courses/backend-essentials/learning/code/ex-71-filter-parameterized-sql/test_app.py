"""Tests for Example 71: Filter Parameterized SQL."""

from fastapi.testclient import TestClient

from app import app, list_tasks_safe, list_tasks_unsafe_for_demo_only

client = TestClient(app)

INJECTION_ATTEMPT = "done' OR '1'='1"  # => a classic tautology-injection payload


def test_route_neutralizes_the_injection_attempt() -> None:
    response = client.get("/tasks", params={"status": INJECTION_ATTEMPT})  # => co-20: this example's focus
    assert response.status_code == 200  # => no SQL error -- the value is treated as ONE opaque string
    assert response.json() == []  # => co-14: no row's status literally equals that whole string -- SAFE


def test_safe_repository_function_matches_route_behavior() -> None:
    assert list_tasks_safe(INJECTION_ATTEMPT) == []  # => the parameterized function, called directly, agrees


def test_unsafe_function_demonstrates_the_vulnerability_it_would_have_had() -> None:
    result = list_tasks_unsafe_for_demo_only(INJECTION_ATTEMPT)  # => co-14: the DELIBERATELY vulnerable twin -- never reachable from any route
    assert len(result) == 25  # => the tautology "OR '1'='1'" genuinely returns EVERY row -- the exact bug
    # => parameterization exists specifically to prevent


def test_safe_status_lookup_still_works_normally() -> None:
    assert len(list_tasks_safe("done")) == 8  # => an ordinary, legitimate value still filters correctly
