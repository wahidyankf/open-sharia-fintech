"""Example 45: a live Flask app -- `?next=` followed blindly after login, then an allow-list fixes it (co-28)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the redirect issue itself

from urllib.parse import (
    urlparse,
)  # => co-28: stdlib URL parsing -- decides whether a target is same-site or not

from flask import (
    Flask,
    redirect,
    request,
)  # => co-28: redirect() builds a real 302 with a Location header

app = Flask(
    __name__
)  # => co-28: one Flask app, hosting both the vulnerable and fixed post-login redirect routes
SAFE_DEFAULT = "/dashboard"  # => co-28: the fallback destination when `next` is missing OR rejected


@app.route(
    "/legacy/post-login"
)  # => co-28: VULNERABLE -- redirects to `next` with zero validation
def legacy_post_login() -> (
    object
):  # => co-28: returns a Flask Response object -- the vulnerable route
    next_url = request.args.get(
        "next", SAFE_DEFAULT
    )  # => co-01: attacker-controlled -- any string the caller sends
    # => seeded bug: next_url is handed straight to redirect() -- a scheme-relative
    # => "//evil.example.com" is parsed by browsers as a full off-site URL
    return redirect(
        next_url
    )  # => co-28: a real 302 Location header, pointed WHEREVER next_url says


def is_safe_relative_target(
    target: str,
) -> bool:  # => co-28: the fix's core check -- relative-only, never off-site
    parsed = urlparse(
        target
    )  # => co-28: splits the target into scheme/netloc/path -- the REAL parse a browser uses
    return (  # => co-28: real, explicit checks -- no scheme, no netloc, a leading slash, not a double slash
        parsed.scheme == ""
        and parsed.netloc == ""
        and target.startswith("/")
        and not target.startswith("//")
    )  # => co-28: ALL four conditions must hold -- any one failing rejects the target as unsafe


@app.route(
    "/secure/post-login"
)  # => co-28: FIXED -- only a genuinely relative path is ever honored
def secure_post_login() -> (
    object
):  # => co-28: returns a Flask Response object -- the fixed route
    next_url = request.args.get(
        "next", SAFE_DEFAULT
    )  # => co-01: still attacker-controlled, now checked before use
    if not is_safe_relative_target(
        next_url
    ):  # => co-28: the fix -- reject anything that isn't a bare relative path
        next_url = (
            SAFE_DEFAULT  # => co-28: falls back to a KNOWN, same-site destination
        )
    return redirect(
        next_url
    )  # => co-28: a real 302 Location header, now guaranteed to stay on this site


if (
    __name__ == "__main__"
):  # => co-28: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5045
    )  # => co-28: localhost-only, fixed port -- curl targets this directly
