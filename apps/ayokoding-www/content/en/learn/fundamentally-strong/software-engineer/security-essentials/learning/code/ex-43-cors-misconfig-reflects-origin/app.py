"""Example 43: a live Flask app -- reflects ANY Origin with credentials allowed, then an allow-list fixes it (co-20)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the CORS misconfiguration itself

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-20: request.headers reads the caller-supplied Origin header

app = Flask(
    __name__
)  # => co-20: one Flask app, hosting both the vulnerable and fixed data routes
ALLOWED_ORIGINS = {
    "https://trusted-app.example.com"
}  # => co-20: the REAL, explicit allow-list for the fixed route


@app.route(
    "/legacy/data"
)  # => co-20: VULNERABLE -- echoes back whatever Origin the caller sent
def legacy_data() -> (
    object
):  # => co-20: returns a Flask Response object -- the vulnerable route
    origin = request.headers.get(
        "Origin", ""
    )  # => co-01: attacker-controlled -- ANY value the caller chooses
    response = jsonify(
        {"secret": "cross-origin-readable-data"}
    )  # => co-20: real payload a browser script could read
    # seeded bug: reflects the caller's OWN Origin header back -- effectively "any origin is allowed"
    response.headers["Access-Control-Allow-Origin"] = (
        origin  # => co-20: the real, reflected header value
    )
    response.headers["Access-Control-Allow-Credentials"] = (
        "true"  # => co-20: PLUS credentials -- the dangerous combo
    )
    return response  # => co-20: a browser reading this would treat ANY origin as permitted, cookies included


@app.route(
    "/secure/data"
)  # => co-20: FIXED -- only a real, explicitly allow-listed origin is ever reflected
def secure_data() -> (
    object
):  # => co-20: returns a Flask Response object -- the fixed route
    origin = request.headers.get(
        "Origin", ""
    )  # => co-01: still attacker-controlled, but now checked against a list
    response = jsonify(
        {"secret": "cross-origin-readable-data"}
    )  # => co-20: the SAME payload as the vulnerable route
    if (
        origin in ALLOWED_ORIGINS
    ):  # => co-20: the fix -- an explicit, real membership check, not a blind echo
        response.headers["Access-Control-Allow-Origin"] = (
            origin  # => co-20: only set for a KNOWN, trusted origin
        )
        response.headers["Access-Control-Allow-Credentials"] = (
            "true"  # => co-20: only paired with an allow-listed origin
        )
    # => co-20: for any other origin, NO Access-Control-Allow-Origin header is set at
    # => all -- a browser then blocks the cross-origin script from reading the response
    return response  # => co-20: identical body either way -- the CORS headers are what actually gate access


if (
    __name__ == "__main__"
):  # => co-20: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5043
    )  # => co-20: localhost-only, fixed port -- curl targets this directly
