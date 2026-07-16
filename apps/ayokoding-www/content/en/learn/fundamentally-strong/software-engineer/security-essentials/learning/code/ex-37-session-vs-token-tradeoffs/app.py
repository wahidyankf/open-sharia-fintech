"""Example 37: a live Flask app -- both a server-side session login and a stateless JWT login (co-12, co-14)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the tradeoff being demonstrated

import datetime  # => co-14: real expiry timestamps for the JWT half of this example
import secrets  # => co-12: cryptographically random session ids -- must be unguessable

import jwt  # => co-14: PyJWT 2.13.0 pinned -- CVE-2026-32597 (crit header) fixed at >=2.12.0, unaffected here
from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)  # => co-12: make_response lets a route set cookies

app = Flask(
    __name__
)  # => co-12: one Flask app, hosting both the session-based and token-based login flows
SESSIONS: dict[
    str, str
] = {}  # => co-12: server-side session store -- sid -> username, killable in one line
JWT_SECRET = "ex37-hmac-secret-at-least-32-bytes!!"  # => co-14: real HMAC secret, RFC 7518-length-compliant


@app.route(
    "/session/login", methods=["POST"]
)  # => co-12: STATEFUL -- creates a real server-side session row
def session_login() -> (
    object
):  # => co-12: returns a Flask Response object with a real Set-Cookie header
    username = request.json.get("username", "")  # => co-12: the real submitted username
    sid = secrets.token_urlsafe(
        16
    )  # => co-12: a fresh, unpredictable session id for this login
    SESSIONS[sid] = (
        username  # => co-12: server-side state -- this row is what makes the session valid
    )
    response = make_response(
        jsonify({"sid": sid})
    )  # => co-12: echoes the sid so this example can show it
    response.set_cookie(
        "sid", sid
    )  # => co-12: the real cookie a browser would store and resend
    return (
        response  # => co-12: the client now holds a reference to REAL server-side state
    )


@app.route(
    "/session/protected"
)  # => co-12: only succeeds while the referenced server-side row still exists
def session_protected() -> (
    object
):  # => co-12: a real, read-only lookup against server-side state
    sid = request.cookies.get(
        "sid", ""
    )  # => co-12: whatever sid this specific request presents
    if (
        sid not in SESSIONS
    ):  # => co-12: the ENTIRE check is "does this row still exist" -- pure server-side state
        return jsonify(
            {"error": "unauthorized"}
        ), 401  # => co-12: a real 401 once the row is gone
    return jsonify(
        {"logged_in_as": SESSIONS[sid]}
    )  # => co-12: real, current lookup -- always up to date


@app.route(
    "/token/login", methods=["POST"]
)  # => co-14: STATELESS -- issues a real signed JWT, no server row at all
def token_login() -> (
    object
):  # => co-14: returns a Flask Response object -- a real, signed token
    username = request.json.get("username", "")  # => co-14: the real submitted username
    now = datetime.datetime.now(
        datetime.timezone.utc
    )  # => co-14: real wall-clock UTC time, taken once
    claims = {
        "user": username,
        "exp": now + datetime.timedelta(minutes=5),
    }  # => co-14: self-contained, no DB lookup
    token = jwt.encode(
        claims, JWT_SECRET, algorithm="HS256"
    )  # => co-14: a real, correctly-signed HS256 token
    return jsonify(
        {"token": token}
    )  # => co-14: the client now holds ALL the state -- nothing stored server-side


@app.route(
    "/token/protected"
)  # => co-14: succeeds purely by verifying the SIGNATURE -- no server-side row to check
def token_protected() -> (
    object
):  # => co-14: a real, stateless signature check -- no server-side row
    auth_header = request.headers.get(
        "Authorization", ""
    )  # => co-14: the real bearer token header, if present
    token = auth_header.removeprefix(
        "Bearer "
    )  # => co-14: strips the real "Bearer " scheme prefix
    try:  # => co-14: a signature/expiry failure is the ONLY way this can reject a token
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=["HS256"]
        )  # => co-14: real verification, no DB involved
    except jwt.PyJWTError:  # => co-14: catches any real PyJWT verification failure (bad sig, expired, malformed)
        return (
            jsonify({"error": "unauthorized"}),
            401,
        )  # => co-14: a real 401 -- but this token is STILL cryptographically valid
    return jsonify(
        {"logged_in_as": payload["user"]}
    )  # => co-14: real, decoded claims -- trusted purely by signature


@app.route(
    "/admin/revoke-all-sessions", methods=["POST"]
)  # => co-12: simulates "killing the server-side session store"
def revoke_all_sessions() -> (
    object
):  # => co-12: simulates an operator killing the session store
    count = len(
        SESSIONS
    )  # => co-12: the real number of live sessions about to be destroyed
    SESSIONS.clear()  # => co-12: the REAL revocation -- every session row is gone in one call
    return jsonify(
        {"revoked": count}
    )  # => co-12: real count -- proves this actually mutated server-side state


if (
    __name__ == "__main__"
):  # => co-12: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5037
    )  # => co-12: localhost-only, fixed port -- exploit_and_fix.py targets this
