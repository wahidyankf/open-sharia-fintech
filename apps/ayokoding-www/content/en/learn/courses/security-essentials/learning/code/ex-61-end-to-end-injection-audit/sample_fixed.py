# learning/code/ex-61-end-to-end-injection-audit/sample_fixed.py
"""Example 61: the SAME 4 routes, each seeded sink now fixed -- for the scanner to re-sweep and find zero (co-03, co-04, co-01)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the fixes themselves

import sqlite3  # => co-03: the SAME stdlib DB driver -- only the QUERY construction changes, not the driver
import subprocess  # => co-04: real subprocess -- replaces os.system entirely, argv list instead of a shell string

from flask import (
    Flask,
    render_template_string,
    request,
)  # => co-06: render_template_string separates data from template

app = Flask(__name__)  # => co-01: one Flask app, hosting all 4 real, now-fixed routes

GREETING_TEMPLATE = "Hello, {{ name }}!"  # => co-06: a FIXED, developer-authored template string -- never built from input


@app.route(
    "/search"
)  # => co-03: FIXED -- a real, parameterized query, no string building at all
def search() -> str:  # => co-03: real route handler
    term = request.args.get("q", "")  # => co-01: still real, attacker-controlled input
    conn = sqlite3.connect(":memory:")  # => co-03: the SAME in-memory DB target
    conn.execute(
        "SELECT * FROM items WHERE name = ?", (term,)
    )  # => co-03: fix -- term is bound as DATA, not SQL text
    return "ok"  # => co-03: return value irrelevant -- this file exists to be SCANNED


@app.route(
    "/ping"
)  # => co-04: FIXED -- a real argv list, shell=False, no string concatenation at all
def ping() -> str:  # => co-04: real route handler
    host = request.args.get(
        "host", ""
    )  # => co-01: still real, attacker-controlled input
    subprocess.run(
        ["ping", "-c", "1", host], shell=False
    )  # => co-04: fix -- host is ONE argv element, never shell text
    return "ok"  # => co-04: return value irrelevant -- this file exists to be SCANNED


@app.route(
    "/greet"
)  # => co-06: FIXED -- user input passed as template CONTEXT DATA, never as the template itself
def greet() -> str:  # => co-06: real route handler
    name = request.args.get(
        "name", ""
    )  # => co-01: still real, attacker-controlled input
    return render_template_string(
        GREETING_TEMPLATE, name=name
    )  # => co-06: fix -- name is DATA, the template is FIXED


@app.route(
    "/safe-lookup"
)  # => co-03: unchanged -- was already safe, still safe after this file's fixes
def safe_lookup() -> (
    str
):  # => co-07: real route handler, unchanged from sample_vulnerable.py
    item_id = request.args.get(
        "id", ""
    )  # => co-01: real, attacker-controlled input, bound correctly below
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-03: a real, if empty, in-memory DB for this scan target
    conn.execute(
        "SELECT * FROM items WHERE id = ?", (item_id,)
    )  # => co-03: a REAL, parameterized, safe query
    return "ok"  # => co-07: return value irrelevant -- proves the scanner's precision holds across BOTH files
