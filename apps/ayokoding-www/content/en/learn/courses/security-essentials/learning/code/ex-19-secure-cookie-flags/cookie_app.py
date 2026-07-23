# learning/code/ex-19-secure-cookie-flags/cookie_app.py
"""Example 19: Secure Cookie Flags -- a real Flask server, run in the background for `curl -I`."""  # => co-13: docstring

from __future__ import (
    annotations,
)  # => co-13: DD-39 hygiene, unrelated to the cookie flags themselves

import os  # => co-13: os.urandom seeds a real, per-run Flask session secret key

from flask import (
    Flask,
    session,
)  # => co-13: session below is what emits the Set-Cookie header this example inspects

app = Flask(
    __name__
)  # => co-13: a single, real, listening app -- this file IS the server, not a test client
app.secret_key = os.urandom(
    32
)  # => co-13: a random per-run key -- signs the session cookie, never hardcode this

# ex-19: the three cookie flags this example verifies with a real `curl -I`
app.config.update(  # => co-13: applied to EVERY cookie Flask's session mechanism sets from here on
    SESSION_COOKIE_SECURE=True,  # => co-13: browser sends this cookie ONLY over HTTPS -- blocks plaintext leakage
    SESSION_COOKIE_HTTPONLY=True,  # => co-13: JavaScript (document.cookie) CANNOT read this cookie -- blocks XSS theft
    SESSION_COOKIE_SAMESITE="Lax",  # => co-13: blocks the cookie riding along on most cross-site requests -- CSRF defense
)  # => co-13: end of the cookie-flag configuration


@app.route(
    "/login"
)  # => co-13: the ONE route this example needs -- setting session data emits Set-Cookie
def login() -> str:  # => co-13: the handler whose response `curl -I` inspects
    """Log in a fixed demo user, which makes Flask emit a Set-Cookie response header."""  # => co-13: doc
    session["user"] = (
        "alice"  # => co-13: writing to `session` is what triggers Flask to set the cookie
    )
    return "logged in"  # => co-13: the response body -- irrelevant to this example, only headers matter


if (
    __name__ == "__main__"
):  # => co-13: entry point -- binds 127.0.0.1 only, never 0.0.0.0, for a local-only demo
    app.run(
        host="127.0.0.1", port=5019, debug=False
    )  # => co-13: a REAL listening server, for the curl -I in this example
