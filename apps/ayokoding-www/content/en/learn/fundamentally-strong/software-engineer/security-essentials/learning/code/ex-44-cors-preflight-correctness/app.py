"""Example 44: a live Flask app -- a correct CORS preflight declaring exact allowed methods/headers/origin (co-20)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the preflight logic itself

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-20: request.method distinguishes the preflight from the real call

app = Flask(
    __name__
)  # => co-20: one Flask app, hosting the credentialed cross-origin route and its preflight
ALLOWED_ORIGIN = "https://trusted-app.example.com"  # => co-20: the ONE origin this server ever authorizes
ALLOWED_METHODS = "GET, POST"  # => co-20: the ONLY methods this server declares as permitted, nothing broader
ALLOWED_HEADERS = "Content-Type, X-Requested-With"  # => co-20: the ONLY custom headers this server declares


@app.route(
    "/api/resource", methods=["GET", "POST", "OPTIONS"]
)  # => co-20: OPTIONS handles the real preflight
def resource() -> (
    object
):  # => co-20: returns a Flask Response object -- serves BOTH the preflight and the real call
    if (
        request.method == "OPTIONS"
    ):  # => co-20: a browser sends OPTIONS BEFORE the real GET/POST for this route
        response = jsonify(
            {}
        )  # => co-20: an empty body -- preflight responses carry no real payload
        response.headers["Access-Control-Allow-Origin"] = (
            ALLOWED_ORIGIN  # => co-20: exactly ONE origin, never reflected
        )
        response.headers["Access-Control-Allow-Methods"] = (
            ALLOWED_METHODS  # => co-20: the declared method allow-list
        )
        response.headers["Access-Control-Allow-Headers"] = (
            ALLOWED_HEADERS  # => co-20: the declared header allow-list
        )
        response.headers["Access-Control-Allow-Credentials"] = (
            "true"  # => co-20: credentialed request support
        )
        response.headers["Access-Control-Max-Age"] = (
            "600"  # => co-20: lets the browser cache this preflight answer
        )
        return response  # => co-20: the browser reads these headers to decide whether the REAL request may proceed
    # => co-20: reached only for a REAL GET or POST -- a browser only sends one after the preflight above passed
    return jsonify(
        {"data": "the real resource, only reached after a passing preflight"}
    )  # => co-20: the actual payload


if (
    __name__ == "__main__"
):  # => co-20: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5044
    )  # => co-20: localhost-only, fixed port -- curl targets this directly
