"""Example 42: a live Flask app setting a session cookie with SameSite=Strict (co-26, co-13)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the SameSite flag itself

import secrets  # => co-13: cryptographically random session id -- must be unguessable

from flask import (
    Flask,
    jsonify,
    make_response,
)  # => co-13: make_response lets a route set cookies explicitly

app = Flask(
    __name__
)  # => co-13: one Flask app, serving the SameSite-protected login route


@app.route(
    "/login", methods=["POST"]
)  # => co-13: the ONE route this example's curl call hits
def login() -> (
    object
):  # => co-13: returns a Flask Response object with a real Set-Cookie header
    sid = secrets.token_urlsafe(
        16
    )  # => co-13: a fresh, unpredictable session id for this login
    response = make_response(
        jsonify({"sid": sid})
    )  # => co-13: the real HTTP response a browser would parse
    flags = {
        "samesite": "Strict",
        "secure": True,
        "httponly": True,
    }  # => co-26: co-13's full defensive trio together
    # => co-13: samesite="Strict" alone would already block cross-site sends -- secure/httponly harden it further
    response.set_cookie(
        "sid", sid, **flags
    )  # => co-13: sets the REAL cookie header with all three flags at once
    return response  # => co-13: the client now holds a cookie the browser itself constrains how it resends


if (
    __name__ == "__main__"
):  # => co-13: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5042
    )  # => co-13: localhost-only, fixed port -- curl targets this directly
