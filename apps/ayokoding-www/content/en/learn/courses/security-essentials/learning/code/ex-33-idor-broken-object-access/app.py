"""Example 33: a live Flask app -- IDOR lets one user read another's order, then an ownership check fixes it (co-15, co-16)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the access-control issue itself

import sqlite3  # => co-15: stdlib DB driver -- the SAME driver both routes below use

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-15: request.headers reads the caller-supplied identity header

app = Flask(
    __name__
)  # => co-15: one Flask app, hosting both the vulnerable and fixed order-lookup routes
DB_PATH = (
    "idor.db"  # => co-15: local SQLite file -- self-contained, no external DB server
)


def build_db() -> (
    None
):  # => co-15: runs once at import time -- seeds two users' orders for this example
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-15: opens (or creates) the local SQLite file
    conn.execute(
        "DROP TABLE IF EXISTS orders"
    )  # => co-15: idempotent re-run -- always starts from a clean table
    conn.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, owner_id TEXT, item TEXT)"
    )  # => co-15: schema
    conn.execute(
        "INSERT INTO orders VALUES (101, 'alice', 'alice-secret-gift')"
    )  # => co-16: alice's OWN order
    conn.execute(
        "INSERT INTO orders VALUES (102, 'bob', 'bob-secret-gift')"
    )  # => co-16: bob's OWN order -- not alice's
    conn.commit()  # => co-15: persists both seeded rows before any request can read them
    conn.close()  # => co-15: releases the connection -- each route below opens its own fresh connection


@app.route(
    "/legacy/orders/<int:order_id>"
)  # => co-15: VULNERABLE -- no ownership check at all
def legacy_get_order(
    order_id: int,
) -> tuple[dict[str, object], int]:  # => co-15: returns (json_body, status)
    requesting_user = request.headers.get(
        "X-User-Id", ""
    )  # => co-15: who is ASKING -- simulates an authenticated session
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-15: a fresh connection per request -- simple, not pooled
    # => seeded bug: order_id alone selects the row -- requesting_user is read but NEVER checked
    row = conn.execute(
        "SELECT id, owner_id, item FROM orders WHERE id = ?", (order_id,)
    ).fetchone()  # => co-15: IDOR
    conn.close()  # => co-15: releases the connection before the response is built
    if row is None:  # => co-15: the only guard present -- existence, not ownership
        return jsonify(
            {"error": "not found"}
        ), 404  # => co-15: a real 404 for a genuinely missing order
    return jsonify(
        {"id": row[0], "owner_id": row[1], "item": row[2]}
    ), 200  # => co-15: leaks ANY user's order


@app.route(
    "/secure/orders/<int:order_id>"
)  # => co-16: FIXED -- ownership enforced in the query itself
def secure_get_order(
    order_id: int,
) -> tuple[dict[str, object], int]:  # => co-16: returns (json_body, status) too
    requesting_user = request.headers.get(
        "X-User-Id", ""
    )  # => co-15: the SAME "who is asking" as the vulnerable route
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-16: a fresh connection, same as the vulnerable route above
    query = "SELECT id, owner_id, item FROM orders WHERE id = ? AND owner_id = ?"  # => co-16: ownership IN the WHERE clause
    row = conn.execute(
        query, (order_id, requesting_user)
    ).fetchone()  # => co-16: only matches if BOTH id and owner agree
    conn.close()  # => co-16: releases the connection before the response is built
    if (
        row is None
    ):  # => co-16: fires for BOTH "no such order" and "not yours" -- deliberately indistinguishable
        return jsonify(
            {"error": "not found"}
        ), 404  # => co-16: same 404 either way -- no ownership info leaked
    return jsonify(
        {"id": row[0], "owner_id": row[1], "item": row[2]}
    ), 200  # => co-16: only the real owner ever sees this


if (
    __name__ == "__main__"
):  # => co-15: only runs when launched directly, e.g. `python3 app.py &`
    build_db()  # => co-15: seed both users' orders before the server starts accepting requests
    app.run(
        host="127.0.0.1", port=5033
    )  # => co-15: localhost-only, fixed port -- exploit_and_fix.py targets this
