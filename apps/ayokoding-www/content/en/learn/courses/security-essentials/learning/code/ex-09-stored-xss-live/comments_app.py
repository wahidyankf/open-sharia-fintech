# learning/code/ex-09-stored-xss-live/comments_app.py
"""Example 9: Stored XSS -- Live."""  # => co-06: module docstring

from __future__ import (
    annotations,
)  # => co-06: DD-39 hygiene, unrelated to the exploit itself

import sqlite3  # => co-06: persists the payload -- this is what makes it STORED, not just reflected

from flask import (
    Flask,
    request,
)  # => co-06: request.form below is the tainted (co-01) POST-body source
from markupsafe import (
    escape,
)  # => co-06: the fix -- HTML-escapes each comment at RENDER time

app = Flask(__name__)  # => co-06: a single throwaway app -- both render routes share it
conn = sqlite3.connect(
    ":memory:", check_same_thread=False
)  # => co-06: one shared in-memory comments store
conn.execute(
    "CREATE TABLE comments (body TEXT)"
)  # => co-06: a single-column table -- the STORED payload lives here
conn.commit()  # => co-06: commits the empty schema before any comment is posted


@app.route(
    "/comments", methods=["POST"]
)  # => co-06: the write path -- storing is NOT itself the vulnerability
def post_comment() -> tuple[
    str, int
]:  # => co-06: returns (body, status) -- Flask accepts this tuple form
    """Store a comment body VERBATIM -- storage is safe, RENDERING it later is not."""  # => co-06: doc
    body = request.form[
        "body"
    ]  # => co-01: POST-body field -- fully attacker-controlled
    conn.execute(
        "INSERT INTO comments (body) VALUES (?)", (body,)
    )  # => co-03: parameterized, so storage itself is safe
    conn.commit()  # => co-06: the payload is now PERSISTED -- every future GET can render it
    return (
        "",
        201,
    )  # => co-06: 201 Created -- no body needed for this example's purposes


@app.route(
    "/comments"
)  # => co-06: the VULNERABLE read path -- renders EVERY stored comment unescaped
def view_comments_naive() -> (
    str
):  # => co-06: what a LATER visitor's browser would receive
    """Render every stored comment with an f-string -- VULNERABLE, do not copy."""  # => co-06: doc
    rows = conn.execute(
        "SELECT body FROM comments"
    ).fetchall()  # => co-06: reads back whatever was stored
    return "".join(
        f"<p>{r[0]}</p>" for r in rows
    )  # => co-06: each body is spliced into HTML with NO encoding


@app.route(
    "/comments_safe"
)  # => co-06: the FIXED read path -- same stored rows, encoded at render time
def view_comments_safe() -> (
    str
):  # => co-06: what a later visitor receives ONCE the render path is fixed
    """Render every stored comment through markupsafe.escape() -- FIXED."""  # => co-06: doc
    rows = conn.execute(
        "SELECT body FROM comments"
    ).fetchall()  # => co-06: the SAME stored rows as the naive route
    return "".join(
        f"<p>{escape(r[0])}</p>" for r in rows
    )  # => co-06: escape() runs on EVERY comment, every render


if (
    __name__ == "__main__"
):  # => co-06: entry point -- store once, then render via both routes
    client = (
        app.test_client()
    )  # => co-06: an in-process client -- issues real Flask request/response cycles
    payload = "<script>steal_cookies()</script>"  # => co-01: a payload one user's comment can plant for OTHERS

    print(
        "=== Storing the attacker's comment (a later, separate request) ==="
    )  # => co-06: the persistence step
    client.post(
        "/comments", data={"body": payload}
    )  # => co-06: ONE write -- the payload now lives in the DB

    print(
        "=== VULNERABLE: /comments renders it to EVERY later visitor ==="
    )  # => co-06: the attack surfaces here
    naive_body = client.get("/comments").get_data(
        as_text=True
    )  # => co-06: a DIFFERENT request, real response body
    print(naive_body)  # => co-06: the stored <script> tag, still literal, unescaped
    assert (
        "<script>steal_cookies()</script>" in naive_body
    )  # => co-06: mechanically proves it survived storage AND render

    print(
        "\n=== FIXED: /comments_safe encodes at render time ==="
    )  # => co-06: re-run against the fix
    safe_body = client.get("/comments_safe").get_data(
        as_text=True
    )  # => co-06: the SAME stored row, different route
    print(safe_body)  # => co-06: rendered as inert, visible text instead of markup
    assert (
        "<script>" not in safe_body
    )  # => co-06: mechanically proves no literal <script> tag remains
    assert (
        "&lt;script&gt;" in safe_body
    )  # => co-06: mechanically proves it was HTML-entity encoded instead
