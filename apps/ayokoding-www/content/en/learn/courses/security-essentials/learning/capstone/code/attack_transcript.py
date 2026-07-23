"""Capstone attack transcript -- runs the exact attacks this capstone's page documents
against a LIVE server and prints PASS/FAIL for each. Every attack below is proven to have
SUCCEEDED against the naive first draft of this app (see the page's Step 1 / Step 3
"before" transcripts, captured from that draft before it was hardened); run against the
SHIPPED app below, every one of them is expected to FAIL.

Run:
    uvicorn app.main:app --host 127.0.0.1 --port 8000   # in one terminal, with
                                                          # CAPSTONE_AUTH_SECRET set
    python attack_transcript.py                          # in another terminal
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8000"


def _request(
    method: str,
    path: str,
    body: dict[str, object] | None = None,
    token: str | None = None,
) -> tuple[int, str]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Content-Type": "application/json"}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        BASE_URL + path, data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(request) as response:  # noqa: S310 -- 127.0.0.1 only, local demo
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


def _check(label: str, condition: bool) -> bool:
    print(f"[{'PASS' if condition else 'FAIL'}] {label}")
    return condition


def main() -> int:
    all_passed = True

    # Register + log in a real user, exactly the way a legitimate client would.
    _request(
        "POST",
        "/auth/register",
        {"username": "attacker_demo", "password": "Sup3rSecret!"},
    )
    status, body = _request(
        "POST", "/auth/login", {"username": "attacker_demo", "password": "Sup3rSecret!"}
    )
    all_passed &= _check("login succeeds end-to-end", status == 200)
    token = json.loads(body)["access_token"]

    # Seed one public task and one "secret-looking" task the attack should NOT be able to reach.
    _request("POST", "/tasks", {"title": "write the report"}, token=token)
    _request("POST", "/tasks", {"title": "rotate prod db credentials"}, token=token)

    # Attack 1: SQL injection via /tasks/search -- co-03. Against the naive f-string draft,
    # this payload matched every row (see the page's Step 1 "before" transcript). Against the
    # shipped, parameterized version, it must match nothing.
    status, body = _request("GET", "/tasks/search?q=%27%20OR%20%271%27%3D%271")
    all_passed &= _check(
        "SQL injection payload returns zero rows",
        status == 200 and json.loads(body) == [],
    )

    # Attack 2: stored XSS via /tasks/{id}/view -- co-06. Against the naive f-string draft,
    # this rendered a literal, executable <script> tag (see the page's Step 3 "before"
    # transcript). Against the shipped, autoescaped template, it must render as inert text.
    status, body = _request(
        "POST", "/tasks", {"title": "<script>alert(1)</script>"}, token=token
    )
    xss_task_id = json.loads(body)["id"]
    status, body = _request("GET", f"/tasks/{xss_task_id}/view")
    all_passed &= _check(
        "XSS payload is rendered escaped, not executable",
        "<script>" not in body and "&lt;script&gt;" in body,
    )

    # Attack 3: writing without a valid bearer token -- co-12.
    status, _ = _request("POST", "/tasks", {"title": "no auth"})
    all_passed &= _check("unauthenticated write is rejected (401)", status == 401)

    # Attack 4: registering a username carrying SQL metacharacters -- co-07.
    status, _ = _request(
        "POST", "/auth/register", {"username": "admin'--", "password": "Sup3rSecret!"}
    )
    all_passed &= _check(
        "hostile username is rejected by the allow-list (422)", status == 422
    )

    print()
    print("ALL ATTACKS BLOCKED" if all_passed else "AT LEAST ONE ATTACK SUCCEEDED")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
