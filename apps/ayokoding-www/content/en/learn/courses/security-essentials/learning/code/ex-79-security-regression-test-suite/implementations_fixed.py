# learning/code/ex-79-security-regression-test-suite/implementations_fixed.py
"""Example 79: the FIXED version of the SAME 4 functions -- the SAME pytest tests must now PASS against these (co-02, co-23)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the fixes themselves

import sqlite3  # => co-03: the SAME stdlib DB driver -- only the query construction changes
import subprocess  # => co-04: real subprocess -- replaces os.system, argv list instead of a shell string

from markupsafe import (
    escape,
)  # => co-06: MarkupSafe 3.0.3 (bundled with Flask 3.1.3) -- the real output-encoding fix


def login(
    conn: sqlite3.Connection, username: str, password: str
) -> bool:  # => co-03: FIXED login check
    row = conn.execute(  # => co-03: a REAL, parameterized query -- username/password sent as DATA, never SQL text
        "SELECT 1 FROM users WHERE username = ? AND password = ?", (username, password)
    ).fetchone()
    return row is not None  # => co-03: real, injection-safe result


def run_echo(host: str) -> None:  # => co-04: FIXED command runner
    subprocess.run(
        ["echo", host], shell=False
    )  # => co-04: real argv list -- host is ONE literal argument, never shell text


def render_comment(text: str) -> str:  # => co-06: FIXED renderer
    return (
        "<div>" + str(escape(text)) + "</div>"
    )  # => co-06: real output encoding -- neutralizes any markup in `text`


def is_authorized(role: str) -> bool:  # => co-16: FIXED authorization check
    return (
        role == "admin"
    )  # => co-16: a REAL, explicit role check -- only "admin" is ever authorized
