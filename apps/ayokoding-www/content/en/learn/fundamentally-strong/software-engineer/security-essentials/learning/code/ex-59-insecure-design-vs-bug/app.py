# learning/code/ex-59-insecure-design-vs-bug/app.py
"""Example 59: a live Flask app -- a coupon with NO one-time-use rule is replayable, even with correct code (co-25)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the design flaw itself

import sqlite3  # => co-25: stdlib DB driver -- the SAME, correctly-parameterized driver both routes use

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-25: request.get_json reads the real submitted coupon code

app = Flask(
    __name__
)  # => co-25: one Flask app, hosting both the vulnerable and fixed redemption routes
DB_PATH = (
    "coupons.db"  # => co-25: local SQLite file -- self-contained, no external DB server
)


def build_db() -> (
    None
):  # => co-25: runs once at import time -- seeds one real coupon for this example
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-25: opens (or creates) the local SQLite file
    conn.execute(
        "DROP TABLE IF EXISTS coupons"
    )  # => co-25: idempotent re-run -- always starts from a clean table
    conn.execute(
        "DROP TABLE IF EXISTS legacy_redemptions"
    )  # => co-25: a separate log the VULNERABLE route writes to
    conn.execute(
        "CREATE TABLE coupons (code TEXT PRIMARY KEY, percent_off INTEGER, redeemed_at TEXT)"
    )  # => co-25: schema
    conn.execute(
        "CREATE TABLE legacy_redemptions (code TEXT, discount_applied INTEGER)"
    )  # => co-25: a real audit log
    conn.execute(
        "INSERT INTO coupons VALUES ('SAVE20', 20, NULL)"
    )  # => co-25: one real, valid, unused coupon
    conn.commit()  # => co-25: persists the seeded coupon before any request can read it
    conn.close()  # => co-25: releases the connection -- each route below opens its own fresh connection


@app.route(
    "/legacy/redeem", methods=["POST"]
)  # => co-25: VULNERABLE -- every line here is individually "correct"
def legacy_redeem() -> tuple[
    dict[str, object], int
]:  # => co-25: returns (json_body, status)
    code = request.get_json(force=True).get(
        "code", ""
    )  # => co-01: attacker-controlled -- but harmless in shape
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-25: a fresh connection per request -- simple, not pooled
    # => co-25: a REAL, correctly parameterized query -- no SQL injection here at all
    row = conn.execute(
        "SELECT percent_off FROM coupons WHERE code = ?", (code,)
    ).fetchone()  # => co-25: safe query
    if row is None:  # => co-25: a real, correct "does this coupon exist" check
        conn.close()  # => co-25: releases the connection before the response is built
        return jsonify(
            {"error": "invalid coupon"}
        ), 404  # => co-25: a real 404 for a genuinely bogus code
    # => seeded bug: NOTHING checks whether this coupon was already redeemed -- the
    # => MISSING business rule, not a missing security control on any single line
    conn.execute(
        "INSERT INTO legacy_redemptions VALUES (?, ?)", (code, row[0])
    )  # => co-25: a real, safe INSERT
    conn.commit()  # => co-25: persists this redemption -- alongside every OTHER redemption of the SAME code
    conn.close()  # => co-25: releases the connection before the response is built
    return jsonify(
        {"discount_applied": row[0]}
    ), 200  # => co-25: succeeds EVERY time, no matter how many times before


@app.route(
    "/secure/redeem", methods=["POST"]
)  # => co-25: FIXED -- adds the missing one-time-use business rule
def secure_redeem() -> tuple[
    dict[str, object], int
]:  # => co-25: returns (json_body, status) too
    code = request.get_json(force=True).get(
        "code", ""
    )  # => co-01: the SAME shape of attacker-controlled input
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-25: a fresh connection, same as the vulnerable route above
    # => co-25: the fix -- the query itself now REQUIRES redeemed_at IS NULL to match at all
    row = conn.execute(  # => co-25: a real, correctly parameterized query, unchanged injection-safety from before
        "SELECT percent_off FROM coupons WHERE code = ? AND redeemed_at IS NULL",
        (code,),
    ).fetchone()
    if (
        row is None
    ):  # => co-25: fires for BOTH "no such coupon" AND "already redeemed" -- deliberately one message
        conn.close()  # => co-25: releases the connection before the response is built
        return jsonify(
            {"error": "coupon not valid or already used"}
        ), 409  # => co-25: a real 409, not a silent success
    conn.execute(
        "UPDATE coupons SET redeemed_at = datetime('now') WHERE code = ?", (code,)
    )  # => co-25: marks it used
    conn.commit()  # => co-25: persists the one-time-use marker BEFORE this coupon can ever match the query again
    conn.close()  # => co-25: releases the connection before the response is built
    return jsonify(
        {"discount_applied": row[0]}
    ), 200  # => co-25: succeeds EXACTLY ONCE per coupon, by construction


if (
    __name__ == "__main__"
):  # => co-25: only runs when launched directly, e.g. `python3 app.py &`
    build_db()  # => co-25: seed the one real coupon before the server starts accepting requests
    app.run(
        host="127.0.0.1", port=5059
    )  # => co-25: localhost-only, fixed port -- exploit_and_fix.py targets this
