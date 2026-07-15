# learning/code/ex-78-harden-the-full-app-transcript/attack_transcript.py
"""Example 78: 3 real attacks, run against the live app.py -- each flips from a real SUCCEEDED line to a real BLOCKED line (co-01, co-24, co-02)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the transcript-driving logic itself

import requests  # => co-01: real HTTP client -- every request below hits the live app.py process

BASE_URL = (
    "http://127.0.0.1:5078"  # => co-01: matches app.py's app.run(port=5078) exactly
)
TRANSCRIPT: list[
    str
] = []  # => co-02: the REAL, running before/after attack transcript this script builds


def record(
    line: str,
) -> None:  # => co-02: appends ONE real transcript line and prints it immediately
    TRANSCRIPT.append(line)  # => co-02: real, in-order transcript entry
    print(line)  # => co-02: real, live output as each attack actually runs


def attack_sql_injection(
    base_path: str,
) -> bool:  # => co-03: returns True if the injection REALLY bypassed the login
    payload = {
        "username": "nobody",
        "password": "' OR '1'='1",
    }  # => co-03: a REAL, classic SQLi login-bypass payload
    response = requests.post(
        f"{BASE_URL}/{base_path}/login", json=payload, timeout=5
    )  # => co-03: a real HTTP POST
    return (
        response.json()["logged_in"] is True
    )  # => co-03: real, computed outcome -- did the bypass really succeed


def attack_stored_xss(
    base_path: str,
) -> bool:  # => co-06: returns True if the raw <script> tag REALLY reached the response
    payload = {
        "text": "<script>alert(1)</script>"
    }  # => co-06: a REAL, minimal stored-XSS probe
    requests.post(
        f"{BASE_URL}/{base_path}/comment", json=payload, timeout=5
    )  # => co-06: a real HTTP POST -- stores it
    response = requests.get(
        f"{BASE_URL}/{base_path}/comments", timeout=5
    )  # => co-06: a real HTTP GET -- renders it back
    return (
        "<script>alert(1)</script>" in response.text
    )  # => co-06: real, literal check -- was it encoded or not


def attack_missing_auth(
    base_path: str,
) -> bool:  # => co-16: returns True if a NON-admin caller REALLY reached admin data
    headers = {
        "X-User-Id": "alice"
    }  # => co-16: alice's own real identity header -- role="user", never "admin"
    response = requests.get(
        f"{BASE_URL}/{base_path}/admin/stats", headers=headers, timeout=5
    )  # => co-16: a real GET
    return (
        response.status_code == 200
    )  # => co-16: real, computed outcome -- did the non-admin request really succeed


def main() -> (
    None
):  # => co-02: runs all 3 real attacks against BOTH the unhardened and hardened route sets
    record("=== BEFORE HARDENING (legacy/*) ===")  # => labels section
    sqli_before = attack_sql_injection(
        "legacy"
    )  # => co-03: a REAL attack run against the unhardened route
    record(
        f"[SQL injection]   payload=' OR '1'='1  -> {'SUCCEEDED (bypassed login)' if sqli_before else 'blocked'}"
    )
    xss_before = attack_stored_xss(
        "legacy"
    )  # => co-06: a REAL attack run against the unhardened route
    record(
        f"[Stored XSS]      payload=<script>alert(1)</script>  -> {'SUCCEEDED (raw tag reached response)' if xss_before else 'blocked'}"
    )
    authz_before = attack_missing_auth(
        "legacy"
    )  # => co-16: a REAL attack run against the unhardened route
    record(
        f"[Missing auth]    caller=alice (role=user)  -> {'SUCCEEDED (reached admin data)' if authz_before else 'blocked'}"
    )
    assert (
        sqli_before and xss_before and authz_before
    )  # => co-02: proves ALL THREE real attacks really succeeded, pre-fix

    record(
        "\n=== AFTER HARDENING (secure/*, the SAME 3 payloads) ==="
    )  # => labels section
    sqli_after = attack_sql_injection(
        "secure"
    )  # => co-03: the IDENTICAL attack, against the hardened route
    record(
        f"[SQL injection]   payload=' OR '1'='1  -> {'SUCCEEDED' if sqli_after else 'BLOCKED (parameterized query)'}"
    )
    xss_after = attack_stored_xss(
        "secure"
    )  # => co-06: the IDENTICAL attack, against the hardened route
    record(
        f"[Stored XSS]      payload=<script>alert(1)</script>  -> {'SUCCEEDED' if xss_after else 'BLOCKED (output encoded)'}"
    )
    authz_after = attack_missing_auth(
        "secure"
    )  # => co-16: the IDENTICAL attack, against the hardened route
    record(
        f"[Missing auth]    caller=alice (role=user)  -> {'SUCCEEDED' if authz_after else 'BLOCKED (require_admin)'}"
    )
    assert (
        not sqli_after and not xss_after and not authz_after
    )  # => co-02: proves ALL THREE real attacks now fail, post-fix

    print(
        "\n=== SUMMARY: every seeded attack flipped succeeded -> blocked ==="
    )  # => labels section
    for (
        attack_name,
        before,
        after,
    ) in [  # => co-02: a real, final table -- one row per real attack, before vs. after
        ("SQL injection", sqli_before, sqli_after),
        ("Stored XSS", xss_before, xss_after),
        ("Missing auth", authz_before, authz_after),
    ]:
        print(
            f"  {attack_name:16} before={'SUCCEEDED' if before else 'blocked':10} after={'SUCCEEDED' if after else 'BLOCKED'}"
        )
        assert (
            before is True and after is False
        )  # => co-02: proves EVERY real attack really flipped, none stayed open


if (
    __name__ == "__main__"
):  # => co-02: only runs when launched directly, e.g. `python3 attack_transcript.py`
    main()  # => co-02: runs all 3 real attacks against both route sets and prints the full real transcript
