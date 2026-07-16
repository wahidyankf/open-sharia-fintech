# learning/code/ex-54-secret-rotation-drill/app.py
"""Example 54: a live Flask app -- a leaked API key is rotated server-side, invalidating the old one for real (co-17)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the rotation logic itself

import secrets  # => co-17: cryptographically random replacement key -- never a predictable successor

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-17: request.headers reads the caller-supplied API key

app = Flask(
    __name__
)  # => co-17: one Flask app, hosting the protected resource and the rotation endpoint
ACTIVE_KEYS: set[str] = {
    "leaked-key-8f3a9c21"
}  # => co-17: real server-side state -- the ONLY currently valid key


@app.route("/protected")  # => co-17: the resource this example's API key actually gates
def protected() -> tuple[
    dict[str, object], int
]:  # => co-17: returns (json_body, status)
    api_key = request.headers.get(
        "X-Api-Key", ""
    )  # => co-01: attacker-controlled -- whatever key the caller presents
    if (
        api_key not in ACTIVE_KEYS
    ):  # => co-17: the REAL check -- membership in server-side state, not a hardcoded string
        return jsonify(
            {"error": "unauthorized"}
        ), 401  # => co-17: a real 401 for any key not currently active
    return jsonify(
        {"data": "protected resource contents"}
    ), 200  # => co-17: only reached for a REAL active key


@app.route(
    "/admin/rotate-key", methods=["POST"]
)  # => co-17: the real rotation operation -- an operator action
def rotate_key() -> tuple[
    dict[str, object], int
]:  # => co-17: returns (json_body, status)
    body = request.get_json(
        force=True
    )  # => co-17: the real request body identifying WHICH key just leaked
    leaked_key = body.get(
        "leaked_key", ""
    )  # => co-17: the specific key being retired, not "all keys"
    if (
        leaked_key not in ACTIVE_KEYS
    ):  # => co-17: a real guard -- can't revoke a key that was never active
        return jsonify(
            {"error": "unknown key"}
        ), 404  # => co-17: a real 404 for a bogus rotation request
    new_key = secrets.token_urlsafe(
        24
    )  # => co-17: a REAL, freshly generated, unpredictable replacement
    ACTIVE_KEYS.discard(
        leaked_key
    )  # => co-17: the REAL invalidation -- removed from server-side state, not just "hidden"
    ACTIVE_KEYS.add(
        new_key
    )  # => co-17: the REAL new credential, now the only one that authenticates
    return jsonify(
        {"new_key": new_key}
    ), 200  # => co-17: returned ONCE, at rotation time -- the caller must store it now


if (
    __name__ == "__main__"
):  # => co-17: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5054
    )  # => co-17: localhost-only, fixed port -- exploit_and_fix.py targets this
