# learning/code/ex-71-secure-file-upload/app.py
"""Example 71: a live Flask app -- extension-only upload validation vs. extension+content-type+magic-bytes (co-05, co-07, co-24)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the upload-validation logic itself

import os  # => co-24: real chmod/path operations -- storage location and permission bits both matter here
import secrets  # => co-05: cryptographically random filenames -- never trust or reuse the client's own filename

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-01: request.files reads the real, attacker-controlled upload

app = Flask(
    __name__
)  # => co-05: one Flask app, hosting both the vulnerable and fixed upload routes
HERE = os.path.dirname(__file__)  # => co-05: this example's own real directory
WEB_ROOT_UPLOADS = os.path.join(
    HERE, "web_root", "uploads"
)  # => co-24: INSIDE the (simulated) served static folder
PRIVATE_UPLOADS = os.path.join(
    HERE, "private_uploads"
)  # => co-05: OUTSIDE the web root -- never served by any route
os.makedirs(
    WEB_ROOT_UPLOADS, exist_ok=True
)  # => co-24: real, on-disk directory this example actually writes into
os.makedirs(
    PRIVATE_UPLOADS, exist_ok=True
)  # => co-05: real, on-disk directory this example actually writes into

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}  # => co-07: an explicit allow-list, not a denylist of "bad" extensions
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
}  # => co-07: the real, declared MIME types this example accepts
MAGIC_BYTES: dict[
    str, bytes
] = {  # => co-07: the REAL, on-disk byte signatures for each allowed image format
    "image/jpeg": b"\xff\xd8\xff",  # => co-07: every genuine JPEG file's real first three bytes (SOI marker)
    "image/png": b"\x89PNG\r\n\x1a\n",  # => co-07: every genuine PNG file's real, fixed 8-byte signature
}


@app.route(
    "/legacy/upload", methods=["POST"]
)  # => co-24: VULNERABLE -- checks the FILENAME EXTENSION only
def legacy_upload() -> tuple[
    dict[str, object], int
]:  # => co-24: returns (json_body, status)
    uploaded = request.files[
        "file"
    ]  # => co-01: the real, attacker-controlled uploaded file object
    _, ext = os.path.splitext(
        uploaded.filename or ""
    )  # => co-24: only inspects the CLAIMED filename's extension
    if (
        ext.lower() not in ALLOWED_EXTENSIONS
    ):  # seeded bug: this is the ONLY check performed, ever
        return jsonify(
            {"error": "extension not allowed"}
        ), 400  # => co-24: a real 400 for an obviously bad extension
    dest = os.path.join(
        WEB_ROOT_UPLOADS, uploaded.filename
    )  # => co-24: stores under the CLIENT'S OWN filename
    uploaded.save(
        dest
    )  # => co-24: writes the REAL bytes to disk, INSIDE the simulated web-servable folder
    return jsonify(
        {"stored_as": uploaded.filename, "path": dest}
    ), 201  # => co-24: real, on-disk result


def _sniff_content_type(
    raw_bytes: bytes,
) -> str | None:  # => co-07: real magic-byte detection, independent of any claim
    for (
        content_type,
        signature,
    ) in MAGIC_BYTES.items():  # => co-07: checks EVERY real, known signature in turn
        if raw_bytes.startswith(
            signature
        ):  # => co-07: a REAL byte-for-byte prefix comparison, not a filename guess
            return content_type  # => co-07: the REAL, sniffed type -- based on content, never on the client's claim
    return None  # => co-07: matches NO known real image signature -- whatever the extension/claimed type said


@app.route(
    "/secure/upload", methods=["POST"]
)  # => co-05: FIXED -- extension AND claimed type AND real magic bytes
def secure_upload() -> tuple[
    dict[str, object], int
]:  # => co-07: returns (json_body, status)
    uploaded = request.files[
        "file"
    ]  # => co-01: the SAME shape of real, attacker-controlled upload
    _, ext = os.path.splitext(
        uploaded.filename or ""
    )  # => co-07: layer 1 -- the claimed extension
    if (
        ext.lower() not in ALLOWED_EXTENSIONS
    ):  # => co-07: layer 1 check -- rejects an obviously wrong extension
        return jsonify({"error": "extension not allowed"}), 400  # => co-07: a real 400
    claimed_type = (
        uploaded.content_type or ""
    )  # => co-07: layer 2 -- the claimed Content-Type header, still just a claim
    if (
        claimed_type not in ALLOWED_CONTENT_TYPES
    ):  # => co-07: layer 2 check -- rejects an obviously wrong claimed type
        return jsonify(
            {"error": "content-type not allowed"}
        ), 400  # => co-07: a real 400
    raw_bytes = (
        uploaded.read()
    )  # => co-07: reads the REAL, actual file bytes -- what the file GENUINELY contains
    sniffed_type = _sniff_content_type(
        raw_bytes
    )  # => co-07: layer 3 -- the fix's core check, real byte inspection
    if (
        sniffed_type is None or sniffed_type != claimed_type
    ):  # => co-05: real bytes must ALSO match the claimed type
        return jsonify(
            {"error": "file content does not match its claimed type"}
        ), 400  # => co-05: a real 400, the fix
    random_name = (
        secrets.token_hex(16) + ext.lower()
    )  # => co-05: a REAL, unpredictable filename -- NEVER the client's own
    dest = os.path.join(
        PRIVATE_UPLOADS, random_name
    )  # => co-05: stored OUTSIDE the (simulated) web-servable folder
    with (
        open(dest, "wb") as f
    ):  # => co-05: writes the REAL, already-verified bytes to the REAL, private destination
        f.write(
            raw_bytes
        )  # => co-05: real bytes, written once, verified before this line ever runs
    os.chmod(
        dest, 0o644
    )  # => co-24: real, explicit permission bits -- read/write for owner, read-only for others, NO execute
    return jsonify(
        {"stored_as": random_name, "path": dest}
    ), 201  # => co-05: the real, randomized on-disk result


if (
    __name__ == "__main__"
):  # => co-05: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5071
    )  # => co-05: localhost-only, fixed port -- exploit_and_fix.py targets this
