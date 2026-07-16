"""Example 32: a live Flask app -- mass-assignment lets a client set is_admin, then an allow-list fixes it (co-08, co-07)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the mass-assignment issue itself

import sqlite3  # => co-08: stdlib DB driver -- the SAME driver both routes below use

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-08: request.get_json reads the attacker-controlled request body

app = Flask(
    __name__
)  # => co-08: one Flask app, hosting both the vulnerable and fixed registration routes
DB_PATH = "mass_assignment.db"  # => co-08: local SQLite file -- self-contained, no external DB server


def build_db() -> (
    None
):  # => co-08: runs once at import time -- fresh users table for this example
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-08: opens (or creates) the local SQLite file
    conn.execute(
        "DROP TABLE IF EXISTS users"
    )  # => co-08: idempotent re-run -- always starts from an empty table
    conn.execute(
        "CREATE TABLE users (username TEXT, password TEXT, is_admin INTEGER DEFAULT 0)"
    )  # => co-08: schema
    conn.commit()  # => co-08: persists the fresh schema before any request can write to it
    conn.close()  # => co-08: releases the connection -- each route below opens its own fresh connection


@app.route(
    "/legacy/register", methods=["POST"]
)  # => co-08: VULNERABLE -- binds the WHOLE request body
def legacy_register() -> tuple[
    dict[str, object], int
]:  # => co-08: returns (json_body, status) -- Flask tuple form
    body = request.get_json(
        force=True
    )  # => co-01: attacker-controlled -- every key the client sends, unfiltered
    # => seeded bug: every key in `body` becomes a column value -- including is_admin,
    # => a field the client was NEVER supposed to be able to set on their own registration
    columns = ", ".join(
        body.keys()
    )  # => co-08: builds the INSERT column list straight from client-supplied keys
    placeholders = ", ".join(
        "?" for _ in body
    )  # => co-08: one placeholder per client-supplied key -- still "safe" SQL
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-08: a fresh connection per request -- simple, not pooled
    conn.execute(
        f"INSERT INTO users ({columns}) VALUES ({placeholders})", tuple(body.values())
    )  # => co-08: mass assign
    conn.commit()  # => co-08: persists whatever fields the client happened to include, is_admin or not
    conn.close()  # => co-08: releases the connection before the response is built
    return jsonify(
        {"status": "registered"}
    ), 201  # => co-08: the response never reveals which fields were bound


@app.route(
    "/secure/register", methods=["POST"]
)  # => co-07: FIXED -- explicit field allow-list
def secure_register() -> tuple[
    dict[str, object], int
]:  # => co-07: returns (json_body, status) too, same shape
    body = request.get_json(
        force=True
    )  # => co-01: still attacker-controlled, but only two keys are ever read
    username = str(
        body.get("username", "")
    )  # => co-07: allow-listed field 1 -- coerced to str, extra keys ignored
    password = str(
        body.get("password", "")
    )  # => co-07: allow-listed field 2 -- coerced to str, extra keys ignored
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-07: a fresh connection, same as the vulnerable route above
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
    )  # => co-07: is_admin NEVER touched
    conn.commit()  # => co-07: persists ONLY the allow-listed fields -- is_admin stays at its schema default (0)
    conn.close()  # => co-07: releases the connection before the response is built
    return jsonify(
        {"status": "registered"}
    ), 201  # => co-07: identical response shape to the vulnerable route


@app.route(
    "/admin-count"
)  # => co-08: test-only introspection route -- counts real rows with is_admin=1
def admin_count() -> dict[
    str, int
]:  # => co-08: returns a plain JSON count -- read-only, no request body needed
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-08: a fresh connection for this read-only check
    count = conn.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1").fetchone()[
        0
    ]  # => co-08: real row count
    conn.close()  # => co-08: releases the connection before the response is built
    return jsonify(
        {"admin_count": count}
    )  # => co-08: the real, current count of admin-flagged rows


if (
    __name__ == "__main__"
):  # => co-08: only runs when launched directly, e.g. `python3 app.py &`
    build_db()  # => co-08: create the fresh users table before the server starts accepting requests
    app.run(
        host="127.0.0.1", port=5032
    )  # => co-08: localhost-only, fixed port -- exploit_and_fix.py targets this
