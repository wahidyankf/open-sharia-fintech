"""Pass-1 capstone attack transcript -- runs the exact attacks this capstone's page documents
against a LIVE server and prints PASS/FAIL for each, using only the Python standard library
(`urllib`) so it never needs an extra runtime dependency beyond what already runs the app.

Run:
    ./setup.sh                    # in one terminal (boots the API on :8100), or
    uvicorn app.main:app --host 127.0.0.1 --port 8100   # with CAPSTONE1_AUTH_SECRET set
    python attack_transcript.py   # in another terminal
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "http://127.0.0.1:8100"


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

    # Register + log in TWO real users, exactly the way legitimate clients would.
    _request(
        "POST",
        "/auth/register",
        {"username": "attacker_demo", "password": "Sup3rSecret!"},
    )
    status, body = _request(
        "POST", "/auth/login", {"username": "attacker_demo", "password": "Sup3rSecret!"}
    )
    all_passed &= _check("login succeeds end-to-end", status == 200)
    attacker_token = json.loads(body)["access_token"]

    _request(
        "POST",
        "/auth/register",
        {"username": "victim_demo", "password": "Sup3rSecret!"},
    )
    status, body = _request(
        "POST", "/auth/login", {"username": "victim_demo", "password": "Sup3rSecret!"}
    )
    victim_token = json.loads(body)["access_token"]

    # Seed one public-looking habit for the attacker and one PRIVATE habit for the victim.
    _request("POST", "/habits", {"name": "Read 20 minutes"}, token=attacker_token)
    _request(
        "POST",
        "/habits",
        {"name": "victim's private therapy journal"},
        token=victim_token,
    )

    # Attack 1: SQL injection via /habits?q= -- must not leak the victim's habit.
    q = urllib.parse.quote("' OR 1=1 -- ")
    status, body = _request("GET", f"/habits?q={q}", token=attacker_token)
    all_passed &= _check(
        "SQL injection payload returns zero rows (no cross-user leak)",
        status == 200 and json.loads(body) == [],
    )

    # Attack 2: writing without a valid bearer token.
    status, _ = _request("POST", "/habits", {"name": "no auth"})
    all_passed &= _check("unauthenticated write is rejected (401)", status == 401)

    # Attack 3: reading without a valid bearer token -- EVERY /habits route is guarded here,
    # unlike the Security Essentials Task API this reuses the auth pattern from (co-12).
    status, _ = _request("GET", "/habits")
    all_passed &= _check("unauthenticated read is rejected (401)", status == 401)

    # Attack 4: registering a username carrying SQL metacharacters.
    status, _ = _request(
        "POST", "/auth/register", {"username": "admin'--", "password": "Sup3rSecret!"}
    )
    all_passed &= _check(
        "hostile username is rejected by the allow-list (422)", status == 422
    )

    # Attack 5: attacker tries to read the victim's habit by guessing its id.
    status, body = _request("GET", "/habits?include_archived=true", token=victim_token)
    victim_habit_id = json.loads(body)[0]["id"]
    status, _ = _request("GET", f"/habits/{victim_habit_id}", token=attacker_token)
    all_passed &= _check(
        "cross-user habit read is rejected (404, not leaked)", status == 404
    )

    print()
    print("ALL ATTACKS BLOCKED" if all_passed else "AT LEAST ONE ATTACK SUCCEEDED")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
