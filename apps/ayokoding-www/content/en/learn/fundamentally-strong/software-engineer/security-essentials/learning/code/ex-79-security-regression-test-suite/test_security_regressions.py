# learning/code/ex-79-security-regression-test-suite/test_security_regressions.py
"""Example 79: real pytest tests -- red against implementations_vulnerable, green against implementations_fixed (co-02, co-23)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the test logic itself

import importlib  # => co-02: real, dynamic import -- selects vulnerable/fixed by env var, at COLLECTION time
import os  # => co-02: os.environ -- the REAL selector this suite's runner script sets before invoking pytest
import sqlite3  # => co-03: stdlib DB driver -- builds a REAL, fresh in-memory DB for every SQL-injection test run

import pytest  # => co-23: pytest 9.1.1 -- the REAL test runner this whole suite is written for

IMPL_NAME = os.environ.get(
    "EX79_IMPLEMENTATION", "fixed"
)  # => co-02: "vulnerable" or "fixed" -- set by run_suite.py
impl = importlib.import_module(
    f"implementations_{IMPL_NAME}"
)  # => co-02: the REAL module this run's tests exercise


@pytest.fixture()  # => co-03: a REAL, fresh in-memory DB for every single test that needs one
def users_db() -> (
    sqlite3.Connection
):  # => co-03: returns a REAL, seeded sqlite3.Connection
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-03: a real, isolated, in-memory DB per test -- no shared state
    conn.execute(
        "CREATE TABLE users (username TEXT, password TEXT)"
    )  # => co-03: real schema
    conn.execute(
        "INSERT INTO users VALUES ('alice', 'correct-horse')"
    )  # => co-03: one real seeded account
    conn.commit()  # => co-03: persists the seed before the test's real query runs
    return conn  # => co-03: a real, ready-to-query connection


def test_sql_injection_is_blocked(
    users_db: sqlite3.Connection,
) -> None:  # => co-03: encodes ex-03's exact vulnerability
    bypassed = impl.login(
        users_db, "nobody", "' OR '1'='1"
    )  # => co-03: the REAL, classic SQLi login-bypass payload
    assert (
        bypassed is False
    )  # => co-03: RED against vulnerable (bypass succeeds -> True), GREEN against fixed


def test_command_injection_is_blocked(
    tmp_path,
) -> None:  # => co-04: encodes ex-06's exact vulnerability
    marker = (
        tmp_path / "ex79-marker.txt"
    )  # => co-04: a REAL, per-test-run temp file -- pytest's own tmp_path fixture
    payload = f"hi; touch {marker}"  # => co-04: a REAL, classic shell-metacharacter injection payload
    impl.run_echo(
        payload
    )  # => co-04: the REAL call under test -- vulnerable os.system vs. fixed subprocess(shell=False)
    assert not marker.exists()  # => co-04: RED against vulnerable (the shell REALLY creates the file), GREEN against fixed


def test_xss_output_is_encoded() -> (
    None
):  # => co-06: encodes ex-08/ex-78's exact vulnerability
    rendered = impl.render_comment(
        "<script>alert(1)</script>"
    )  # => co-06: a REAL, minimal stored-XSS probe
    assert (
        "<script>" not in rendered
    )  # => co-06: RED against vulnerable (raw tag present), GREEN against fixed


def test_missing_authorization_is_blocked() -> (
    None
):  # => co-16: encodes ex-34/ex-78's exact vulnerability
    allowed = impl.is_authorized(
        "user"
    )  # => co-16: a REAL, non-admin role -- must NEVER be authorized
    assert (
        allowed is False
    )  # => co-16: RED against vulnerable (always True), GREEN against fixed
