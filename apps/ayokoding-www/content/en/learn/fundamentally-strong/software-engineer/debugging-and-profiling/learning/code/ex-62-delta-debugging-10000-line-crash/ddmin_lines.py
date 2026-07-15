"""Example 62: automated line-based ddmin on a 10,000-line crashing input,
reduced to under 10 lines while still triggering the IDENTICAL exception.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to delta-debugging itself

import sys  # => needed only for sys.path.insert below

sys.path.insert(
    0, "."
)  # => co-11: makes local csv_parser.py importable regardless of caller's cwd
from csv_parser import parse_lines  # noqa: E402  # => co-11: the function under minimization, unchanged from ex-45/46


def make_10000_line_input() -> list[
    str
]:  # => co-11: builds the LARGE, realistic-looking crashing input
    lines = [
        f"item-{i},{i},{i * 3}" for i in range(9999)
    ]  # => co-11: 9,999 perfectly valid rows
    lines.insert(4321, "item-bad,4321,")  # =>  the ONE crashing row, buried deep
    return (
        lines  # => co-11: 10,000 lines total -- one crash buried among 9,999 valid rows
    )


def crash_signature(
    lines: list[str],
) -> str | None:  # => co-11: the SAME oracle shape as ex-45/46/capstone
    try:  # => co-11: catches whatever parse_lines() actually raises, to compare signatures across candidates
        parse_lines(
            lines
        )  # => co-11: the SAME function under minimization, called with a candidate subset
    except Exception as exc:  # noqa: BLE001 -- deliberately broad: we compare signatures  # => co-11
        return f"{type(exc).__name__}: {exc}"  # => co-11: the signature ddmin_lines compares against the original
    return None  # => co-11: no exception at all -- this candidate does NOT reproduce the crash


def ddmin_lines(
    lines: list[str], target_signature: str
) -> list[str]:  # => co-11: the automated, n-way ddmin loop
    n = 2  # => co-11: starts by splitting the input into 2 chunks, same shape as ex-46's string ddmin
    current = list(
        lines
    )  # => co-11: the SMALLEST failing input found SO FAR -- shrinks across iterations
    while len(current) >= 2:  # => co-11: stops once no further splitting is possible
        chunk_size = max(
            1, len(current) // n
        )  # => co-11: at least 1 line per chunk, even as current shrinks
        chunks = [
            current[i : i + chunk_size] for i in range(0, len(current), chunk_size)
        ]  # => co-11: n roughly-equal chunks
        reduced = False  # => co-11: tracks whether THIS pass found a smaller failing candidate
        for i in range(
            len(chunks)
        ):  # => co-11: tries removing each chunk in turn, one at a time
            candidate = [
                line for j, chunk in enumerate(chunks) if j != i for line in chunk
            ]  # => co-11: all EXCEPT chunk i
            if (
                candidate and crash_signature(candidate) == target_signature
            ):  # => co-11: still fails the SAME way?
                current = candidate  # => co-11: keeps the smaller candidate -- a genuine reduction
                n = max(
                    n - 1, 2
                )  # => co-11: retries with fewer chunks next pass, per the classic ddmin algorithm
                reduced = (
                    True  # => co-11: signals the outer while loop to continue shrinking
                )
                break  # => co-11: restarts chunking from the new, smaller current
        if (
            not reduced
        ):  # => co-11: no single-chunk removal reproduced the crash this pass
            if n >= len(
                current
            ):  # => co-11: already at maximum granularity -- cannot split further
                break  # => co-11: ddmin has converged -- current is now 1-minimal
            n = min(
                n * 2, len(current)
            )  # => co-11: doubles the chunk count for a finer-grained next attempt
    return current  # => co-11: the final, minimized-but-still-crashing input


def main() -> (
    None
):  # => co-11: builds the 10,000-line input, minimizes it, and verifies the result
    original = (
        make_10000_line_input()
    )  # => co-11: the large, realistic-looking starting input
    original_signature = crash_signature(
        original
    )  # => co-11: the exception ddmin must preserve exactly
    assert original_signature is not None, (
        "sanity check: original 10,000-line input must crash"
    )  # => co-11
    print(
        f"original input: {len(original)} lines"
    )  # => co-11: confirms the starting size before minimizing
    print(
        f"original crash: {original_signature}"
    )  # => co-11: the exact signature the minimized case must match

    minimal = ddmin_lines(
        original, original_signature
    )  # => co-11: the automated reduction, start to finish
    minimal_signature = crash_signature(
        minimal
    )  # => co-11: re-derives the signature from the MINIMIZED input
    print(
        f"minimized input: {len(minimal)} lines"
    )  # => co-11: the headline result -- how far it shrank
    print(
        f"minimized lines: {minimal!r}"
    )  # => co-11: shows the actual surviving line(s), for a human to read
    print(
        f"minimized crash: {minimal_signature}"
    )  # => co-11: proves the SAME exception, not a different one

    assert minimal_signature == original_signature, (
        "minimized input must raise the IDENTICAL exception"
    )  # => co-11
    assert len(minimal) < 10, (
        f"expected under 10 lines, got {len(minimal)}"
    )  # => co-11: the syllabus's own target
    print(
        f"confirmed: {len(original)} lines reduced to {len(minimal)}, same exception preserved exactly"
    )  # => co-11


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that builds, minimizes, and verifies the crashing input
