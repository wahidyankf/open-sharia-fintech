# learning/code/ex-69-csrf-for-json-and-spa/app.py
"""Example 69: a live Flask app -- a real double-submit-cookie CSRF defense for a token-auth JSON/SPA API (co-26, co-20)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the double-submit logic itself

import secrets  # => co-26: cryptographically random session AND CSRF-cookie values -- both must be unguessable

from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)  # => co-26: make_response lets a route set cookies explicitly

app = Flask(
    __name__
)  # => co-26: one Flask app -- a real SPA-style JSON API, no HTML forms anywhere
SESSIONS: dict[
    str, str
] = {}  # => co-26: sid -> email -- real server-side session state, same shape as earlier examples


@app.route(
    "/login", methods=["POST"]
)  # => co-26: issues a real HttpOnly session cookie AND a real, JS-readable CSRF cookie
def login() -> (
    object
):  # => co-26: returns a Flask Response object with TWO real cookies
    sid = secrets.token_urlsafe(16)  # => co-26: a fresh, unpredictable session id
    csrf_value = secrets.token_urlsafe(
        16
    )  # => co-26: a SEPARATE random value -- the double-submit cookie's own secret
    SESSIONS[sid] = (
        "victim@example.com"  # => co-26: the victim's real starting state, keyed by the real session id
    )
    response = make_response(
        jsonify({"sid": sid, "csrf_token": csrf_value})
    )  # => co-26: an SPA reads BOTH from the body
    response.set_cookie(
        "sid", sid, httponly=True
    )  # => co-26: the AMBIENT cookie -- JS can never read this one
    response.set_cookie(
        "csrf_cookie", csrf_value, httponly=False
    )  # => co-26: JS on the SAME origin CAN read this one
    return response  # => co-26: an SPA now holds sid (ambient) and csrf_value (readable, must be echoed in a header)


@app.route(
    "/api/change-email", methods=["POST"]
)  # => co-26: the REAL, state-changing endpoint this defense protects
def change_email() -> (
    object
):  # => co-26: returns a Flask Response object -- the double-submit-cookie check lives here
    sid = request.cookies.get(
        "sid", ""
    )  # => co-26: the ambient cookie -- a browser attaches this cross-site too
    if (
        sid not in SESSIONS
    ):  # => co-26: the same existence check every earlier session example used
        return jsonify(
            {"error": "unauthorized"}
        ), 401  # => co-26: a real 401 for a genuinely unknown session
    csrf_cookie_value = request.cookies.get(
        "csrf_cookie", ""
    )  # => co-26: the ambient CSRF cookie -- also auto-resent
    csrf_header_value = request.headers.get(
        "X-CSRF-Token", ""
    )  # => co-26: a foreign origin's JS CANNOT set this header
    # => co-26: the REAL double-submit check -- the header value must match the COOKIE value.
    # => A cross-site attacker's browser resends the csrf_cookie automatically, but same-origin
    # => policy stops the attacker's own JS from ever READING that cookie's value to put it in a header
    if (
        not csrf_header_value or csrf_header_value != csrf_cookie_value
    ):  # => co-26: the fix -- header MUST equal cookie
        return jsonify(
            {"error": "csrf token mismatch"}
        ), 403  # => co-26: a real 403 -- the write never happens
    new_email = request.get_json(force=True).get(
        "email", ""
    )  # => co-01: attacker-controlled -- a foreign origin's payload
    SESSIONS[sid] = (
        new_email  # => co-26: only reached once the double-submit check has already passed
    )
    return jsonify(
        {"email": new_email}
    )  # => co-26: confirms the change -- only for a request that PROVED same-origin JS


if (
    __name__ == "__main__"
):  # => co-26: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5069
    )  # => co-26: localhost-only, fixed port -- exploit_and_fix.py targets this
