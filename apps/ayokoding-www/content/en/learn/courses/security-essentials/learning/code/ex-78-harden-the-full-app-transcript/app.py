# learning/code/ex-78-harden-the-full-app-transcript/app.py
"""Example 78: ONE live Flask app -- 3 real attack surfaces (SQLi, XSS, missing auth), unhardened AND hardened routes (co-01, co-24, co-02)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the combined hardening itself

import sqlite3  # => co-03: stdlib DB driver -- backs the login attack surface

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-01: request reads every attacker-controlled input this app processes
from functools import (
    wraps,
)  # => co-16: preserves the wrapped view function's identity through require_admin
from markupsafe import (
    escape,
)  # => co-06: MarkupSafe -- the REAL output-encoding fix for the comment attack surface

app = Flask(
    __name__
)  # => co-01: one Flask app, hosting BOTH the unhardened and hardened route sets for all 3 attacks
DB_PATH = (
    "app.db"  # => co-03: local SQLite file -- self-contained, no external DB server
)
COMMENTS: list[
    str
] = []  # => co-06: real, in-memory comment store -- shared between legacy and secure comment routes
USERS_ROLES = {
    "alice": "user",
    "root": "admin",
}  # => co-16: a real role table for the missing-auth attack surface


def build_db() -> (
    None
):  # => co-03: runs once at import time -- seeds one real login row this attack surface targets
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-03: opens (or creates) the local SQLite file
    conn.execute(
        "DROP TABLE IF EXISTS users"
    )  # => co-03: idempotent re-run -- always starts from a clean table
    conn.execute(
        "CREATE TABLE users (username TEXT, password TEXT)"
    )  # => co-03: schema
    conn.execute(
        "INSERT INTO users VALUES ('alice', 'correct-horse')"
    )  # => co-03: the one real seeded account
    conn.commit()  # => co-03: persists the seeded row before any request can read it
    conn.close()  # => co-03: releases the connection -- each route below opens its own fresh connection


# === attack surface 1: SQL injection on login ===================================================


@app.route(
    "/legacy/login", methods=["POST"]
)  # => co-03: VULNERABLE -- f-string SQL, the SAME shape as ex-03
def legacy_login() -> tuple[
    dict[str, object], int
]:  # => co-03: returns (json_body, status)
    body = request.get_json(
        force=True
    )  # => co-01: attacker-controlled -- the real submitted credentials
    username = body.get("username", "")  # => co-01: attacker-controlled username
    password = body.get("password", "")  # => co-01: attacker-controlled password
    conn = sqlite3.connect(DB_PATH)  # => co-03: a fresh connection per request
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"  # seeded bug: f-string SQL
    row = conn.execute(
        query
    ).fetchone()  # => co-03: executes whatever the injected query says
    conn.close()  # => co-03: releases the connection before the response is built
    return jsonify(
        {"logged_in": row is not None}
    ), 200  # => co-03: real, injectable login result


@app.route(
    "/secure/login", methods=["POST"]
)  # => co-03: FIXED -- parameterized query, no injection at all
def secure_login() -> tuple[
    dict[str, object], int
]:  # => co-03: returns (json_body, status)
    body = request.get_json(
        force=True
    )  # => co-01: the SAME shape of attacker-controlled input
    username = body.get("username", "")  # => co-01: attacker-controlled username
    password = body.get("password", "")  # => co-01: attacker-controlled password
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-03: a fresh connection, same as the vulnerable route above
    row = conn.execute(  # => co-03: a REAL, parameterized query -- username/password sent as DATA, not SQL text
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    ).fetchone()
    conn.close()  # => co-03: releases the connection before the response is built
    return jsonify(
        {"logged_in": row is not None}
    ), 200  # => co-03: real, injection-safe login result


# === attack surface 2: stored XSS via unescaped comment rendering ================================


@app.route(
    "/legacy/comment", methods=["POST"]
)  # => co-06: VULNERABLE -- stores raw, unescaped comment text
def legacy_comment() -> tuple[
    dict[str, object], int
]:  # => co-06: returns (json_body, status)
    text = request.get_json(force=True).get(
        "text", ""
    )  # => co-01: attacker-controlled comment text
    COMMENTS.append(
        text
    )  # => co-06: stores the RAW, unescaped text -- the seeded bug lives in the RENDER route below
    return jsonify({"stored": True}), 201  # => co-06: real, successful storage


@app.route(
    "/legacy/comments"
)  # => co-06: VULNERABLE -- renders stored comments WITHOUT encoding
def legacy_comments() -> str:  # => co-06: returns a plain HTML string
    return (
        "<div>" + "</div><div>".join(COMMENTS) + "</div>"
    )  # seeded bug: raw concatenation, no escape() at all


@app.route(
    "/secure/comment", methods=["POST"]
)  # => co-06: FIXED -- storage is unchanged, the FIX is in rendering
def secure_comment() -> tuple[
    dict[str, object], int
]:  # => co-06: returns (json_body, status)
    text = request.get_json(force=True).get(
        "text", ""
    )  # => co-01: the SAME shape of attacker-controlled input
    COMMENTS.append(
        text
    )  # => co-06: storing raw text is fine -- output encoding is what actually matters (co-06)
    return jsonify({"stored": True}), 201  # => co-06: real, successful storage


@app.route(
    "/secure/comments"
)  # => co-06: FIXED -- every comment is encoded for its HTML context before rendering
def secure_comments() -> str:  # => co-06: returns a plain HTML string
    return (
        "<div>" + "</div><div>".join(str(escape(c)) for c in COMMENTS) + "</div>"
    )  # => co-06: the real fix


# === attack surface 3: missing function-level authorization on an admin route ====================


@app.route(
    "/legacy/admin/stats"
)  # => co-16: VULNERABLE -- no role check at all, the SAME shape as ex-34
def legacy_admin_stats() -> tuple[
    dict[str, object], int
]:  # => co-16: returns (json_body, status)
    return jsonify(
        {"total_users": len(USERS_ROLES), "roles": USERS_ROLES}
    ), 200  # seeded bug: leaks to ANY caller


def require_admin(
    view_func,
):  # => co-16: the SAME real decorator pattern as ex-34's fix
    @wraps(
        view_func
    )  # => co-16: keeps Flask's URL-rule machinery happy with the wrapped function's identity
    def wrapper(
        *args: object, **kwargs: object
    ) -> tuple[dict[str, object], int]:  # => co-16: intercepts EVERY call
        caller = request.headers.get(
            "X-User-Id", ""
        )  # => co-16: who is calling -- simulates an authenticated session
        role = USERS_ROLES.get(
            caller, ""
        )  # => co-16: the caller's REAL role, looked up server-side
        if (
            role != "admin"
        ):  # => co-16: the actual enforcement point -- runs BEFORE the real view function
            return jsonify(
                {"error": "forbidden"}
            ), 403  # => co-16: a real 403 -- the view function never even runs
        return view_func(
            *args, **kwargs
        )  # => co-16: only reached once the role check has already passed

    return wrapper  # => co-16: the decorated view now carries this check on every single request


@app.route(
    "/secure/admin/stats"
)  # => co-16: FIXED -- the SAME logic, now behind require_admin
@require_admin  # => co-16: this ONE line is the fix -- function-level authorization, applied at the route
def secure_admin_stats() -> tuple[
    dict[str, object], int
]:  # => co-16: returns (json_body, status)
    return jsonify(
        {"total_users": len(USERS_ROLES), "roles": USERS_ROLES}
    ), 200  # => co-16: identical body, gated access


if (
    __name__ == "__main__"
):  # => co-01: only runs when launched directly, e.g. `python3 app.py &`
    build_db()  # => co-03: seed the login row before the server starts accepting requests
    app.run(
        host="127.0.0.1", port=5078
    )  # => co-01: localhost-only, fixed port -- attack_transcript.py targets this
