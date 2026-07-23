# learning/code/ex-22-security-headers-baseline/headers_app.py
"""Example 22: Security Headers Baseline -- a real Flask server, run in the background for `curl -I`."""  # => co-19: docstring

from __future__ import (
    annotations,
)  # => co-19: DD-39 hygiene, unrelated to the headers themselves

from flask import (
    Flask,
    Response,
)  # => co-19: Response below is what after_request mutates on EVERY response

app = Flask(
    __name__
)  # => co-19: a single, real, listening app -- this file IS the server, not a test client


@app.after_request  # => co-19: runs on EVERY response this app sends, regardless of route
def add_security_headers(
    response: Response,
) -> Response:  # => co-19: the baseline this example verifies with curl -I
    """Attach a baseline set of security headers to every outgoing response."""  # => co-19: doc
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'"  # => co-19: restricts script/style/etc sources
    )
    response.headers["X-Content-Type-Options"] = (
        "nosniff"  # => co-19: stops the browser from MIME-sniffing content
    )
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"  # => co-19: forces HTTPS for a year
    )
    return (
        response  # => co-19: the SAME response object, now carrying all three headers
    )


@app.route(
    "/"
)  # => co-19: the ONE route this example needs -- headers apply here via after_request, above
def index() -> str:  # => co-19: the handler whose response `curl -I` inspects
    """A minimal handler -- the interesting part is the headers, not this body."""  # => co-19: doc
    return "ok"  # => co-19: the response body -- irrelevant to this example, only headers matter


if (
    __name__ == "__main__"
):  # => co-19: entry point -- binds 127.0.0.1 only, never 0.0.0.0, for a local-only demo
    app.run(
        host="127.0.0.1", port=5022, debug=False
    )  # => co-19: a REAL listening server, for the curl -I in this example
