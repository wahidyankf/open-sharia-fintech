"""Example 28: a live Flask app exposing a blind boolean SQL-injection oracle, then the fix (co-03)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the injection itself

import sqlite3  # => co-03: stdlib DB driver -- the SAME driver both the vulnerable and fixed route use

from flask import (
    Flask,
    Response,
    request,
)  # => co-03: request.args reads attacker-controlled query params

app = Flask(
    __name__
)  # => co-03: one Flask app instance, hosting both the vulnerable and fixed routes
DB_PATH = "blind_sqli.db"  # => co-03: local SQLite file -- self-contained, no external DB server


def build_db() -> (
    None
):  # => co-03: runs once at import time -- seeds the one secret row this example targets
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-03: opens (or creates) the local SQLite file
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )  # => co-03: schema
    conn.execute(
        "DELETE FROM users"
    )  # => co-03: idempotent re-run -- clears any row left from a prior server start
    conn.execute(
        "INSERT INTO users (id, username, password) VALUES (1, 'admin', 'z7qphrase')"
    )  # => co-03: the secret
    conn.commit()  # => co-03: persists the seeded row to disk before any request can read it
    conn.close()  # => co-03: releases the connection -- each route below opens its own fresh connection


@app.route(
    "/legacy/check-oracle"
)  # => co-03: VULNERABLE -- naive f-string boolean oracle
def legacy_check_oracle() -> tuple[
    str, int
]:  # => co-03: returns (body, status) -- Flask's shorthand tuple form
    id_value = request.args.get(
        "id", "1"
    )  # => co-01: attacker-controlled -- never validated as an integer
    letter = request.args.get(
        "letter", ""
    )  # => co-01: attacker-controlled candidate character
    position = request.args.get(
        "position", "1"
    )  # => co-01: attacker-controlled 1-based SUBSTR position
    # => seeded bug: id_value/letter/position are spliced directly into SQL text
    # => an attacker who controls `id_value` can append arbitrary SQL after "1"
    query = f"SELECT 1 FROM users WHERE id={id_value} AND SUBSTR(password, {position}, 1) = '{letter}'"  # => co-03: f-string SQL
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-03: a fresh connection per request -- simple, not pooled
    cursor = conn.execute(
        query
    )  # => co-03: executes whatever `query` says, injected or not
    row = (
        cursor.fetchone()
    )  # => co-03: None means no match, a tuple means match -- the oracle signal itself
    conn.close()  # => co-03: releases the connection before the response is built
    if (
        row is not None
    ):  # => co-03: the TRUE branch of the oracle -- distinct HTTP response
        return (
            "MATCH",
            200,
        )  # => co-03: attacker reads this 200/"MATCH" as "letter is correct"
    return (
        "NO MATCH",
        404,
    )  # => co-03: attacker reads this 404 as "letter is wrong" -- same oracle, other branch


@app.route(
    "/secure/check"
)  # => co-03: FIXED -- parameterized query, no boolean oracle exposed
def secure_check() -> tuple[
    str, int
]:  # => co-03: returns (body, status) too, but the status never varies
    id_value = request.args.get(
        "id", "1"
    )  # => co-01: still attacker-controlled, but now bound as DATA not SQL
    letter = request.args.get(
        "letter", ""
    )  # => co-01: also bound as data -- cannot change the query's shape
    position = request.args.get(
        "position", "1"
    )  # => co-01: also bound as data -- SQLite coerces text to int safely
    query = "SELECT 1 FROM users WHERE id = ? AND SUBSTR(password, ?, 1) = ?"  # => co-03: placeholders, not f-string
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-03: a fresh connection, same as the vulnerable route above
    conn.execute(
        query, (id_value, position, letter)
    )  # => co-03: id_value/letter/position sent as PARAMETERS, not text
    conn.close()  # => co-03: the query's result is deliberately discarded -- never inspected here
    # => co-03: the response is IDENTICAL no matter what the query found -- this removes
    # => the true/false oracle itself, not just the SQL-injection vector that fed it
    return Response(
        "checked", status=200, mimetype="text/plain"
    )  # => co-03: always 200 "checked", never varies


if (
    __name__ == "__main__"
):  # => co-03: only runs when launched directly, e.g. `python3 app.py &`
    build_db()  # => co-03: seed the secret row before the server starts accepting requests
    app.run(
        host="127.0.0.1", port=5028
    )  # => co-03: localhost-only, fixed port -- exploit_and_fix.py targets this
