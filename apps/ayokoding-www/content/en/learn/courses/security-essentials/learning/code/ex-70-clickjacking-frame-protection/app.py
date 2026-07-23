# learning/code/ex-70-clickjacking-frame-protection/app.py
"""Example 70: a live Flask app -- a sensitive page sends REAL X-Frame-Options and CSP frame-ancestors headers (co-19, co-25)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the frame-protection logic itself

from flask import (
    Flask,
    Response,
)  # => co-19: Response lets this route set custom headers explicitly

app = Flask(
    __name__
)  # => co-19: one Flask app, serving the one sensitive page this example protects


@app.route(
    "/legacy/account-settings"
)  # => co-19: VULNERABLE -- no frame protection headers at all
def legacy_account_settings() -> (
    Response
):  # => co-19: returns a Flask Response object -- the vulnerable route
    html = "<html><body><h1>Account Settings</h1><button>Delete Account</button></body></html>"  # => co-19: real body
    return Response(
        html, mimetype="text/html"
    )  # => co-19: NO X-Frame-Options, NO frame-ancestors -- framable by anyone


@app.route(
    "/secure/account-settings"
)  # => co-19: FIXED -- both a real X-Frame-Options AND a real CSP frame-ancestors
def secure_account_settings() -> (
    Response
):  # => co-19: returns a Flask Response object -- the fixed route
    html = "<html><body><h1>Account Settings</h1><button>Delete Account</button></body></html>"  # => co-19: SAME body
    response = Response(
        html, mimetype="text/html"
    )  # => co-19: the real HTTP response a browser would parse
    response.headers["X-Frame-Options"] = (
        "DENY"  # => co-19: the REAL, legacy but still widely honored header
    )
    response.headers["Content-Security-Policy"] = (
        "frame-ancestors 'none'"  # => co-19: the REAL, modern CSP equivalent
    )
    # => co-19: sending BOTH is deliberate defense-in-depth -- CSP frame-ancestors is the current
    # => standard and takes precedence in modern browsers, X-Frame-Options covers older clients
    return response  # => co-19: a real browser reads EITHER header and refuses to render this page inside an <iframe>


if (
    __name__ == "__main__"
):  # => co-19: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5070
    )  # => co-19: localhost-only, fixed port -- curl targets this directly
