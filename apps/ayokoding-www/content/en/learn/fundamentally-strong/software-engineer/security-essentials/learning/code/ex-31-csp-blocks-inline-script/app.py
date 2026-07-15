"""Example 31: a live Flask app serving a strict nonce-based CSP header (co-19, co-06)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the CSP header itself

import secrets  # => co-19: cryptographically random nonce -- must be unpredictable per RFC/CSP spec

from flask import (
    Flask,
    Response,
)  # => co-19: Response lets this route set a custom header explicitly

app = Flask(__name__)  # => co-19: one Flask app, serving the CSP-protected page


@app.route("/page")  # => co-19: the ONE route this example's curl calls hit
def page() -> (
    Response
):  # => co-19: builds a fresh nonce and CSP header on every single request
    nonce = secrets.token_urlsafe(
        16
    )  # => co-19: a NEW random nonce per response -- never reused, never guessable
    allowed_script = f'<script nonce="{nonce}">document.title = "allowed script ran";</script>'  # => co-19: matching nonce
    blocked_script = '<script>document.title = "blocked script ran";</script>'  # => co-06: NO nonce attribute at all
    html = f"<html><body>{allowed_script}{blocked_script}</body></html>"  # => co-19: both scripts in one real HTML body
    response = Response(
        html, mimetype="text/html"
    )  # => co-19: the real HTTP response body a browser would parse
    response.headers["Content-Security-Policy"] = (
        f"script-src 'nonce-{nonce}'"  # => co-19: the REAL enforced header
    )
    # => co-19: `script-src 'nonce-X'` also drops the 'unsafe-inline' default -- only
    # => a <script> whose OWN nonce attribute equals X is permitted, per CSP Level 3
    return response  # => co-19: header and body both reference the SAME nonce value, by construction


if (
    __name__ == "__main__"
):  # => co-19: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5031
    )  # => co-19: localhost-only, fixed port -- curl targets this directly
