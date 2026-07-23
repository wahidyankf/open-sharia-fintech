# learning/code/ex-79-security-regression-test-suite/implementations_vulnerable.py
"""Example 79: the VULNERABLE version of 4 functions this suite's pytest tests exercise -- expected to FAIL here (co-02, co-23)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the seeded vulnerabilities themselves

import os  # => co-04: os.system -- the REAL command-injection sink this vulnerable module seeds
import sqlite3  # => co-03: stdlib DB driver -- the REAL SQL-injection sink this vulnerable module seeds


def login(
    conn: sqlite3.Connection, username: str, password: str
) -> bool:  # => co-03: VULNERABLE login check
    query = f"SELECT 1 FROM users WHERE username = '{username}' AND password = '{password}'"  # seeded bug: f-string SQL
    return (
        conn.execute(query).fetchone() is not None
    )  # => co-03: real, injectable query execution


def run_echo(host: str) -> None:  # => co-04: VULNERABLE command runner
    os.system(
        "echo " + host
    )  # seeded bug: os.system with concatenated untrusted input -- a REAL shell sink


def render_comment(text: str) -> str:  # => co-06: VULNERABLE renderer
    return (
        "<div>" + text + "</div>"
    )  # seeded bug: raw concatenation, NO output encoding at all


def is_authorized(role: str) -> bool:  # => co-16: VULNERABLE authorization check
    return True  # seeded bug: no real check at all -- every role is "authorized"
