"""Example 34: a live Flask app -- an admin endpoint reachable by any user, then a role check fixes it (co-15, co-16)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the authorization issue itself

from functools import (
    wraps,
)  # => co-16: preserves the wrapped view function's name/metadata through the decorator

from flask import (
    Flask,
    jsonify,
    request,
)  # => co-16: request.headers reads the caller-supplied identity header

app = Flask(
    __name__
)  # => co-15: one Flask app, hosting both the vulnerable and fixed admin routes
USERS = {
    "alice": "user",
    "root": "admin",
}  # => co-16: a real role table -- alice is NOT an admin, root IS


@app.route(
    "/legacy/admin/users"
)  # => co-15: VULNERABLE -- no role check at all, only reachable via routing
def legacy_admin_users() -> tuple[
    dict[str, object], int
]:  # => co-15: returns (json_body, status)
    # => seeded bug: this handler assumes only admins ever call this URL -- nothing
    # => in the code actually enforces that assumption
    return jsonify(
        {"users": list(USERS.keys())}
    ), 200  # => co-15: leaks the FULL user list to ANY caller


def require_admin(
    view_func,
):  # => co-16: a real decorator -- the function-level check the vulnerable route lacked
    @wraps(
        view_func
    )  # => co-16: keeps Flask's URL-rule machinery happy with the wrapped function's identity
    def wrapper(
        *args: object, **kwargs: object
    ) -> tuple[dict[str, object], int]:  # => co-16: intercepts EVERY call
        caller = request.headers.get(
            "X-User-Id", ""
        )  # => co-16: who is calling -- simulates an authenticated session
        role = USERS.get(
            caller, ""
        )  # => co-16: the caller's REAL role, looked up server-side, never trusted from the client
        if (
            role != "admin"
        ):  # => co-16: the actual enforcement point -- runs BEFORE the real view function
            return jsonify(
                {"error": "forbidden"}
            ), 403  # => co-16: a real 403 -- the view function never even runs
        return view_func(
            *args, **kwargs
        )  # => co-16: only reached once the role check has already passed

    return wrapper  # => co-16: the decorated view now carries this check on every single request


@app.route(
    "/secure/admin/users"
)  # => co-16: FIXED -- the SAME logic, now behind require_admin
@require_admin  # => co-16: this ONE line is the fix -- function-level authorization, applied at the route
def secure_admin_users() -> tuple[
    dict[str, object], int
]:  # => co-16: returns (json_body, status) too
    return jsonify(
        {"users": list(USERS.keys())}
    ), 200  # => co-16: identical body -- only reachable role differs


if (
    __name__ == "__main__"
):  # => co-15: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5034
    )  # => co-15: localhost-only, fixed port -- exploit_and_fix.py targets this
