# learning/code/ex-08-reflected-xss-live/greet_app.py
"""Example 8: Reflected XSS -- Live."""  # => co-06: module docstring

from __future__ import (
    annotations,
)  # => co-06: DD-39 hygiene, unrelated to the exploit itself

from flask import (
    Flask,
    request,
)  # => co-06: request.args below is the tainted (co-01) query-string source
from markupsafe import (
    escape,
)  # => co-06: the fix -- Flask's own bundled HTML-escaping helper

app = Flask(
    __name__
)  # => co-06: a single throwaway app -- both routes share it, self-contained per-run


@app.route(
    "/greet"
)  # => co-06: the VULNERABLE route -- reflects `name` with zero encoding
def greet_naive() -> (
    str
):  # => co-06: response body IS the return value here -- an f-string, not a template
    """Echo the name query param straight into HTML -- VULNERABLE, do not copy."""  # => co-06: doc
    name = request.args.get(
        "name", ""
    )  # => co-01: query-string value -- fully attacker-controlled
    return f"<h1>Hello, {name}</h1>"  # => co-06: name is spliced into HTML text with NO encoding at all


@app.route(
    "/greet_safe"
)  # => co-06: the FIXED route -- same tainted param, encoded before rendering
def greet_safe() -> (
    str
):  # => co-06: response body is again a plain f-string, but now around escape()
    """Echo the name query param through markupsafe.escape() -- FIXED."""  # => co-06: doc
    name = request.args.get(
        "name", ""
    )  # => co-01: the SAME tainted source as greet_naive
    return f"<h1>Hello, {escape(name)}</h1>"  # => co-06: escape() turns '<', '>', '&', quotes into HTML entities


if (
    __name__ == "__main__"
):  # => co-06: entry point -- Flask's own test client, no real socket needed
    client = (
        app.test_client()
    )  # => co-06: an in-process client -- issues real Flask request/response cycles
    payload = "<script>alert('xss')</script>"  # => co-01: the classic script-tag payload this example fires

    print(
        "=== VULNERABLE: /greet reflects the payload verbatim ==="
    )  # => co-06: the attack
    naive_body = client.get("/greet", query_string={"name": payload}).get_data(
        as_text=True
    )  # => co-06: real response body
    print(
        naive_body
    )  # => co-06: contains the LITERAL <script> tag, unescaped, exactly as sent
    assert (
        "<script>alert('xss')</script>" in naive_body
    )  # => co-06: mechanically proves the tag survived intact

    print(
        "\n=== FIXED: /greet_safe encodes the same payload ==="
    )  # => co-06: re-run against the fix
    safe_body = client.get("/greet_safe", query_string={"name": payload}).get_data(
        as_text=True
    )  # => co-06: real response body
    print(safe_body)  # => co-06: the SAME payload, now rendered as inert, visible text
    assert (
        "<script>" not in safe_body
    )  # => co-06: mechanically proves NO literal <script> tag remains
    assert (
        "&lt;script&gt;" in safe_body
    )  # => co-06: mechanically proves it was HTML-entity encoded instead
