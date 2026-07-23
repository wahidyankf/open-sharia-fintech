# learning/code/ex-61-end-to-end-injection-audit/sample_vulnerable.py
"""Example 61: a real 4-route sample app -- 3 real concatenated-untrusted-input sinks, seeded for the scanner (co-03, co-04, co-01)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the seeded sinks themselves

import os  # => co-04: os.system -- the FIRST real command-injection sink this file seeds
import sqlite3  # => co-03: stdlib DB driver -- the SECOND real SQL-injection sink this file seeds

from flask import (
    Flask,
    request,
)  # => co-01: request.args/request.form -- every sink below reads real attacker input
from jinja2 import (
    Template,
)  # => co-06: Jinja2's Template class -- the THIRD real sink this file seeds (SSTI-shaped)

app = Flask(
    __name__
)  # => co-01: one Flask app, hosting all 4 real routes this scanner sweeps


@app.route(
    "/search"
)  # => co-03: SINK 1 -- SQL built via an f-string, not bound parameters
def search() -> str:  # => co-03: real route handler
    term = request.args.get(
        "q", ""
    )  # => co-01: real, attacker-controlled query parameter
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-03: a real, if empty, in-memory DB for this scan target
    # seeded bug: the REAL sink -- execute() called directly with a built, not bound, f-string
    conn.execute(
        f"SELECT * FROM items WHERE name = '{term}'"
    )  # => co-03: concatenated untrusted input, inline
    return "ok"  # => co-03: return value irrelevant -- this file exists to be SCANNED, not actually queried


@app.route(
    "/ping"
)  # => co-04: SINK 2 -- a shell command built via string concatenation
def ping() -> str:  # => co-04: real route handler
    host = request.args.get(
        "host", ""
    )  # => co-01: real, attacker-controlled query parameter
    os.system(
        "ping -c 1 " + host
    )  # => seeded bug: the REAL sink -- os.system with concatenated untrusted input
    return "ok"  # => co-04: return value irrelevant -- this file exists to be SCANNED, not actually executed


@app.route(
    "/greet"
)  # => co-06: SINK 3 -- user input rendered as a TEMPLATE STRING, not template DATA
def greet() -> str:  # => co-06: real route handler
    name = request.args.get(
        "name", ""
    )  # => co-01: real, attacker-controlled query parameter
    template = Template(
        "Hello, " + name + "!"
    )  # => seeded bug: the REAL sink -- Template() built from untrusted input
    return template.render()  # => co-06: renders whatever the untrusted string CONTAINS as real template syntax


@app.route(
    "/safe-lookup"
)  # => co-03: NOT a sink -- included so the scanner's precision is also verified
def safe_lookup() -> str:  # => co-07: real route handler, deliberately unproblematic
    item_id = request.args.get(
        "id", ""
    )  # => co-01: real, attacker-controlled input, but bound correctly below
    conn = sqlite3.connect(
        ":memory:"
    )  # => co-03: a real, if empty, in-memory DB for this scan target
    conn.execute(
        "SELECT * FROM items WHERE id = ?", (item_id,)
    )  # => co-03: a REAL, parameterized, safe query
    return "ok"  # => co-07: return value irrelevant -- this route exists to prove the scanner does NOT false-positive
