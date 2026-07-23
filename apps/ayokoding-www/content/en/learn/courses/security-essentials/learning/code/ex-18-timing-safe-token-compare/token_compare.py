# learning/code/ex-18-timing-safe-token-compare/token_compare.py
"""Example 18: Timing-Safe Token Compare."""  # => co-11: module docstring

from __future__ import (
    annotations,
)  # => co-11: DD-39 hygiene, unrelated to the comparison itself

import hmac  # => co-11: hmac.compare_digest -- the constant-time comparison this example recommends
import secrets  # => co-11: secrets.token_hex -- a real, unguessable token, generated fresh per run


def naive_equal(
    candidate: str, real_token: str
) -> bool:  # => co-11: the UNSAFE comparison -- short-circuits early
    """Compare two tokens with plain '==' -- LEAKS timing per mismatched byte position."""  # => co-11: doc
    return (
        candidate == real_token
    )  # => co-11: CPython exits at the FIRST differing byte -- position-dependent time


def safe_equal(
    candidate: str, real_token: str
) -> bool:  # => co-11: the SAFE comparison -- constant-time BY CONSTRUCTION
    """Compare two tokens with hmac.compare_digest -- constant-time, position-independent."""  # => co-11: doc
    return hmac.compare_digest(
        candidate, real_token
    )  # => co-11: always walks every byte, regardless of WHERE it differs


def print_timing_explanation() -> (
    None
):  # => co-11: the printed explanation the syllabus requires -- OUTPUT, not just a comment
    """Print, in the script's own real output, why '==' leaks a timing side-channel."""  # => co-11: doc
    print(
        "WHY '==' LEAKS A TIMING SIDE-CHANNEL, PER CHARACTER:"
    )  # => co-11: heading for the printed explanation
    print(
        "CPython's string/bytes '==' short-circuits: it returns False the INSTANT"
    )  # => co-11: mechanism, line 1
    print(
        "it finds the first mismatched byte, without comparing anything after it."
    )  # => co-11: mechanism, line 2
    print(
        "A guess that differs at byte 0 returns FASTER than a guess that differs at"
    )  # => co-11: consequence, line 1
    print(
        "byte 31 of a 32-byte token, because the second guess made '==' do MORE work."
    )  # => co-11: consequence, line 2
    print(
        "Timed over many requests, that gap lets an attacker recover a secret token"
    )  # => co-11: exploit, line 1
    print(
        "ONE BYTE AT A TIME, instead of needing to guess the whole token at once."
    )  # => co-11: exploit, line 2
    print(
        "hmac.compare_digest removes this signal: it always walks EVERY byte of both"
    )  # => co-11: fix, line 1
    print(
        "inputs, so its running time depends only on LENGTH, never on mismatch position."
    )  # => co-11: fix, line 2


if (
    __name__ == "__main__"
):  # => co-11: entry point -- correctness parity first, then the printed explanation
    real_token = secrets.token_hex(
        32
    )  # => co-11: a real, freshly-generated 64-hex-char secret, this run only
    print(
        f"Real token: {real_token}"
    )  # => co-11: what the server actually holds -- never sent back to a client

    wrong_early = (
        "0" + real_token[1:]
    )  # => co-11: differs at byte 0 -- naive_equal would return FASTEST
    wrong_late = real_token[:-1] + (
        "1" if real_token[-1] != "1" else "2"
    )  # => co-11: differs at the LAST byte

    print(
        "\n=== Both comparisons must agree on every outcome ==="
    )  # => co-11: correctness, not timing, is checked here
    cases = [
        ("correct", real_token),
        ("wrong-early", wrong_early),
        ("wrong-late", wrong_late),
    ]  # => co-11: 3 test cases
    for label, candidate in cases:  # => co-11: one comparison pair per case
        n = naive_equal(
            candidate, real_token
        )  # => co-11: the unsafe comparison's verdict for this candidate
        s = safe_equal(
            candidate, real_token
        )  # => co-11: the safe comparison's verdict for the SAME candidate
        print(
            f"{label:<12} naive_equal={n!s:<5} safe_equal={s!s:<5} agree={n == s}"
        )  # => co-11: both MUST agree
        assert (
            n == s
        )  # => co-11: mechanically proves correctness parity -- they differ ONLY in timing, never in result

    print()  # => co-11: blank separator before the printed explanation
    print_timing_explanation()  # => co-11: the actual "verify" for this example -- a genuine, captured printed statement
