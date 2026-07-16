# learning/code/ex-80-secure-error-and-logging-review/app.py
"""Example 80: a live Flask app -- every error path returns a generic message to the client, logs full detail server-side, never a password (co-23, co-22)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the safe-error/logging logic itself

import io  # => co-22: captures the REAL, structured server-side log in-memory, for this example's own inspection
import json  # => co-22: every server-side log line below is REAL JSON -- parsed back for verification, not assumed
import logging  # => co-22: the stdlib logging module -- the SAME machinery a real production service would use
import sqlite3  # => co-23: stdlib DB driver -- the real source of some of the internal errors this example fuzzes

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-01: request reads every real, attacker-controlled fuzz input

app = Flask(
    __name__
)  # => co-23: one Flask app -- every route below applies the SAME safe-error-handling discipline
DB_PATH = (
    "app.db"  # => co-23: local SQLite file -- self-contained, no external DB server
)

LOG_STREAM = (
    io.StringIO()
)  # => co-22: a real, in-memory sink -- stands in for a real log file/aggregator
_handler = logging.StreamHandler(
    LOG_STREAM
)  # => co-22: a real stdlib handler, writing to the stream above


class JsonFormatter(
    logging.Formatter
):  # => co-22: a real Formatter -- controls EXACTLY what ends up on the wire
    def format(
        self, record: logging.LogRecord
    ) -> str:  # => co-22: called once per real log call, by the logging module
        payload = {  # => co-22: the REAL, closed set of fields this formatter ever emits
            "action": getattr(
                record, "action", None
            ),  # => co-22: WHAT was attempted -- a fixed vocabulary
            "outcome": getattr(
                record, "outcome", None
            ),  # => co-22: the REAL result -- "error", "not_found", etc.
            "error_type": getattr(
                record, "error_type", None
            ),  # => co-23: the REAL exception type name, safe to log
            "detail": getattr(
                record, "detail", None
            ),  # => co-23: the REAL internal detail -- server-side ONLY, never sent to the client
        }  # => co-22: notice: "password" is not, and can never be, a key this formatter reads or emits
        return json.dumps(
            payload
        )  # => co-22: one real, compact JSON object per log line -- machine-queryable


_handler.setFormatter(
    JsonFormatter()
)  # => co-22: EVERY line this handler writes goes through JsonFormatter first
audit_logger = logging.getLogger(
    "ex80.audit"
)  # => co-22: a real, named logger -- isolated from Python's root logger
audit_logger.setLevel(
    logging.INFO
)  # => co-22: real logs at INFO and above are captured
audit_logger.addHandler(
    _handler
)  # => co-22: wires the REAL handler+formatter pair onto this logger
audit_logger.propagate = False  # => co-22: keeps this example's captured output limited to exactly this stream


def build_db() -> (
    None
):  # => co-23: runs once at import time -- seeds one real row this route's happy path can find
    conn = sqlite3.connect(
        DB_PATH
    )  # => co-23: opens (or creates) the local SQLite file
    conn.execute(
        "DROP TABLE IF EXISTS items"
    )  # => co-23: idempotent re-run -- always starts from a clean table
    conn.execute(
        "CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)"
    )  # => co-23: schema
    conn.execute(
        "INSERT INTO items VALUES (1, 'widget')"
    )  # => co-23: one real seeded row
    conn.commit()  # => co-23: persists the seeded row before any request can read it
    conn.close()  # => co-23: releases the connection -- each route below opens its own fresh connection


@app.route(
    "/lookup"
)  # => co-23: fuzzed with malformed/edge-case `id` values -- the real error-path target
def lookup() -> tuple[
    dict[str, object], int
]:  # => co-23: returns (json_body, status) -- ALWAYS a generic body on error
    raw_id = request.args.get(
        "id", ""
    )  # => co-01: attacker/fuzzer-controlled -- never validated before this point
    try:  # => co-23: the REAL boundary -- everything inside can raise, nothing inside ever reaches the client raw
        item_id = int(
            raw_id
        )  # => co-23: a REAL conversion that can genuinely raise ValueError on malformed input
        conn = sqlite3.connect(DB_PATH)  # => co-23: a fresh connection per request
        row = conn.execute(
            "SELECT name FROM items WHERE id = ?", (item_id,)
        ).fetchone()  # => co-03: real, parameterized
        conn.close()  # => co-23: releases the connection before the response is built
        if (
            row is None
        ):  # => co-23: a real, ordinary "not found" -- not an exception, not an internal error
            audit_logger.info(
                "lookup",
                extra={
                    "action": "lookup",
                    "outcome": "not_found",
                    "error_type": None,
                    "detail": raw_id,
                },
            )
            return jsonify(
                {"error": "item not found"}
            ), 404  # => co-23: a real, generic, safe 404
        return jsonify({"name": row[0]}), 200  # => co-23: the real, successful result
    except Exception as exc:  # => co-23: catches EVERY real internal failure -- ValueError, sqlite3 errors, anything
        audit_logger.info(  # => co-22: the REAL, full internal detail -- server-side log ONLY, never in the response
            "lookup",
            extra={
                "action": "lookup",
                "outcome": "error",
                "error_type": type(exc).__name__,
                "detail": str(exc),
            },
        )
        return jsonify(
            {"error": "unable to process request"}
        ), 400  # => co-23: a real, GENERIC message -- no internals


@app.route(
    "/login", methods=["POST"]
)  # => co-23: fuzzed with malformed JSON bodies -- the real error-path target
def login() -> tuple[
    dict[str, object], int
]:  # => co-23: returns (json_body, status) -- ALWAYS a generic body on error
    username_for_log = None  # => co-22: captured BEFORE the try block so the log still has a `user` field on error
    try:  # => co-23: the REAL boundary -- malformed input can genuinely raise here (wrong types, missing keys)
        body = request.get_json(
            force=True
        )  # => co-01: attacker/fuzzer-controlled -- may not even be a JSON object
        username = body[
            "username"
        ]  # => co-23: a REAL KeyError if missing, a real TypeError if body isn't a dict
        password = body[
            "password"
        ]  # => co-23: a REAL KeyError if missing -- NEVER logged, whatever happens next
        username_for_log = (
            username if isinstance(username, str) else repr(username)
        )  # => co-22: safe for the log call
        normalized = (
            username.strip().lower()
        )  # => co-23: a REAL AttributeError if username isn't a real string
        _ = len(
            password
        )  # => co-23: a REAL TypeError if password isn't sized (e.g. an int) -- password value UNUSED
        audit_logger.info(  # => co-22: a real, structured log line -- user/action/outcome, NEVER the password VALUE
            "login",
            extra={
                "action": "login",
                "outcome": "checked",
                "error_type": None,
                "detail": f"user={normalized}",
            },
        )
        return jsonify(
            {"status": "checked"}
        ), 200  # => co-23: a real, generic, successful response
    except (
        Exception
    ) as exc:  # => co-23: catches EVERY real internal failure from the block above
        audit_logger.info(  # => co-22: the REAL, full internal detail -- server-side log ONLY, password value NEVER included
            "login",
            extra={
                "action": "login",
                "outcome": "error",
                "error_type": type(exc).__name__,
                "detail": f"user={username_for_log}",
            },
        )
        return jsonify(
            {"error": "unable to process request"}
        ), 400  # => co-23: a real, GENERIC message -- no internals


@app.route(
    "/debug/log-contents"
)  # => co-22: TEST-ONLY introspection route -- returns the real captured log, verbatim
def debug_log_contents() -> tuple[
    dict[str, object], int
]:  # => co-22: read-only, no request body needed
    return jsonify(
        {"log": LOG_STREAM.getvalue()}
    ), 200  # => co-22: the REAL, complete captured log text so far


if (
    __name__ == "__main__"
):  # => co-23: only runs when launched directly, e.g. `python3 app.py &`
    build_db()  # => co-23: seed the one real row before the server starts accepting requests
    app.run(
        host="127.0.0.1", port=5080
    )  # => co-23: localhost-only, fixed port -- fuzz_and_verify.py targets this
