# learning/code/ex-11-allow-list-vs-deny-list/country_code.py
"""Example 11: Allow-List vs. Deny-List."""  # => co-07: module docstring

from __future__ import (
    annotations,
)  # => co-07: DD-39 hygiene, unrelated to the validation itself

ALLOWED_COUNTRY_CODES: frozenset[str] = (
    frozenset(  # => co-07: the CLOSED set of codes this app actually supports
        {
            "US",
            "GB",
            "ID",
            "JP",
            "DE",
            "FR",
        }  # => co-07: exactly six known-good, real ISO-3166 codes
    )
)  # => co-07: end of the allow-list

BLOCKLIST_CHARACTERS: frozenset[str] = (
    frozenset(  # => co-07: an OPEN-ended guess at "dangerous" characters
        "<>;'\"\\/&|`$(){}[]"  # => co-07: quotes, shell metacharacters, HTML-special chars -- the usual suspects
    )
)  # => co-07: end of the blocklist


def is_allowed_by_allowlist(
    code: str,
) -> bool:  # => co-07: robust -- membership in a KNOWN-GOOD set
    """Accept only a code that exactly matches one of the known-good country codes."""  # => co-07: doc
    return (
        code in ALLOWED_COUNTRY_CODES
    )  # => co-07: exact match -- anything not literally listed is rejected


def is_allowed_by_blocklist(
    code: str,
) -> bool:  # => co-07: fragile -- absence of KNOWN-BAD characters
    """Accept any code that contains none of the blocklisted characters."""  # => co-07: doc
    return not any(
        ch in BLOCKLIST_CHARACTERS for ch in code
    )  # => co-07: rejects only characters someone THOUGHT of


if (
    __name__ == "__main__"
):  # => co-07: entry point -- a normal code, then the case the blocklist misses
    print(
        "=== Normal input: 'US' ==="
    )  # => co-07: sanity check -- both approaches should agree here
    print(
        f"allow-list accepts 'US': {is_allowed_by_allowlist('US')}"
    )  # => co-07: True -- listed exactly
    print(
        f"blocklist accepts 'US': {is_allowed_by_blocklist('US')}"
    )  # => co-07: True -- no bad characters present

    print(
        "\n=== Attacker input: fullwidth-Unicode homoglyph of 'US' ==="
    )  # => co-07: the case that diverges
    payload = "ＵS"  # => co-01: U+FF35 FULLWIDTH LATIN CAPITAL LETTER U, followed by ASCII 'S'
    print(
        f"payload repr: {payload!r}  (looks like 'US' when displayed, but is NOT the same string)"
    )  # => co-07
    print(
        f"allow-list accepts payload: {is_allowed_by_allowlist(payload)}"
    )  # => co-07: False -- not an EXACT match
    print(
        f"blocklist accepts payload: {is_allowed_by_blocklist(payload)}"
    )  # => co-07: True -- contains NO blocked char

    allowlist_result = is_allowed_by_allowlist(
        payload
    )  # => co-07: captured for the final comparison line
    blocklist_result = is_allowed_by_blocklist(
        payload
    )  # => co-07: captured for the final comparison line
    print(  # => co-07: the final, mechanically-checked verdict this example exists to demonstrate
        f"\nallow-list correctly rejects it, blocklist misses it: "  # => co-07: message prefix
        f"{(not allowlist_result) and blocklist_result}"  # => co-07: True -- exactly the divergence claimed above
    )  # => co-07: end of the summary print
