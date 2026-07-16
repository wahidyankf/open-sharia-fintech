"""Example 46: a live Flask app -- flask-limiter throttles rapid login attempts with a real 429 (co-27)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the rate-limiting logic itself

from flask import Flask, jsonify
from flask_limiter import (
    Limiter,
)  # => co-27: flask-limiter 4.1.1 pinned -- per-route request-rate enforcement
from flask_limiter.util import (
    get_remote_address,
)  # => co-27: keys the limit by the caller's real remote IP

app = Flask(
    __name__
)  # => co-27: one Flask app, hosting the rate-limited login endpoint
limiter = Limiter(
    get_remote_address, app=app, storage_uri="memory://"
)  # => co-27: in-process store -- self-contained


@app.route(
    "/login", methods=["POST"]
)  # => co-27: the protected endpoint every real request below hits
@limiter.limit(
    "5 per minute"
)  # => co-27: the REAL enforced rule -- at most 5 requests per IP, per rolling minute
def login() -> object:
    return jsonify(
        {"status": "checked"}
    )  # => co-27: a generic response -- the limiter runs BEFORE this body executes


if (
    __name__ == "__main__"
):  # => co-27: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5046
    )  # => co-27: localhost-only, fixed port -- exploit_and_fix.py targets this
