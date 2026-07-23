# learning/code/ex-50-directory-listing-and-default-creds/app.py
"""Example 50: a live Flask app -- directory listing + a hardcoded default admin cred, then both are closed (co-24)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the misconfiguration itself

import os  # => co-24: builds a real on-disk static folder this example actually serves from

from flask import (
    Flask,
    abort,
    jsonify,
    request,
    send_from_directory,
)  # => co-24: send_from_directory serves real files

app = Flask(
    __name__
)  # => co-24: one Flask app, hosting both the vulnerable and fixed halves
STATIC_DIR = os.path.join(
    os.path.dirname(__file__), "public_files"
)  # => co-24: a real folder on disk, seeded below
PUBLIC_ALLOW_LIST = {
    "readme.txt",
    "logo.txt",
}  # => co-24: the ONLY filenames the fixed route will ever serve


def seed_static_dir() -> (
    None
):  # => co-24: runs once at import time -- creates real files this example actually reads
    os.makedirs(
        STATIC_DIR, exist_ok=True
    )  # => co-24: idempotent -- safe to call on every server start
    with open(
        os.path.join(STATIC_DIR, "readme.txt"), "w"
    ) as f:  # => co-24: a genuinely public, intended-to-be-served file
        f.write(
            "Welcome -- this file is meant to be public.\n"
        )  # => co-24: real bytes on disk
    with open(
        os.path.join(STATIC_DIR, "logo.txt"), "w"
    ) as f:  # => co-24: another genuinely public file
        f.write("ASCII logo placeholder.\n")  # => co-24: real bytes on disk
    with open(
        os.path.join(STATIC_DIR, "secret-notes.txt"), "w"
    ) as f:  # => co-24: NEVER meant to be web-reachable
        f.write(
            "db_password=hunter2-internal-only\n"
        )  # => co-24: the real sensitive content directory listing exposes


@app.route(
    "/legacy/files/"
)  # => co-24: VULNERABLE -- a real directory listing of the whole static folder
def legacy_list_files() -> (
    object
):  # => co-24: returns a Flask Response object -- the vulnerable listing route
    # => seeded bug: os.listdir() enumerates EVERY file in STATIC_DIR, intended or not,
    # => and hands the full real filename list straight back to any caller
    names = sorted(
        os.listdir(STATIC_DIR)
    )  # => co-24: the REAL directory contents, unfiltered
    return jsonify(
        {"files": names}
    )  # => co-24: leaks "secret-notes.txt" exists, before anyone even fetches it


@app.route(
    "/legacy/files/<path:filename>"
)  # => co-24: VULNERABLE -- serves ANY file in the folder, no allow-list
def legacy_get_file(
    filename: str,
) -> object:  # => co-24: returns a Flask Response object -- the vulnerable fetch route
    return send_from_directory(
        STATIC_DIR, filename
    )  # => co-24: no filtering at all -- secret-notes.txt is fetchable


@app.route(
    "/legacy/login", methods=["POST"]
)  # => co-24: VULNERABLE -- a real, hardcoded default credential pair
def legacy_login() -> (
    object
):  # => co-24: returns a Flask Response object -- the vulnerable login route
    body = request.get_json(
        force=True
    )  # => co-01: attacker-controlled -- the real submitted credentials
    # => seeded bug: "admin"/"admin" is the SHIPPED default, never rotated, checked in plain code
    if (
        body.get("username") == "admin" and body.get("password") == "admin"
    ):  # => co-24: the real default-cred check
        return jsonify(
            {"status": "logged in as admin"}
        ), 200  # => co-24: a real 200 -- the default cred still works
    return jsonify(
        {"error": "invalid credentials"}
    ), 401  # => co-24: a real 401 for anything else


@app.route(
    "/secure/files/<path:filename>"
)  # => co-24: FIXED -- an explicit allow-list, no listing route at all
def secure_get_file(
    filename: str,
) -> object:  # => co-24: returns a Flask Response object -- the fixed fetch route
    if (
        filename not in PUBLIC_ALLOW_LIST
    ):  # => co-24: the fix -- membership check BEFORE touching the filesystem
        abort(
            404
        )  # => co-24: a real 404 -- indistinguishable from "no such file" for anything not allow-listed
    return send_from_directory(
        STATIC_DIR, filename
    )  # => co-24: only reached for a genuinely allow-listed name


ROTATED_ADMIN_PASSWORD = os.environ.get(
    "EX50_ADMIN_PASSWORD", "kJ8-x2Qz-9vM1-rotated"
)  # => co-24: NOT "admin"


@app.route(
    "/secure/login", methods=["POST"]
)  # => co-24: FIXED -- the default credential is rotated, not hardcoded-weak
def secure_login() -> (
    object
):  # => co-24: returns a Flask Response object -- the fixed login route
    body = request.get_json(
        force=True
    )  # => co-01: the SAME shape of attacker-controlled input as the vulnerable route
    if (
        body.get("username") == "admin"
        and body.get("password") == ROTATED_ADMIN_PASSWORD
    ):  # => co-24: a real, rotated check
        return jsonify(
            {"status": "logged in as admin"}
        ), 200  # => co-24: only the ROTATED password ever succeeds
    return jsonify(
        {"error": "invalid credentials"}
    ), 401  # => co-24: the SAME 401 the vulnerable route uses for failure


if (
    __name__ == "__main__"
):  # => co-24: only runs when launched directly, e.g. `python3 app.py &`
    seed_static_dir()  # => co-24: create the real on-disk files before the server starts accepting requests
    app.run(
        host="127.0.0.1", port=5050
    )  # => co-24: localhost-only, fixed port -- exploit_and_fix.py targets this
