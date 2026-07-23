# learning/code/ex-68-defense-in-depth-xss/app.py
"""Example 68: a live Flask app -- 4 independently toggleable XSS defense layers on ONE comment endpoint (co-06, co-19, co-13, co-07)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the layering logic itself

from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)  # => co-07: request.args reads THIS example's own layer toggles
from markupsafe import (
    escape,
)  # => co-06: MarkupSafe 3.0.3 (bundled with Flask 3.1.3) -- the real output-encoding layer

app = Flask(
    __name__
)  # => co-06: one Flask app -- a single route, four independently toggleable layers


@app.route(
    "/comment", methods=["POST"]
)  # => co-06: the ONE endpoint every layer combination in this example exercises
def comment() -> (
    object
):  # => co-06: returns a Flask Response object -- shape depends on which layers are active
    # => co-07: these toggles exist ONLY for this example's pedagogy -- a real app would never
    # => let a CALLER decide whether its own security layers run; they are fixed, server-side config
    validation_on = (
        request.args.get("validation", "on") == "on"
    )  # => co-07: layer 1 -- input allow/deny-list validation
    encoding_on = (
        request.args.get("encoding", "on") == "on"
    )  # => co-06: layer 2 -- output encoding before rendering
    csp_on = (
        request.args.get("csp", "on") == "on"
    )  # => co-19: layer 3 -- Content-Security-Policy response header
    body = request.get_json(
        force=True
    )  # => co-01: the real, attacker-controlled request body
    raw_comment = body.get(
        "comment", ""
    )  # => co-01: the real, untrusted comment text this whole pipeline processes

    if validation_on and (
        "<" in raw_comment or ">" in raw_comment
    ):  # => co-07: layer 1 -- a real, strict allow-list-ish check
        return jsonify(
            {"error": "comment rejected by input validation"}
        ), 400  # => co-07: blocked BEFORE rendering at all

    rendered_value = (
        str(escape(raw_comment)) if encoding_on else raw_comment
    )  # => co-06: layer 2 -- encode, or don't
    html_body = f"<div class='comment'>{rendered_value}</div>"  # => co-06: the REAL HTML this response actually returns

    response = make_response(
        html_body
    )  # => co-19: a real Flask Response object -- headers attached below
    response.headers["Content-Type"] = (
        "text/html"  # => co-06: a real, correct content type for the body above
    )
    if csp_on:  # => co-19: layer 3 -- Content-Security-Policy, toggled independently of the other three layers
        response.headers["Content-Security-Policy"] = (
            "script-src 'self'"  # => co-19: NO 'unsafe-inline', NO nonce
        )
    # => co-13: layer 4 -- HttpOnly is ALWAYS on for the session cookie in this example, deliberately
    # => never toggleable (a real app never makes ITS OWN cookie security caller-controlled either)
    response.set_cookie(
        "session", "opaque-session-value", httponly=True, secure=True, samesite="Lax"
    )  # => co-13: real
    return response  # => co-06: the real response this specific layer combination actually produces


if (
    __name__ == "__main__"
):  # => co-06: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5068
    )  # => co-06: localhost-only, fixed port -- exploit_and_fix.py targets this
