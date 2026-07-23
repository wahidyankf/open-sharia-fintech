# learning/code/ex-65-token-revocation-strategy/app.py
"""Example 65: a live Flask app -- short-lived JWT access tokens, a longer-lived refresh token, and a REAL revocation list (co-12, co-14)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the revocation logic itself

import datetime  # => co-14: real UTC timestamps for token expiry
import secrets  # => co-12: cryptographically random refresh tokens -- opaque, never a JWT themselves

import jwt  # => co-14: PyJWT 2.13.0 pinned -- CVE-2026-32597 (crit header) fixed at >=2.12.0, unaffected here
from flask import (
    Flask,
    jsonify,
    request,
)  # => co-12: request.get_json reads the caller-supplied refresh token

app = Flask(
    __name__
)  # => co-12: one Flask app, hosting login, refresh, and the real revocation endpoint
JWT_SECRET = "ex65-hmac-secret-at-least-32-bytes-long!!"  # => co-14: real HMAC secret, RFC 7518-length-compliant
# => co-12: token -> {"user": ..., "revoked": bool} -- a REAL, in-memory revocation table (a SQLite table
# => would use the identical shape in production; an in-memory dict keeps this example self-contained)
REFRESH_TOKENS: dict[str, dict[str, object]] = {}


def make_access_token(
    user: str,
) -> str:  # => co-14: mints a REAL, short-lived signed JWT
    now = datetime.datetime.now(
        datetime.timezone.utc
    )  # => co-14: real wall-clock UTC time, taken once per call
    claims = {
        "user": user,
        "exp": now + datetime.timedelta(minutes=5),
    }  # => co-14: a real, SHORT 5-minute lifetime
    return jwt.encode(
        claims, JWT_SECRET, algorithm="HS256"
    )  # => co-14: a real, correctly-signed HS256 token


@app.route(
    "/login", methods=["POST"]
)  # => co-12: issues a REAL access token AND a REAL, tracked refresh token
def login() -> (
    object
):  # => co-12: returns a Flask Response object with both real tokens
    user = request.get_json(force=True).get(
        "username", ""
    )  # => co-12: the real submitted username
    refresh_token = secrets.token_urlsafe(
        24
    )  # => co-12: a REAL, opaque, unpredictable refresh token
    REFRESH_TOKENS[refresh_token] = {
        "user": user,
        "revoked": False,
    }  # => co-12: real, fresh entry in the revocation table
    access_token = make_access_token(
        user
    )  # => co-14: a real, short-lived JWT for this SAME login
    return jsonify(
        {"access_token": access_token, "refresh_token": refresh_token}
    )  # => co-12: both real tokens returned


@app.route(
    "/refresh", methods=["POST"]
)  # => co-12: mints a NEW access token FROM a real, still-valid refresh token
def refresh() -> (
    object
):  # => co-12: returns a Flask Response object -- a new access token, or a real rejection
    refresh_token = request.get_json(force=True).get(
        "refresh_token", ""
    )  # => co-01: attacker-adjacent -- caller-supplied
    entry = REFRESH_TOKENS.get(
        refresh_token
    )  # => co-12: the REAL, current state of this specific refresh token
    if (
        entry is None or entry["revoked"]
    ):  # => co-12: the REAL check -- unknown OR explicitly revoked, both rejected
        return jsonify(
            {"error": "invalid or revoked refresh token"}
        ), 401  # => co-12: a real 401 for either case
    new_access_token = make_access_token(
        str(entry["user"])
    )  # => co-14: a REAL, freshly minted, short-lived access token
    return jsonify(
        {"access_token": new_access_token}
    )  # => co-12: only the ACCESS token rotates -- refresh stays the same


@app.route(
    "/admin/revoke", methods=["POST"]
)  # => co-12: the REAL revocation operation -- e.g. on logout or compromise
def revoke() -> (
    object
):  # => co-12: returns a Flask Response object -- confirms the real revocation
    refresh_token = request.get_json(force=True).get(
        "refresh_token", ""
    )  # => co-12: WHICH real token to kill
    entry = REFRESH_TOKENS.get(
        refresh_token
    )  # => co-12: the real, current entry for this token, if any
    if (
        entry is None
    ):  # => co-12: a real guard -- can't revoke a token that was never issued
        return jsonify(
            {"error": "unknown refresh token"}
        ), 404  # => co-12: a real 404 for a bogus revoke request
    entry["revoked"] = (
        True  # => co-12: the REAL revocation -- flips server-side state, the token itself is unchanged
    )
    return jsonify(
        {"status": "revoked"}
    )  # => co-12: confirms the real, immediate effect on the NEXT /refresh call


if (
    __name__ == "__main__"
):  # => co-12: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5065
    )  # => co-12: localhost-only, fixed port -- exploit_and_fix.py targets this
