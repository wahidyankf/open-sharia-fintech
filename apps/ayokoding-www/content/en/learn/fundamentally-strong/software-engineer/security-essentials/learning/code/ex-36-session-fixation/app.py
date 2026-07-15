"""Example 36: a live Flask app -- a pre-login session id stays valid after login, then regenerating it fixes fixation (co-12)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the fixation issue itself

import secrets  # => co-12: cryptographically random session ids -- must be unguessable

from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)  # => co-12: make_response lets a route set cookies explicitly

app = Flask(
    __name__
)  # => co-12: one Flask app, hosting both the vulnerable and fixed login routes
SESSIONS: dict[
    str, str | None
] = {}  # => co-12: server-side session store -- sid -> logged-in username (or None)


@app.route(
    "/legacy/visit"
)  # => co-12: issues a session id BEFORE any login -- exactly what an attacker pre-sets
def legacy_visit() -> (
    object
):  # => co-12: returns a Flask Response object with a real Set-Cookie header
    sid = request.cookies.get("sid") or secrets.token_urlsafe(
        16
    )  # => co-12: reuses a cookie if already present
    SESSIONS.setdefault(
        sid, None
    )  # => co-12: registers the sid with no user attached yet -- a real "anonymous" session
    response = make_response(
        jsonify({"sid": sid})
    )  # => co-12: echoes the sid so this example can show it explicitly
    response.set_cookie(
        "sid", sid
    )  # => co-12: sets the REAL cookie a browser would store and resend
    return response  # => co-12: this is the exact response an attacker's pre-login visit would receive


@app.route(
    "/legacy/login", methods=["POST"]
)  # => co-12: VULNERABLE -- logs in WITHOUT rotating the session id
def legacy_login() -> (
    object
):  # => co-12: returns a Flask Response object -- the vulnerable login handler
    sid = request.cookies.get(
        "sid", ""
    )  # => co-12: the SAME sid the client (or attacker) already had, unchanged
    username = request.json.get(
        "username", ""
    )  # => co-01: attacker-adjacent -- the victim's real submitted username
    # => seeded bug: SESSIONS[sid] is updated in place -- the sid itself never changes
    SESSIONS[sid] = (
        username  # => co-12: the PRE-EXISTING sid is now a fully authenticated session
    )
    return jsonify(
        {"sid": sid, "logged_in_as": username}
    )  # => co-12: same sid, now privileged


@app.route(
    "/legacy/whoami"
)  # => co-12: reveals who (if anyone) the presented sid is currently logged in as
def legacy_whoami() -> (
    object
):  # => co-12: returns a Flask Response object -- a real, read-only lookup
    sid = request.cookies.get(
        "sid", ""
    )  # => co-12: whatever sid this specific request presents
    return jsonify(
        {"logged_in_as": SESSIONS.get(sid)}
    )  # => co-12: real, current lookup -- None if not logged in


@app.route(
    "/secure/login", methods=["POST"]
)  # => co-12: FIXED -- regenerates the session id on successful login
def secure_login() -> (
    object
):  # => co-12: returns a Flask Response object -- the fixed login handler
    old_sid = request.cookies.get(
        "sid", ""
    )  # => co-12: the pre-login sid, about to be discarded
    username = request.json.get(
        "username", ""
    )  # => co-12: the SAME victim-submitted username as the vulnerable route
    SESSIONS.pop(
        old_sid, None
    )  # => co-12: the fix -- the OLD sid is invalidated, not just relabeled
    new_sid = secrets.token_urlsafe(
        16
    )  # => co-12: a BRAND NEW, unpredictable sid -- the attacker never saw this one
    SESSIONS[new_sid] = username  # => co-12: only the NEW sid is ever authenticated
    response = make_response(
        jsonify({"sid": new_sid, "logged_in_as": username})
    )  # => co-12: a different sid, returned
    response.set_cookie(
        "sid", new_sid
    )  # => co-12: overwrites the client's cookie with the new, safe sid
    return response  # => co-12: the client's OLD (attacker-known) sid is now dead


if (
    __name__ == "__main__"
):  # => co-12: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5036
    )  # => co-12: localhost-only, fixed port -- exploit_and_fix.py targets this
