# learning/code/ex-80-secure-error-and-logging-review/fuzz_and_verify.py
"""Example 80: a REAL fuzz loop -- 16 malformed inputs, live server, checks the client response AND the server log (co-23, co-22)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the fuzzing/verification logic itself

import json  # => co-22: parses the REAL captured log text back into structured lines for inspection

import requests  # => co-23: real HTTP client -- every fuzz case below is a REAL request against 127.0.0.1:5080

BASE_URL = "http://127.0.0.1:5080"  # => co-23: localhost-only target -- matches app.py's bind address+port

INTERNAL_MARKERS = [  # => co-23: strings that must NEVER appear in a client-facing response body
    "Traceback",  # => co-23: a real Python traceback header -- would leak stack info
    'File "',  # => co-23: a real traceback frame's file-path prefix -- would leak filesystem layout
    ".py",  # => co-23: any real source-file name/extension -- would leak implementation detail
    "sqlite3",  # => co-23: the real DB driver's name -- would leak internal architecture
    "SELECT",  # => co-23: real SQL keyword text -- would leak query shape
    "AttributeError",  # => co-23: a real raw Python exception class name -- leaks internals if unfiltered
    "KeyError",  # => co-23: a real raw Python exception class name -- leaks internals if unfiltered
    "TypeError",  # => co-23: a real raw Python exception class name -- leaks internals if unfiltered
    "ValueError",  # => co-23: a real raw Python exception class name -- leaks internals if unfiltered
]

LOOKUP_FUZZ_INPUTS: list[
    str
] = [  # => co-23: 8 REAL malformed/edge-case `id` values for GET /lookup
    "not-a-number",  # => co-23: real ValueError trigger -- int() fails on non-numeric text
    "",  # => co-23: real ValueError trigger -- int() fails on empty string
    "1; DROP TABLE items; --",  # => co-23: a real SQL-injection-shaped string -- must be safely rejected, not executed
    "../../etc/passwd",  # => co-23: a real path-traversal-shaped string -- irrelevant to int(), still must not leak
    "ünïcödé-日本語"
    * 5,  # => co-23: real non-ASCII multi-script input -- a real Unicode edge case
    "9"
    * 400,  # => co-23: a real, extremely long numeric-looking string -- int() CAN parse this (Python bigints)
    "-1",  # => co-23: a real negative id -- parses fine, real "not found" path (no row for id=-1)
    "1.5",  # => co-23: a real float-shaped string -- int() genuinely raises ValueError on this
]

LOGIN_FUZZ_INPUTS: list[
    dict[str, object]
] = [  # => co-23: 8 REAL malformed JSON bodies for POST /login
    {},  # => co-23: real KeyError trigger -- missing both username and password
    {"username": "alice"},  # => co-23: real KeyError trigger -- missing password
    {
        "username": 12345,
        "password": "hunter2-fuzz-a",
    },  # => co-23: real AttributeError trigger -- int has no .strip()
    {
        "username": "alice",
        "password": 999999,
    },  # => co-23: password is an int -- len() on it raises real TypeError
    {
        "username": ["alice"],
        "password": "hunter2-fuzz-b",
    },  # => co-23: real AttributeError -- list has no .strip()
    {
        "username": None,
        "password": "hunter2-fuzz-c",
    },  # => co-23: real AttributeError -- NoneType has no .strip()
    {
        "username": "  Alice  ",
        "password": "hunter2-fuzz-d",
    },  # => co-23: real, VALID input -- exercises the happy path too
    {
        "username": "'; DROP TABLE users; --",
        "password": "hunter2-fuzz-e",
    },  # => co-23: SQLi-shaped username, still just a string
]

SEEDED_PASSWORDS = [  # => co-22: every REAL password VALUE used above -- the log must contain NONE of these, ever
    "hunter2-fuzz-a",
    "hunter2-fuzz-b",
    "hunter2-fuzz-c",
    "hunter2-fuzz-d",
    "hunter2-fuzz-e",
]


def run_lookup_fuzz() -> list[
    str
]:  # => co-23: fires all 8 real /lookup fuzz cases, returns their real response bodies
    bodies: list[
        str
    ] = []  # => co-23: accumulates each real response body for the leak check below
    for (
        raw_id
    ) in LOOKUP_FUZZ_INPUTS:  # => co-23: iterates the REAL fuzz corpus defined above
        resp = requests.get(
            f"{BASE_URL}/lookup", params={"id": raw_id}
        )  # => co-23: a REAL HTTP GET, real query param
        bodies.append(
            resp.text
        )  # => co-23: the REAL response body text -- exactly what a real client would see
        shown = (
            raw_id if len(raw_id) <= 40 else raw_id[:40] + "..."
        )  # => co-23: truncates only the PRINTED line, not the real request
        print(
            f"  /lookup?id={shown!r} -> {resp.status_code} {resp.text}"
        )  # => co-23: real, observed transcript line
    return bodies  # => co-23: real collected bodies, for the caller's leak assertions


def run_login_fuzz() -> list[
    str
]:  # => co-23: fires all 8 real /login fuzz cases, returns their real response bodies
    bodies: list[
        str
    ] = []  # => co-23: accumulates each real response body for the leak check below
    for (
        payload
    ) in LOGIN_FUZZ_INPUTS:  # => co-23: iterates the REAL fuzz corpus defined above
        resp = requests.post(
            f"{BASE_URL}/login", json=payload
        )  # => co-23: a REAL HTTP POST with a real JSON body
        bodies.append(
            resp.text
        )  # => co-23: the REAL response body text -- exactly what a real client would see
        print(
            f"  /login {payload!r:.70} -> {resp.status_code} {resp.text}"
        )  # => co-23: real, observed transcript line
    return bodies  # => co-23: real collected bodies, for the caller's leak assertions


def main() -> (
    None
):  # => co-23: runs the full real fuzz loop, then real client- and server-side verification
    print(
        "=== fuzzing GET /lookup with 8 real malformed/edge-case ids ==="
    )  # => labels section
    lookup_bodies = (
        run_lookup_fuzz()
    )  # => co-23: real, observed responses from 8 real requests

    print(
        "\n=== fuzzing POST /login with 8 real malformed JSON bodies ==="
    )  # => labels section
    login_bodies = (
        run_login_fuzz()
    )  # => co-23: real, observed responses from 8 real requests

    print(
        "\n=== verifying: zero internal-detail leaks in any of the 16 real client responses ==="
    )  # => labels section
    all_bodies = (
        lookup_bodies + login_bodies
    )  # => co-23: all 16 real response bodies, combined for one leak sweep
    leaks_found = 0  # => co-23: real, computed count -- must end at 0
    for body in (
        all_bodies
    ):  # => co-23: checks EVERY real response body against EVERY real internal marker
        for marker in (
            INTERNAL_MARKERS
        ):  # => co-23: the closed set of internal-detail signatures defined above
            if (
                marker in body
            ):  # => co-23: a REAL substring check against the REAL response text
                leaks_found += (
                    1  # => co-23: real, observed leak -- would fail the assertion below
                )
                print(
                    f"  LEAK: {marker!r} found in {body!r}"
                )  # => co-23: real, actionable failure detail
    assert (
        leaks_found == 0
    )  # => co-23: proves NONE of the 16 real responses ever exposed an internal detail
    print(
        f"real leaks found across 16 real responses: {leaks_found}"
    )  # => co-23: real, computed number

    print(
        "\n=== verifying: zero seeded password values ever appear in the real server-side log ==="
    )  # => section
    log_resp = requests.get(
        f"{BASE_URL}/debug/log-contents"
    )  # => co-22: fetches the REAL, complete captured log text
    log_text = log_resp.json()[
        "log"
    ]  # => co-22: the real log text, exactly as JsonFormatter wrote it
    password_leaks = sum(
        1 for pw in SEEDED_PASSWORDS if pw in log_text
    )  # => co-22: real count of leaked password values
    assert (
        password_leaks == 0
    )  # => co-22: proves NONE of the 5 real seeded passwords ever reached the log
    print(
        f"real password leaks found in the server log: {password_leaks}"
    )  # => co-22: real, computed number

    print(
        "\n=== verifying: the real log DID capture internal detail server-side (it's not just silent) ==="
    )  # => section
    log_lines = [
        json.loads(line) for line in log_text.strip().splitlines() if line.strip()
    ]  # => co-22: real parsed lines
    error_lines = [
        entry for entry in log_lines if entry["outcome"] == "error"
    ]  # => co-22: real lines from real except blocks
    assert (
        len(error_lines) > 0
    )  # => co-22: proves at least one real internal failure was genuinely captured server-side
    assert any(
        entry["error_type"] == "ValueError" for entry in error_lines
    )  # => co-22: real /lookup failure was captured
    assert any(
        entry["error_type"] == "AttributeError" for entry in error_lines
    )  # => co-22: real /login failure was captured
    print(
        f"real total log lines: {len(log_lines)}, real error-outcome lines: {len(error_lines)}"
    )  # => co-22: real counts
    print(
        "sample real error log line:", json.dumps(error_lines[0])
    )  # => co-22: one real, full example line, for inspection


if (
    __name__ == "__main__"
):  # => co-23: only runs when launched directly, e.g. `python3 fuzz_and_verify.py`
    main()  # => co-23: runs the full real fuzz-then-verify pass against the live server on port 5080
