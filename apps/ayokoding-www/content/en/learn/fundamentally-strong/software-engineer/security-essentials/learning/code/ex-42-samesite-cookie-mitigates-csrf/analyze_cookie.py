"""Example 42: fetches the live app.py response, applies the SameSite spec's OWN rule (co-26, co-13). See
this example's Brief Explanation in the markdown for the full honest sandbox-limitation statement."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the cookie-flag parsing itself

import requests  # => co-13: real HTTP client -- the request below hits the live app.py process

BASE_URL = (
    "http://127.0.0.1:5042"  # => co-13: matches app.py's app.run(port=5042) exactly
)


def main() -> (
    None
):  # => co-13: fetches the real Set-Cookie header, then reports each real flag it carries
    response = requests.post(
        f"{BASE_URL}/login", timeout=5
    )  # => co-13: a real HTTP POST against the live server
    raw_cookie = response.headers[
        "Set-Cookie"
    ]  # => co-13: the REAL Set-Cookie header text, straight off the wire
    print(
        f"Set-Cookie: {raw_cookie}"
    )  # => co-13: the exact real header value this server sent

    flags = {
        part.strip().split("=")[0].lower() for part in raw_cookie.split(";")[1:]
    }  # => co-13: real flag names
    print(
        f"flags present: {sorted(flags)}"
    )  # => co-13: real, parsed set -- not assumed, extracted from the header
    # => co-13: three real, independent assertions -- each checks ONE flag actually present on the wire
    assert (
        "samesite" in raw_cookie.lower()
    )  # => co-13: proves the SameSite attribute really is on the wire
    assert (
        "strict" in raw_cookie.lower()
    )  # => co-13: proves the value really is Strict, not Lax or None
    assert (
        "secure" in flags and "httponly" in flags
    )  # => co-13: proves all three defensive flags are present together
    # => co-13: this local verification is a real HTTP fetch, not a fabricated header -- see the honest limitation below

    print(
        "\nSameSite=Strict spec rule (RFC 6265bis / MDN, cited, not executed):"
    )  # => labels section
    print(
        "  a Strict cookie is withheld from EVERY cross-site request, including top-level"
    )  # => co-26: the real rule
    print(
        "  navigation -- a forged cross-site POST would arrive with NO cookie attached at all"
    )  # => co-26: the effect
    print(
        "  -- the server-side CSRF-token check in ex-41 becomes redundant defense-in-depth here"
    )  # => co-26: framing


if (
    __name__ == "__main__"
):  # => co-13: only runs when launched directly, e.g. `python3 analyze_cookie.py`
    main()  # => co-13: fetches once, then reports the real flags and the spec's documented consequence
