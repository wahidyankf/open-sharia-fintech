# learning/code/ex-01-trust-boundary-map-tainted-input/trust_map.py
"""Example 1: Trust-Boundary Map -- Tainted Input."""

from __future__ import annotations
# => __future__ import: lets `list[tuple[...]]` below work identically on every
# => supported interpreter version -- DD-39 hygiene, unrelated to tainting itself

from typing import (
    NamedTuple,
)  # => co-01: a typed tuple beats a bare dict -- fields are named AND typed


class TaintedEntryPoint(
    NamedTuple
):  # => co-01: one row of the trust-boundary map this example builds
    name: str  # => the variable name as it appears in the handler
    source: str  # => co-01: WHERE this value crosses into the code (query, form, header, cookie, path)
    attacker_controlled: bool  # => co-01: the single fact every downstream validation decision depends on


# ex-01: a small Flask-shaped login handler, expressed as literal STRINGS rather
# than a running server -- this example's whole job is the taint MAP, not a live request
HANDLER_SOURCE: list[
    str
] = [  # => co-01: the handler this map describes, as literal source text
    "@app.route('/login', methods=['POST'])",  # => the route decorator -- not itself an entry point
    "def login() -> Response:",  # => the handler signature -- not itself an entry point
    "    username = request.form['username']",  # => co-01: FORM_BODY -- attacker chooses this string
    "    remember = request.args.get('remember')",  # => co-01: QUERY_STRING -- attacker chooses this
    "    ua = request.headers.get('User-Agent')",  # => co-01: HTTP_HEADER -- attacker chooses this
    "    sid = request.cookies.get('sid')",  # => co-01: COOKIE -- attacker can forge/replay this
    "    oid = request.view_args['order_id']",  # => co-01: PATH_PARAM -- attacker chooses this
    "    app_version = '2026.07'",  # => co-01: SERVER_CONSTANT -- developer-written, NOT attacker input
]

# ex-01: the map itself -- one row per boundary crossing, in the SAME order as the
# handler source above, so a reader can match each row to the line it describes
TRUST_MAP: list[
    TaintedEntryPoint
] = [  # => co-01: 5 attacker-controlled rows, 1 server-controlled row
    TaintedEntryPoint(
        "username", "FORM_BODY", True
    ),  # => co-01: POST body field -- fully attacker-chosen
    TaintedEntryPoint(
        "remember", "QUERY_STRING", True
    ),  # => co-01: URL query param -- fully attacker-chosen
    TaintedEntryPoint(
        "user_agent", "HTTP_HEADER", True
    ),  # => co-01: request header -- fully attacker-chosen
    TaintedEntryPoint(
        "session_id", "COOKIE", True
    ),  # => co-01: cookie value -- attacker can send ANY value
    TaintedEntryPoint(
        "order_id", "PATH_PARAM", True
    ),  # => co-01: URL path segment -- fully attacker-chosen
    TaintedEntryPoint(
        "app_version", "SERVER_CONSTANT", False
    ),  # => co-01: literal in source -- never tainted
]


def render_trust_map(
    entries: list[TaintedEntryPoint],
) -> str:  # => co-01: reader-facing report, one line per entry
    """Format the trust map as a reader-facing table."""
    header = f"{'ENTRY POINT':<14} | {'SOURCE':<15} | ATTACKER-CONTROLLED"  # => co-01: column header row
    rows = [
        header,
        "-" * 55,
    ]  # => co-01: header plus a cosmetic separator, both fixed report lines
    for e in (
        entries
    ):  # => co-01: one row per tainted-or-not entry point, in TRUST_MAP order
        verdict = (
            "YES" if e.attacker_controlled else "no"
        )  # => co-01: the verdict this map exists to state
        rows.append(
            f"{e.name:<14} | {e.source:<15} | {verdict}"
        )  # => co-01: one fully-formed report row
    return "\n".join(rows)  # => co-01: joined into the final printable report string


if __name__ == "__main__":
    print(
        "Handler under review:"
    )  # => co-01: names WHAT this map describes before describing it
    for line in (
        HANDLER_SOURCE
    ):  # => co-01: prints the literal handler source, for reader context
        print(line)  # => co-01: one printed source line per HANDLER_SOURCE entry
    print()  # => co-01: blank separator line between the handler and its trust map
    print(
        render_trust_map(TRUST_MAP)
    )  # => co-01: prints all 6 rows -- 5 tainted, 1 not
    tainted = sum(
        1 for e in TRUST_MAP if e.attacker_controlled
    )  # => co-01: counts the YES rows -- 5
    print(
        f"\n{tainted} of {len(TRUST_MAP)} entry points are attacker-controlled."
    )  # => co-01: "5 of 6..."
